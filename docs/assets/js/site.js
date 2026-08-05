/**
 * CardScanR legal site — local UI helpers only.
 * No analytics, cookies, trackers, or third-party requests (except feedback page).
 */
(function () {
  "use strict";

  document.documentElement.classList.add("js");

  var yearEls = document.querySelectorAll("[data-year]");
  if (yearEls.length) {
    var year = String(new Date().getFullYear());
    yearEls.forEach(function (el) {
      el.textContent = year;
    });
  }

  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("nav--open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    });
  }

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
