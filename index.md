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

## Highlights

{% capture text %}

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.

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

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.

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

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.

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
