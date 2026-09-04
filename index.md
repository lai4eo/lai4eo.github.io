---
layout: default
---

{% assign s = site.data.stats %}

{% include section.html size="full" %}

<div class="page-hero" style="background-image: url('{{ "images/background.jpg" | relative_url }}')">
  <div class="page-hero-inner">
    <h1>Harmonising global crop leaf-area measurements</h1>
    <p>
      A global, open collection of in-situ <strong>Leaf Area Index</strong> measurements
      over cropland &mdash; harmonised for validating Sentinel-2-era satellite products.
    </p>
  </div>
</div>

{% include section.html size="page" %}

<div class="hero-buttons">
  {%
    include button.html
    link="contribute"
    text="Contribute your measurements"
    icon="fa-solid fa-hand-holding-heart"
    tooltip="How to add your dataset to the database"
  %}
  {%
    include button.html
    link="https://doi.org/10.5281/zenodo.21246927"
    text="Explore the data"
    icon="fa-solid fa-database"
    style="bare"
    tooltip="Starter Dataset v1.0 on Zenodo"
  %}
</div>

{% include stats.html %}

{% include section.html size="wide" %}

## Where the measurements come from

Every circle is a measurement site, sized by how many elementary sampling units it
contributed. Filter by crop or instrument to see what the database holds.

{% include measurement-map.html height="500px" %}

{% capture gap_text %}
**Help us fill the map.** The current release has {{ s.contributors }} contributors in
{{ s.countries }} countries, with **no data from Africa, Asia, or the Americas**, and
nearly four-fifths of records drawn from rice and wheat. If your group holds in-situ LAI
measurements over agricultural land &mdash; a single season or several decades, published
or not &mdash; they belong here.
{% endcapture %}

{% include alert.html type="tip" content=gap_text %}

{% include section.html dark=true size="page" %}

## Why this is needed

{% capture col1 %}

### The validation gap

No satellite-derived LAI product has passed **CEOS Stage 2** validation. The reason is
in-situ coverage: too few sites, and gaps in space and time.

**DIRECT V2.1**, the reference collection behind most product intercomparison, holds
280 LAI values from 176 sites, averaged over 3&nbsp;km&nbsp;&times;&nbsp;3&nbsp;km to match
MODIS. Four-fifths are cropland &mdash; but 161 of those come from China, and only
**two were collected after 2017**, when Sentinel-2 brought 10&nbsp;m products.

Copernicus **GBOV** spans over 150 sites, but only 53 deliver LAI, and it draws on
permanently instrumented sites rather than field campaigns.

{% endcapture %}

{% capture col2 %}

### The measurements already exist

Research groups across the world hold multi-season LAI field campaigns that at present
cannot be combined &mdash; different protocols, instruments, sampling geometries and
phenological conventions, and no shared metadata standard.

LAI4EO harmonises them. The atomic record is the **elementary sampling unit (ESU)**:
standardised geolocation and acquisition time, crop and phenology, LAI value and its
dispersion, and the instrument and protocol used.

ESU footprints in the current release run from {{ s.esu_area_min }} to
{{ s.esu_area_max }}&nbsp;m&sup2; &mdash; a scale that matches decametric pixels.

{% endcapture %}

{% include cols.html col1=col1 col2=col2 %}

{% include section.html %}

## What is in the database

{% capture text %}

{{ s.measurements }} harmonised ESU-level measurements across {{ s.sampling_units }}
sampling units and {{ s.field_plots }} field plots, recorded between {{ s.year_min }} and
{{ s.year_max }}. LAI values range from {{ s.lai_min }} to {{ s.lai_max }}.

**Crops.** {{ s.crop_list | join: ", " }}.

**Instruments.** {{ s.instrument_list | join: ", " }}.

**Metadata depth.** BBCH phenology on {{ s.bbch_records }} records, per-ESU standard
deviation on {{ s.std_records }}, and RTK positions accurate to 0.03&nbsp;m on
{{ s.rtk_records }}.

{%
  include button.html
  link="https://doi.org/10.5281/zenodo.21246927"
  text="Starter Dataset v1.0 on Zenodo"
  icon="fa-solid fa-arrow-right"
  flip=true
  style="bare"
%}

{% endcapture %}

{% include feature.html image="images/photo.jpg" title="Starter Dataset v1.0" text=text %}

{% include section.html %}

## Contributing

You keep your data. We do the harmonising.

{% capture col1 %}

### What you get

- **You keep ownership.** No transfer of ownership, intellectual property, or control.
- **Named as a Consortium member** in the Data Paper and every subsequent release.
- **Early access** to the full harmonised database, before the Data Paper is published.
- **Harmonisation done for you**, with your own quality flags preserved and a link back
  to your original record.

{% endcapture %}

{% capture col2 %}

### What we ask

1. **Deposit on Zenodo** under CC BY 4.0 or CC BY-NC 4.0.
2. **Contact the Core Team** to start the review.
3. **Be reachable by email** to help us interpret your data correctly. This is the main
   commitment.
4. Check your institutional, funder, and national requirements before sharing.

Nothing here is legally binding, and participation costs nothing. You may withdraw at any
time by email.

{% endcapture %}

{% include cols.html col1=col1 col2=col2 %}

{% capture embargo %}
**On the embargo.** Until the Consortium's first Data Paper is published, contributors
agree not to publish analyses that *combine* data from two or more contributors.
**Analyses of your own data alone are unrestricted, at any time.**
{% endcapture %}

{% include alert.html type="info" content=embargo %}

<div class="hero-buttons">
  {%
    include button.html
    link="contribute"
    text="How to contribute"
    icon="fa-solid fa-arrow-right"
    flip=true
  %}
  {%
    include button.html
    link="https://zenodo.org/communities/lai4eo"
    text="Zenodo community"
    icon="fa-solid fa-up-right-from-square"
    style="bare"
  %}
</div>

{% include section.html %}

## Who we are

LAI4EO was established by **NASA Harvest** and **CNR-IREA**. It runs without funding or
administrative structure, and is open to any group willing to share data.

{% capture institutions %}

{% include card.html title="ICube Laboratory" subtitle="University of Strasbourg, France" image="images/photo.jpg" %}
{% include card.html title="CNR-IREA" subtitle="National Research Council, Milan, Italy" image="images/photo.jpg" %}
{% include card.html title="University of Maryland" subtitle="Geographical Sciences, College Park, USA" image="images/photo.jpg" %}
{% include card.html title="Monash University" subtitle="Earth, Atmosphere and Environment, Australia" image="images/photo.jpg" %}
{% include card.html title="SatFarming" subtitle="France" image="images/photo.jpg" %}

{% endcapture %}

{% include grid.html content=institutions %}

{%
  include button.html
  link="team"
  text="Meet the Core Team"
  icon="fa-solid fa-arrow-right"
  flip=true
  style="bare"
%}
