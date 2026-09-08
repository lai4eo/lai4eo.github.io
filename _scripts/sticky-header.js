// Collapse the masthead once the page is scrolled.
//
// Uses a sentinel + IntersectionObserver rather than reading window.scrollY,
// because reading scrollY creates a feedback loop:
//
//   scrollY passes 48  ->  header collapses (84px -> 47px)
//   ->  document is 37px shorter, so Chrome's scroll anchoring reduces scrollY
//       by 37 to keep the visible content still
//   ->  scrollY is now back under 48  ->  header expands
//   ->  document grows 37px, anchoring pushes scrollY back up
//   ->  repeat, several times a second: the header jitters between sizes
//
// The sentinel is a 1px, out-of-flow marker pinned 48px down the *document*.
// Its position does not depend on the header's height, so collapsing the header
// cannot move it - the trigger has no path back to itself and the loop is gone.

(function () {
  var OFFSET = 48; // px down the page at which the header collapses

  function setup() {
    var header = document.querySelector(".masthead");
    if (!header) return;

    var sentinel = document.createElement("div");
    sentinel.className = "masthead-sentinel";
    sentinel.setAttribute("aria-hidden", "true");
    document.body.insertBefore(sentinel, document.body.firstChild);

    if (!("IntersectionObserver" in window)) {
      fallback(header);
      return;
    }

    new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          header.removeAttribute("data-minified");
        } else {
          header.setAttribute("data-minified", "");
        }
      });
    }).observe(sentinel);
  }

  // Only for browsers without IntersectionObserver. Hysteresis - a wide gap
  // between the collapse and expand thresholds - is what keeps the scrollY
  // feedback described above from oscillating: the 37px correction can never
  // carry the page across both thresholds.
  function fallback(header) {
    var COLLAPSE_AT = 96;
    var EXPAND_AT = 24;
    var ticking = false;

    function update() {
      ticking = false;
      var y = window.scrollY;
      if (y > COLLAPSE_AT) {
        header.setAttribute("data-minified", "");
      } else if (y < EXPAND_AT) {
        header.removeAttribute("data-minified");
      }
    }

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

    update();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", setup);
  } else {
    setup();
  }
})();
