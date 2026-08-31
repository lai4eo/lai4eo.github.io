---
layout: default
---

<div class="site-hero">
  <div class="hero-inner">
    <h1>LAI4EO</h1>
    <p class="lead">A consortium collecting in-situ Leaf Area Index (LAI) measurements to support Earth Observation.</p>
    <p><a class="cta" href="research">Explore our research</a></p>
  </div>
</div>

<div class="container">

## Participating institutions

<div id="institutions-map" style="height: 420px; width: 100%; border-radius: 12px; overflow: hidden; margin: 1.5rem 0 2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.12);"></div>

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
<script>
  document.addEventListener('DOMContentLoaded', function () {
    var map = L.map('institutions-map', {
      scrollWheelZoom: false,
      zoomControl: true
    }).setView([24, 20], 2);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    var institutions = [
      {
        name: 'University of Maryland',
        coords: [38.9897, -76.9378],
        note: 'College Park, MD, USA'
      },
      {
        name: 'University of Strasbourg',
        coords: [48.5241, 7.7141],
        note: 'Illkirch-Graffenstaden, Strasbourg, France'
      },
      {
        name: 'CNR-IREA',
        coords: [45.4654, 9.1860],
        note: 'Milan, Italy'
      },
      {
        name: 'Monash University',
        coords: [-37.9105, 145.1303],
        note: 'Melbourne, Australia'
      }
    ];

    institutions.forEach(function (institution) {
      L.marker(institution.coords)
        .addTo(map)
        .bindPopup('<strong>' + institution.name + '</strong><br>' + institution.note);
    });
  });
</script>

{% include section.html %}

## Highlights

{% capture text %}

LAI4EO advances in-situ leaf area index (LAI) measurements to support crop monitoring, agricultural forecasting, and Earth observation applications worldwide.

{%
  include button.html
  link="research"
  text="See our publications"
  icon="fa-solid fa-arrow-right"
  flip=true
  style="bare"
%}

{% endcapture %}

{% include feature.html image="images/photo.jpg" link="research" title="Our Research" text=text %}

{% capture text %}

We are building a collaborative framework for data sharing, community participation, and practical pathways for contributing LAI observations and tools.

{%
  include button.html
  link="projects"
  text="Browse our projects"
  icon="fa-solid fa-arrow-right"
  flip=true
  style="bare"
%}

{% endcapture %}

{% include feature.html image="images/photo.jpg" link="projects" title="Our Projects" flip=true style="bare" text=text %}

{% capture text %}

Our consortium brings together scientists, agronomists, and data specialists working across countries and disciplines to improve monitoring of vegetation and land use.

{%
  include button.html
  link="team"
  text="Meet our team"
  icon="fa-solid fa-arrow-right"
  flip=true
  style="bare"
%}

{% endcapture %}

{% include feature.html image="images/photo.jpg" link="team" title="Our Team" text=text %}

</div>
