# Maintaining this site

Runbooks for the person who keeps <https://lai4eo.github.io> up to date. If you
are looking to **contribute LAI measurements**, that is the
[contribution form](https://forms.gle/HgwCA3h278ANHPjz8), not this file.

| I want to… | Go to |
|---|---|
| See my changes before pushing | [Preview locally](#preview-locally) |
| Update the map and the counters after a new data release | [1. New data release](#1-new-data-release) |
| Add a group whose data just arrived | [2. Register a contributing group](#2-register-a-contributing-group) |
| Add or remove a paper on the Research page | [3. Citations](#3-citations) |
| Point the site at a new Zenodo release | [4. New dataset release](#4-new-dataset-release) |
| Add someone to the Team page | [5. Team members](#5-team-members) |
| Write a blog post | [6. Blog posts](#6-blog-posts) |
| Change the nav, or the institution list | [7. Small edits](#7-small-edits) |
| Understand what happens when I push | [Deploying](#deploying) |

Two rules hold across all of it:

- **Numbers are generated, never typed.** Counters, the map and the site list
  come from `tools/build_site_data.py`. A digit typed into `index.md` goes stale
  the moment the database changes.
- **Push to `main` deploys.** There is no staging site. Preview locally first.

---

## Preview locally

Two ways. Both serve <http://localhost:4000> with live reload.

### Option A — native Ruby (fast, recommended for editing)

One-time setup:

```bash
brew install ruby@3.1                       # match CI
echo 'export PATH="/opt/homebrew/opt/ruby@3.1/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc
ruby -v                                     # must print 3.1.x, not 2.6
gem install bundler -v 2.5.6
bundle config set --local path vendor/bundle
bundle install
```

If `bundle install` dies compiling **`posix-spawn 0.3.15`**, it is not your
setup — current clang treats `incompatible function pointer types` as an error.
Install that one gem with the flag, then re-run `bundle install`:

```bash
gem install posix-spawn -v 0.3.15 -- --with-cflags="-Wno-incompatible-function-pointer-types"
```

Every time after that:

```bash
export PATH="/opt/homebrew/opt/ruby@3.1/bin:$PATH"
bundle exec jekyll serve --livereload --open-url
```

Jekyll never hot-reloads `_config.yaml`. Restart the server after editing it.

### Option B — Docker (matches CI byte for byte)

```bash
open -a Docker                    # wait for the whale to stop animating
docker info > /dev/null && echo up
bash .docker/run.sh               # first run builds the image, 5-10 min
```

`Ctrl+C` stops it; the container is `--rm`. This path also restarts Jekyll when
`_config.yaml` changes, which Option A will not do.

> **⚠️ Docker rewrites your citations.** `.docker/entrypoint.sh` runs
> `_cite/cite.py` on startup and again whenever `_data/sources*.yaml` changes,
> overwriting the tracked `_data/citations.yaml`.
>
> If the container cannot reach the DOI resolvers, `cite.py` still writes the
> file — with every title, author, publisher and date stripped. **The CI check
> will not catch this**: it compares DOI ids, which are unchanged.
>
> So after any Docker session:
>
> ```bash
> git diff _data/citations.yaml     # expect no output
> git checkout _data/citations.yaml # if it changed and you did not mean it
> ```

---

## 1. New data release

Run this after every harmonised release. It rewrites the counters, the map, the
site list and the contributor list — the only supported way to change any number
on the site.

```bash
"<path-to-parent-venv>/bin/python" tools/build_site_data.py \
  "<path-to>/private_lai4eo_dataset_YYYY-MM-DD.csv"

git diff _data/ assets/data/      # every published number, on one screen
```

Notes:

- **It needs the parent venv, not `_cite/.venv`.** Country and site names come
  from the Natural Earth shapefiles found beside the CSV, so the interpreter
  needs `geopandas`.
- **The private CSV is the correct input.** The script publishes aggregates
  only. Generating from the public Starter Dataset would describe the slice
  rather than the database.
- **It writes nothing at all if any check fails.** A partial run is not a
  failure mode you have to think about.
- If it stops on an unmapped `source_id`, go to
  [2. Register a contributing group](#2-register-a-contributing-group). Do not
  work around it — the fallback it is refusing would print a contributor's name
  and a folder date onto the homepage.

Review `git diff`, then commit and push.

## 2. Register a contributing group

`tools/build_site_data.py` refuses to run when it meets a `source_id` it has no
name for. Add the mapping near the top of the script:

```python
CONTRIBUTORS = {
    ...
    "<source_id as it appears in the CSV>": "Institution name as it should be published",
}
```

Then re-run step 1. The name you write is what appears in `contributor_list` in
`_data/stats.yaml`, so use the form the group itself would want.

While you are there, `SITE_NAMES` in the same file overrides the site label for
a region. The default is `"<admin-1 region>, <country>"`, derived from Natural
Earth — correct and dull. Add an override only once the contributor has
confirmed what they call the site.

## 3. Citations

`_data/sources.yaml` is the source of truth for the Research page. Add a DOI and
it appears; delete one and it goes.

```bash
$EDITOR _data/sources.yaml     # the only file you edit by hand
./tools/citations.sh           # regenerates _data/citations.yaml
git diff _data/                # review, then commit BOTH files
```

- The first run of `citations.sh` builds `_cite/.venv` and takes a couple of
  minutes. Later runs are seconds.
- **Do not hand-edit `_data/citations.yaml`.** It is generated, and it says so
  at the top of itself.
- CI runs `tools/check_citations.py` and **fails the build** if the two files
  disagree, so a forgotten regen is loud rather than a silently stale page.
  `citations.sh` runs the same check for you at the end.
- Entries in `sources.yaml` may carry extra fields (`title:`, `authors:`, …)
  which override whatever Manubot fetches. That is why the Zenodo dataset entry
  lists its authors explicitly.

## 4. New dataset release

When a new Starter Dataset version is deposited, the DOI has to change in
**two** places. There is no generator for this.

1. `_data/sources.yaml` — the `- id: doi:…` entry and its `link:`, so the
   Research page cites the new version. Then run `./tools/citations.sh`.
2. `index.md` — the **Starter Dataset** button in the `## Explore the database`
   section, whose `link=` is the DOI URL.

Check both before pushing:

```bash
grep -rn "zenodo" index.md _data/sources.yaml
```

The Zenodo *community* link (`zenodo.org/communities/lai4eo`) is version-independent
and does not change.

## 5. Team members

The Team page renders `_members/*.md`, one file per person, sorted by `order:`.

```markdown
---
name: Ada Lovelace
order: 90
image: images/ada.jpg
role: researcher
affiliation: Institution, Country
links:
  home-page: "https://…"
  orcid: "0000-0000-0000-0000"
---

One or two sentences, in the third person.
```

- **`order:` is deliberate, not alphabetical.** Use gaps of 10 so a later
  insertion does not renumber everyone.
- `image:` is a path under `images/`. Put the file there first.
- The page is **Core Team only** — the signatories to the Collaboration
  Agreement.

### Consortium members are not added by hand

This is the part that catches people. Contributing groups are **generated**:
step 1 writes them into `contributor_list` in `_data/stats.yaml` from the
release itself. Adding a group means
[registering it in the generator](#2-register-a-contributing-group) and
re-running, not writing a file.

**Nothing on the site renders `contributor_list` today.** The plan is portrait
cards below the Core Team's, and it is waiting on there being enough groups to
fill a row. Until that section is built, a new group appears in the data and on
the map, but not as a named entry on the Team page.

## 6. Blog posts

One file per post in `_posts/`, named `YYYY-MM-DD-slug.md`:

```markdown
---
title: A short, specific headline
author: nikhil-sasi-rajan
tags: LAI4EO, data release
---

The first paragraph is the excerpt shown on the Blog index. Make it stand alone.

The rest of the post.
```

- **`author:` is the filename stem of a file in `_members/`** (its slug), not a
  display name. A slug that matches renders that person's portrait, name and
  affiliation; one that does not is printed verbatim, so `author: Sheila Baber`
  shows the literal text "sheila baber" next to a quill icon. Several authors
  can be given comma-separated.
- The date in the filename is the publication date and drives ordering.
- **A post dated in the future is silently not built.** Jekyll excludes them by
  default. If a new post does not appear, check the date first.

## 7. Small edits

| File | Holds | Watch for |
|---|---|---|
| `_data/nav.yaml` | the top navigation, in render order | `link:` is site-root-relative (`/team/`, `/#join`), never bare, never with the domain |
| `_data/institutions.yaml` | the "Who we are" list on the homepage | hand-typed, the Core Team's **host institutions**. Not the contributing groups — do not wire it to `contributor_list` |
| `_config.yaml` | site title, subtitle, description, `exclude:` | Jekyll does not hot-reload it; restart the server |

Each of those files carries a header comment explaining its own rules. Read it
before editing.

---

## Deploying

Push to `main`. That is the whole deploy.

`.github/workflows/on-push.yaml` runs `build-site.yaml`, which checks that the
citations are in sync, builds the site, and commits the result to the
`gh-pages` branch that GitHub Pages serves. Watch it in the repository's
**Actions** tab.

There is no staging environment, so the local preview is the only place to catch
a mistake before it is live. A failed build leaves the previous version up.
