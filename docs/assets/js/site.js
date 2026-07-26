/**
 * CardScanR legal site — local UI helpers only.
 * No analytics, cookies, trackers, or third-party requests.
 */
(function () {
  "use strict";

  document.documentElement.classList.add("js");

  // Mark current nav item from path for keyboard/screen-reader clarity.
  var path = window.location.pathname.replace(/\/+$/, "/") || "/";
  var links = document.querySelectorAll(".nav a[href], .footer-nav a[href]");
  links.forEach(function (link) {
    try {
      var href = link.getAttribute("href");
      if (!href || href.charAt(0) === "#") return;
      var url = new URL(href, window.location.href);
      var linkPath = url.pathname.replace(/\/+$/, "/") || "/";
      if (linkPath === path) {
        link.setAttribute("aria-current", "page");
      }
    } catch (e) {
      /* ignore malformed relative paths during local file opens */
    }
  });
})();
