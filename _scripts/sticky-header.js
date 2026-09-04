// Collapse the masthead once the page is scrolled.
//
// Mirrors what ESA WorldCereal does: past a small scroll threshold the header
// gets a `data-minified` attribute, and CSS handles the rest - dark banner,
// shrunken logos, tighter padding. The header itself is `position: sticky`, so
// unlike WorldCereal's fixed-position version no JavaScript is needed to
// compensate the page offset.

(function () {
  var THRESHOLD = 48; // px, same as WorldCereal's 3rem

  function setup() {
    var header = document.querySelector(".masthead");
    if (!header) return;

    var ticking = false;

    function update() {
      ticking = false;
      if (window.scrollY > THRESHOLD) {
        header.setAttribute("data-minified", "");
      } else {
        header.removeAttribute("data-minified");
      }
    }

    // rAF-throttled: the scroll handler must not do layout work per event
    window.addEventListener(
      "scroll",
      function () {
        if (!ticking) {
          ticking = true;
          window.requestAnimationFrame(update);
        }
      },
      { passive: true }
    );

    update(); // handle a page loaded already scrolled (anchor link, refresh)
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", setup);
  } else {
    setup();
  }
})();
