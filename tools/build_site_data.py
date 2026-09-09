"""
Regenerate the published site data from a LAI4EO harmonised release.

    "…/LAI database/.venv/bin/python" tools/build_site_data.py \
        ../../Database/private_lai4eo_dataset_YYYY-MM-DD.csv

Writes three files, all world-readable once committed:

    _data/stats.yaml              top-level counts and lists
    _data/sites.yaml              one row per site
    assets/data/measurements.json the same site rows, for the map

The input is the PRIVATE release. The output is aggregates only. What may be
published is fixed and exhaustive:

    site name at region grain, country, measurement count, crop mix and
    instrument mix per site, the global year span, and the top-level counts.

Never: an LAI value of any kind including a mean, any date, any per-site year
range, any coordinate finer than a cluster centroid, any per-measurement row.
Nothing in this script reads `lai_mean`, `lai_std` or a full `datetime_utc`,
and that is deliberate — see website/guide/STATE.md, "Settled 2026-09-08".

Country and site name are DERIVED from Natural Earth, not typed. A hand-typed
table is how a four-country dataset came to report three. Needs geopandas, so
run it with the parent venv, not the website one.

The script fails loudly and writes nothing at all if it cannot account for
every row. A warning printed under three lines saying "wrote …" is a warning
nobody reads.
"""

import collections
import csv
import json
import re
import sys
from pathlib import Path

# how close two points must be (degrees) to be treated as the same site
CLUSTER_DEG = 0.4

# published coordinate precision, in decimal places. 2 dp is ~1 km: enough to
# put a circle over the right district, far too coarse to be a field.
CENTROID_DP = 2

# source_id -> contributing institution.
#
# This is the one field that cannot be derived from anything else, so an
# unmapped source_id is a hard error, not a fallback. The raw string is
# "<place>_<firstname>_<ingestion date>": letting it through would publish a
# contributor's name and a folder date in _data/stats.yaml, which is
# world-readable on GitHub whether or not any page renders it.
CONTRIBUTORS = {
    "CNR-IREA_Francesco_2026-04-23": "CNR-IREA",
    "Monash_Yuval_2026-03-17": "Monash University",
    "Harvest_Josef_2026-03-17": "NASA Harvest / SatFarming",
    "Valencia_Katarzyna_2026-07-28": "University of Valencia",
}

# instrument model -> display label
INSTRUMENTS = {
    "LAI-2000": "LI-COR LAI-2000",
    "LAI-2200": "LI-COR LAI-2200",
    "LAI-2200c": "LI-COR LAI-2200C",
    "LP-80": "AccuPAR LP-80",
    "PocketLAI": "PocketLAI",
    "DHP": "Hemispherical photography",
}

# (country, Natural Earth admin-1 name) -> the name we publish instead.
#
# The default is "<admin-1>, <country>" — boring, deterministic, and right the
# moment a new region arrives. An entry here upgrades one site to the name its
# contributor actually uses. Add one only once the contributor has confirmed
# it: every name below was inferred from coordinates by eye and none has been
# checked yet (see guide/TODO.md).
#
# Because the key is the derived admin-1 unit, an override cannot contradict
# the geography — a name for a region that is not in this release is reported
# as unused rather than silently applied to the wrong site.
SITE_NAMES = {
    ("Italy", "Ferrara"): "Po Valley (Emilia-Romagna)",
    ("Italy", "Pavia"): "Lomellina rice district (Lombardy)",
    ("Italy", "Grosseto"): "Maremma (Tuscany)",
    ("Italy", "Oristano"): "Oristano plain (Sardinia)",
    ("Italy", "Vercelli"): "Vercelli rice district (Piedmont)",
    ("France", "Eure-et-Loir"): "Beauce (Eure-et-Loir)",
    ("Australia", "Victoria"): "Wimmera-Mallee (Victoria)",
}


class Stop(Exception):
    """Something the script must not guess at. Nothing is written."""


# ---------------------------------------------------------------- geography


class Places:
    """Natural Earth lookups: a point -> its country and its admin-1 region."""

    def __init__(self, geo_dir):
        try:
            import geopandas as gpd
            from shapely.geometry import Point
        except ImportError:
            raise Stop(
                "geopandas is not importable.\n"
                "  Run this with the parent venv, which has it:\n"
                '    "…/LAI database/.venv/bin/python" tools/build_site_data.py …'
            )
        self._point = Point

        self.admin0 = self._load(gpd, geo_dir, "ne_10m_admin_0_sovereignty")
        self.admin1 = self._load(gpd, geo_dir, "ne_10m_admin_1_states_provinces")
        self._cache = {}

    @staticmethod
    def _load(gpd, geo_dir, stem):
        shp = geo_dir / stem / f"{stem}.shp"
        if not shp.exists():
            raise Stop(
                f"missing shapefile: {shp}\n"
                "  Download it from naturalearthdata.com -> 10m Cultural, and\n"
                f"  unzip it into {geo_dir / stem}/"
            )
        frame = gpd.read_file(shp)
        return frame, frame.sindex

    def _hit(self, layer, lat, lon):
        frame, sindex = layer
        pt = self._point(lon, lat)  # note: Point takes lon, lat
        for i in sindex.query(pt):
            if frame.geometry.iloc[i].contains(pt):
                return frame.iloc[i]
        return None

    def lookup(self, lat, lon):
        """(country, admin-1 name) for one point; either may be None."""
        key = (round(lat, 4), round(lon, 4))
        if key not in self._cache:
            hit0 = self._hit(self.admin0, lat, lon)
            hit1 = self._hit(self.admin1, lat, lon)
            country = hit0["ADMIN"] if hit0 is not None else None
            # name_en is the English form; `name` is local and carries the odd
            # typo ("Oristrano"), so prefer name_en and fall back.
            region = None
            if hit1 is not None:
                region = hit1["name_en"] or hit1["name"]
            self._cache[key] = (country, region)
        return self._cache[key]


# ---------------------------------------------------------------- helpers


def title_crop(name):
    """Crop names are inconsistently cased in the source data."""
    fixes = {"sorgum": "sorghum", "sugarbeet": "sugar beet"}
    name = name.strip().lower()
    return fixes.get(name, name)


def yaml_str(s):
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"'


def modal(counter, label, where):
    """The one value the majority of a cluster's points agree on."""
    if not counter:
        raise Stop(f"no {label} resolved for the site at {where}")
    return counter.most_common(1)[0][0]


# ---------------------------------------------------------------- clustering


def cluster_sites(rows, places):
    """Group measurements into sites, and name each site from the map."""
    clusters = []
    for r in rows:
        if not r.get("lat", "").strip() or not r.get("lon", "").strip():
            raise Stop(
                "a row has no coordinates, so it belongs to no site and would "
                "vanish from the counts. Fix the release, not this script."
            )
        lat, lon = float(r["lat"]), float(r["lon"])
        for c in clusters:
            if abs(c["lat"] - lat) < CLUSTER_DEG and abs(c["lon"] - lon) < CLUSTER_DEG:
                c["rows"].append(r)
                c["pts"].append((lat, lon))
                break
        else:
            clusters.append({"lat": lat, "lon": lon, "rows": [r], "pts": [(lat, lon)]})

    sites, used_overrides = [], set()
    for c in clusters:
        rs = c["rows"]
        lat = round(sum(p[0] for p in c["pts"]) / len(c["pts"]), CENTROID_DP)
        lon = round(sum(p[1] for p in c["pts"]) / len(c["pts"]), CENTROID_DP)
        where = f"{lat:.2f},{lon:.2f}"

        # A cluster can straddle a boundary — the Lomellina one spans five
        # provinces — so take what most of its points agree on rather than
        # whatever polygon the centroid happens to land in.
        countries, regions = collections.Counter(), collections.Counter()
        for plat, plon in c["pts"]:
            country, region = places.lookup(plat, plon)
            if country:
                countries[country] += 1
            if region:
                regions[region] += 1
        country = modal(countries, "country", where)
        region = modal(regions, "admin-1 region", where)

        key = (country, region)
        if key in SITE_NAMES:
            name = SITE_NAMES[key]
            used_overrides.add(key)
        else:
            name = f"{region}, {country}"

        crops = collections.Counter(
            title_crop(r["dominant_species_or_crop"])
            for r in rs
            if r["dominant_species_or_crop"].strip()
        )
        instruments = collections.Counter(
            INSTRUMENTS.get(r["lai_instrument_model"], r["lai_instrument_model"])
            for r in rs
            if r["lai_instrument_model"].strip()
        )
        for src in {r["source_id"] for r in rs}:
            if src not in CONTRIBUTORS:
                raise Stop(unmapped_source_message(src))

        sites.append({
            "name": name,
            "country": country,
            "lat": lat,
            "lon": lon,
            "count": len(rs),
            "main_crop": crops.most_common(1)[0][0] if crops else "",
            "crops": crops.most_common(),
            "instruments": instruments.most_common(),
        })

    duplicates = [n for n, k in collections.Counter(
        s["name"] for s in sites).items() if k > 1]
    if duplicates:
        raise Stop(
            "two sites resolved to the same published name: "
            + ", ".join(duplicates)
            + "\n  Two clusters share an admin-1 region. Give at least one of "
              "them its own name — SITE_NAMES is keyed on the region, so it "
              "cannot tell them apart."
        )

    unused = sorted(set(SITE_NAMES) - used_overrides)
    return sorted(sites, key=lambda s: -s["count"]), unused


def unmapped_source_message(src):
    return (
        f"unmapped source_id: {src!r}\n"
        "  Add it to CONTRIBUTORS near the top of this script and re-run.\n"
        "  Do NOT work around this. A source_id is\n"
        "  '<place>_<firstname>_<ingestion date>', and _data/stats.yaml is\n"
        "  world-readable on GitHub — the fallback this replaced would have\n"
        "  published a contributor's name and a folder date."
    )


# ---------------------------------------------------------------- writing


def build_stats(rows, sites):
    def filled(key):
        return [r[key] for r in rows if r.get(key, "").strip()]

    crops = sorted({title_crop(c) for c in filled("dominant_species_or_crop")})
    instruments = sorted({INSTRUMENTS.get(i, i) for i in filled("lai_instrument_model")})
    countries = sorted({s["country"] for s in sites})
    contributors = sorted({CONTRIBUTORS[s] for s in filled("source_id")})
    # the global span only. A per-site year range narrows a campaign to one
    # group's field season, which is theirs to disclose, not ours.
    years = sorted({d[:4] for d in filled("datetime_utc")})
    areas = [float(v) for v in filled("esu_area")]

    return {
        "measurements": len(rows),
        "sampling_units": len(set(filled("esu_id"))),
        "field_plots": len(set(filled("plot_id"))),
        "crops": len(crops),
        "instruments": len(instruments),
        "countries": len(countries),
        "contributors": len(contributors),
        "sites": len(sites),
        "year_min": years[0],
        "year_max": years[-1],
        "esu_area_min": min(areas),
        "esu_area_max": max(areas),
        "bbch_records": len(filled("phenology_stage")),
        "std_records": len(filled("lai_std")),
        "rtk_records": sum(1 for r in rows if r.get("gps_protocol", "").strip() == "RTK"),
    }, crops, instruments, countries, contributors


def render_stats(stats, crops, instruments, countries, contributors, release):
    out = ["# DO NOT EDIT - generated by tools/build_site_data.py",
           f"# release: {release}", ""]
    out += [f"{k}: {v}" for k, v in stats.items()]

    for label, values, quote in (
        ("crop_list", crops, False),
        ("instrument_list", instruments, True),
        ("country_list", countries, False),
        ("contributor_list", contributors, True),
    ):
        out += ["", f"{label}:"]
        out += [f"  - {yaml_str(v) if quote else v}" for v in values]
    return "\n".join(out) + "\n"


def render_sites(sites, release):
    out = ["# DO NOT EDIT - generated by tools/build_site_data.py",
           f"# release: {release}",
           "#",
           "# Aggregates only. lat/lon are cluster centroids rounded to "
           f"{CENTROID_DP} dp (~1 km),",
           "# never a measurement position. No LAI value and no date is "
           "published here.",
           ""]
    for s in sites:
        out.append(f"- name: {yaml_str(s['name'])}")
        out.append(f"  country: {yaml_str(s['country'])}")
        out.append(f"  lat: {s['lat']}")
        out.append(f"  lon: {s['lon']}")
        out.append(f"  count: {s['count']}")
        out.append(f"  main_crop: {yaml_str(s['main_crop'])}")
        out.append("  crops:")
        out += [f"    - {{ name: {yaml_str(n)}, count: {k} }}" for n, k in s["crops"]]
        out.append("  instruments:")
        out += [f"    - {{ name: {yaml_str(n)}, count: {k} }}" for n, k in s["instruments"]]
        out.append("")
    return "\n".join(out)


def render_json(sites):
    """The map reads this. Same rows as _data/sites.yaml, nothing extra."""
    return json.dumps(
        {
            "sites": [
                {
                    "name": s["name"],
                    "country": s["country"],
                    "lat": s["lat"],
                    "lon": s["lon"],
                    "count": s["count"],
                    "main_crop": s["main_crop"],
                    "crops": [[n, k] for n, k in s["crops"]],
                    "instruments": [[n, k] for n, k in s["instruments"]],
                }
                for s in sites
            ],
        },
        separators=(",", ":"),
    )


# ---------------------------------------------------------------- main


def main(csv_path, geo_dir=None):
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise Stop(f"no such release: {csv_path}")
    # the shapefiles live beside the release, in Database/misc/
    geo_dir = Path(geo_dir) if geo_dir else csv_path.parent / "misc"
    # the release date, not the file name. The generated files are committed,
    # and "private_lai4eo_dataset_….csv" is not ours to advertise.
    match = re.search(r"\d{4}-\d{2}-\d{2}", csv_path.stem)
    release = match.group(0) if match else "unknown"

    rows = list(csv.DictReader(csv_path.open(newline="", encoding="utf-8")))
    if not rows:
        raise Stop(f"{csv_path.name} has no rows")

    places = Places(geo_dir)
    sites, unused = cluster_sites(rows, places)
    stats, crops, instruments, countries, contributors = build_stats(rows, sites)

    # everything has resolved; only now does anything reach disk
    Path("_data/stats.yaml").write_text(
        render_stats(stats, crops, instruments, countries, contributors, release),
        encoding="utf-8")
    Path("_data/sites.yaml").write_text(render_sites(sites, release), encoding="utf-8")
    points = Path("assets/data/measurements.json")
    points.parent.mkdir(parents=True, exist_ok=True)
    points.write_text(render_json(sites), encoding="utf-8")

    print(f"source: {csv_path.name} -> release {release} "
          f"({stats['measurements']} measurements)")
    print(f"wrote _data/stats.yaml    {stats['countries']} countries, "
          f"{stats['crops']} crops, {stats['contributors']} contributors")
    print(f"wrote _data/sites.yaml    {len(sites)} sites")
    print(f"wrote {points}  {points.stat().st_size // 1024 or 1} KB")
    print()
    width = max(len(s["name"]) for s in sites)
    for s in sites:
        print(f"  {s['count']:5d}  {s['name']:<{width}}  {s['country']}")
    if unused:
        print()
        for key in unused:
            print(f"  note: SITE_NAMES has {SITE_NAMES[key]!r} for {key[1]}, "
                  f"{key[0]} - no site there in this release")
    print()
    print("Review before committing:  git diff _data/ assets/data/")


if __name__ == "__main__":
    if not 2 <= len(sys.argv) <= 3:
        sys.exit(__doc__)
    try:
        main(*sys.argv[1:])
    except Stop as e:
        sys.exit(f"\nSTOPPED, nothing written.\n\n  {e}\n")
