---
layout: default
---

{% assign s = site.data.stats %}

{% include section.html size="full" %}

<div class="page-hero" style="background-image: url('{{ "images/background.jpg" | relative_url }}')">
  <div class="page-hero-inner">
    <!-- non-breaking hyphen: keeps "leaf-area" on one line, so the title
     wraps after "crop" instead of splitting the compound -->
    <h1>Harmonising global crop leaf&#8209;area measurements</h1>
    <p>
      LAI4EO is an open consortium harmonising in-situ <strong>Leaf Area Index</strong>
      measurements over cropland into a <strong>free reference database</strong> for
      validating Sentinel-2-era satellite products. Contributors keep ownership of their
      data. The reference collections behind satellite LAI validation were built for
      kilometre pixels; this one is built for ten-metre ones.
    </p>
  </div>
</div>

{% include section.html size="page" %}

<div class="home-tight"></div>

{% include stats.html %}

<div class="hero-buttons">
  {%
    include button.html
    link="#join"
    text="Contribute your measurements"
    icon="fa-solid fa-hand-holding-heart"
    tooltip="How to add your dataset to the database"
  %}
  {%
    include button.html
    link="#database"
    text="Explore the data"
    icon="fa-solid fa-database"
    tooltip="What the database holds and how to get it"
    style="bare"
  %}
</div>

{% include section.html size="wide" %}

<div class="home-tight"></div>

## Where the measurements come from

Every bubble is a count of measurements, coloured by the crop most of them are from.
Nearby sites group together, and split apart as you zoom in. Filter by crop or instrument
to see what the database holds.

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

{% capture why %}

### Built for kilometre pixels

The reference collections behind satellite LAI validation were assembled for
**kilometre-scale sensors**, and they still reflect that design.

[**DIRECT V2.1**](https://calvalportal.ceos.org/web/guest/lpv-direct-v2.1), which underlies most product intercomparison, holds 280 LAI values from
176 sites, averaged over 3&nbsp;km&nbsp;&times;&nbsp;3&nbsp;km so that the footprint
comfortably exceeds the pixel being validated. Cropland supplies four-fifths of those
values, but 161 come from China, and only **two were collected after 2017**, the year
Sentinel-2 reached its two-satellite configuration.

Copernicus [**GBOV**](https://gbov.land.copernicus.eu/) spans over 150 sites, but only 53 deliver LAI, and it draws on
permanently instrumented sites rather than field campaigns.

Sentinel-2 and HLS observe cropland at 10 to 30&nbsp;m, where a field-scale measurement
corresponds to roughly one pixel rather than one part of a large average. At that scale,
**no comparable reference collection exists** for cropland.

### The measurements already exist

Research groups across the world hold multi-season LAI field campaigns that at present
cannot be combined: different protocols, instruments, sampling geometries and
phenological conventions, and no shared metadata standard.

LAI4EO harmonises them. The atomic record is the **elementary sampling unit (ESU)**,
carrying standardised geolocation and acquisition time, crop and phenology, LAI value and its
dispersion, and the instrument, measurement type and protocol used to obtain it.

ESU footprints in the current release run from {{ s.esu_area_min }} to
{{ s.esu_area_max }}&nbsp;m&sup2;, a scale that matches decametric pixels.

{% endcapture %}

{% include flow-cols.html content=why %}

{% include section.html %}

## Explore the database {#database}

The harmonised database holds {{ s.measurements }} ESU-level measurements across
{{ s.sampling_units }} sampling units and {{ s.field_plots }} field plots, gathered at
{{ s.sites }} sites in {{ s.countries }} countries between {{ s.year_min }} and
{{ s.year_max }} by {{ s.contributors }} contributing groups.

{% capture col1 %}

### What it holds

**Crops.** {{ s.crop_list | join: ", " }}.

**Instruments.** {{ s.instrument_list | join: ", " }}.

**Metadata depth.** BBCH phenology on {{ s.bbch_records }} records, per-ESU standard
deviation on {{ s.std_records }}, and RTK positions accurate to 0.03&nbsp;m on
{{ s.rtk_records }}.

Every harmonised record keeps a link back to the contributor's original entry, and
carries the contributor's own quality flags.

{% endcapture %}

{% capture col2 %}

### How to get it

**Starter Dataset v1.0** is the public slice: a subset of the harmonised database,
deposited on Zenodo under CC BY 4.0. Free to anyone, no registration, citable by DOI.

**The full database** is open to Consortium members, who get it through the Harvest
Portal ahead of the Data Paper. Contributing measurements is what makes you a member
&mdash; see [Join the Consortium](#join) below.

Contributors' own deposits live in the
[LAI4EO Zenodo community](https://zenodo.org/communities/lai4eo), where each dataset
stays under its authors' names.

{% endcapture %}

{% include cols.html col1=col1 col2=col2 %}

<div class="hero-buttons">
  {%
    include button.html
    link="https://doi.org/10.5281/zenodo.21246927"
    text="Starter Dataset v1.0 on Zenodo"
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

## Join the Consortium {#join}

You keep your data. We do the harmonising.

Membership is free. There is no funding, no administrative structure and nothing legally
binding &mdash; the terms are set out in the
[LAI4EO Collaboration Agreement](https://drive.google.com/file/d/1-e-KTbwJrrcchIktZkSxD6IvpJf48EwF/view), and you may withdraw at any time by email.

New to LAI4EO? The
[Letter of Invitation](https://drive.google.com/file/d/1Bk0W11YTykSF11Pzo3vyOdw_VJ1Akv9i/view)
is the one-page version of what follows &mdash; the document to forward to a
colleague, a data manager, or a head of department.

{% capture col1 %}

### What you get

- **You keep ownership.** No transfer of ownership, intellectual property, or control.
- **Named as a Consortium member** on this site, in the Data Paper, and in every
  subsequent release.
- **Early access** to the full harmonised database, before the Data Paper is published.
- **Harmonisation done for you**, with your own quality flags preserved and a link back
  to your original record.
- **Co-authorship** case by case for substantial datasets, and for anyone who helps
  compile, curate, analyse or write.

{% endcapture %}

{% capture col2 %}

### What we ask

- **Be reachable by email** so we can interpret your data correctly. This is the main
  commitment.
- **Deposit on Zenodo** under CC BY 4.0 or CC BY-NC 4.0.
- **Check your institutional, funder and national requirements** before sharing.
- **Observe the embargo** below, and keep Harvest Portal access inside the Consortium.

{% endcapture %}

{% include cols.html col1=col1 col2=col2 %}

### How to join

1. **Tell us what you hold.** The form below asks for a short description &mdash; crops,
   instruments, roughly how many campaigns. A single season counts.
2. **Deposit your dataset on Zenodo** under CC BY 4.0 or CC BY-NC 4.0, and submit it to
   the LAI4EO community. It stays yours, under your names.
3. **We harmonise it** to the ESU schema and send it back to you. Nothing scientifically
   meaningful changes without your agreement.
4. **You are a member.** Your group is listed on the Team page and you get access to the
   full database.

{% capture embargo %}
**On the embargo.** Until the Consortium's first Data Paper is published, contributors
agree not to publish analyses that *combine* data from two or more contributors.
**Analyses of your own data alone are unrestricted, at any time.**
{% endcapture %}

{% include alert.html type="info" content=embargo %}

<div class="hero-buttons">
  {%
    include button.html
    link="https://forms.gle/HgwCA3h278ANHPjz8"
    text="Open the contribution form"
    icon="fa-solid fa-pen-to-square"
    tooltip="A short Google Form - step 1 above"
  %}
  {%
    include button.html
    link="mailto:lai4eo@umd.edu"
    text="Email the Core Team"
    icon="fa-solid fa-envelope"
    style="bare"
  %}
</div>

{% include section.html %}

## Who we are

LAI4EO was established by **NASA Harvest** and **CNR-IREA**. It runs without funding or
administrative structure, and is open to any group willing to share data.

The institutions below host the Core Team, who maintain the harmonised database. They are
not the list of contributing groups &mdash; any group that shares a dataset becomes a
Consortium member, and that list grows with every release.

{% include institutions.html %}

{%
  include button.html
  link="team"
  text="Meet the Core Team"
  icon="fa-solid fa-arrow-right"
  flip=true
  style="bare"
%}
