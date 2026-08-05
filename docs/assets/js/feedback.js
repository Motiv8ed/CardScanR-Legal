/**
 * CardScanR website feedback form — submits to Supabase Edge Function.
 * Never logs tokens, emails, or full payloads.
 */
(function () {
  "use strict";

  var config = window.CARDSCANR_FEEDBACK_CONFIG;
  var form = document.getElementById("feedback-form");
  if (!form || !config || !config.submitUrl) return;

  var LIMITS = {
    subject: 120,
    description: 4000,
    reproduction_steps: 2000
  };

  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  var successEl = document.getElementById("form-success");
  var failureEl = document.getElementById("form-failure");
  var errorSummary = document.getElementById("error-summary");
  var errorList = document.getElementById("error-list");
  var submitBtn = document.getElementById("feedback-submit");
  var turnstileWidget = document.getElementById("turnstile-widget");
  var turnstileWidgetId = null;

  function $(id) {
    return document.getElementById(id);
  }

  function hide(el) {
    if (el) el.hidden = true;
  }

  function show(el) {
    if (el) el.hidden = false;
  }

  function trim(val) {
    return (val || "").trim();
  }

  function setFieldError(fieldId, message) {
    var field = $(fieldId);
    var err = document.querySelector('[data-error-for="' + fieldId + '"]');
    if (field) field.setAttribute("aria-invalid", message ? "true" : "false");
    if (err) {
      if (message) {
        err.textContent = message;
        err.hidden = false;
      } else {
        err.textContent = "";
        err.hidden = true;
      }
    }
  }

  function clearErrors() {
    hide(errorSummary);
    if (errorList) errorList.innerHTML = "";
    form.querySelectorAll("[aria-invalid]").forEach(function (el) {
      el.setAttribute("aria-invalid", "false");
    });
    form.querySelectorAll(".field-error").forEach(function (el) {
      el.hidden = true;
      el.textContent = "";
    });
    hide(successEl);
    hide(failureEl);
  }

  function updateCounter(inputId, counterId, max) {
    var input = $(inputId);
    var counter = $(counterId);
    if (!input || !counter) return;
    var len = input.value.length;
    counter.textContent = len + " / " + max;
    counter.classList.toggle("is-over", len > max);
  }

  function bindCounter(inputId, counterId, max) {
    var input = $(inputId);
    if (!input) return;
    var update = function () {
      updateCounter(inputId, counterId, max);
    };
    input.addEventListener("input", update);
    update();
  }

  bindCounter("subject", "subject-count", LIMITS.subject);
  bindCounter("description", "description-count", LIMITS.description);
  bindCounter("reproduction_steps", "reproduction-count", LIMITS.reproduction_steps);

  function getTurnstileToken() {
    if (!window.turnstile) return "";
    try {
      if (turnstileWidgetId !== null) {
        return window.turnstile.getResponse(turnstileWidgetId) || "";
      }
      return window.turnstile.getResponse() || "";
    } catch (e) {
      return "";
    }
  }

  function resetTurnstile() {
    if (!window.turnstile) return;
    try {
      if (turnstileWidgetId !== null) {
        window.turnstile.reset(turnstileWidgetId);
      } else {
        window.turnstile.reset();
      }
    } catch (e) {
      /* ignore */
    }
  }

  function validate() {
    var errors = [];

    setFieldError("feedback_type", "");
    setFieldError("subject", "");
    setFieldError("description", "");
    setFieldError("contact_email", "");
    setFieldError("reproduction_steps", "");

    var feedbackType = trim($("feedback_type") && $("feedback_type").value);
    if (!feedbackType) {
      setFieldError("feedback_type", "Select a feedback type.");
      errors.push("Select a feedback type.");
    }

    var subject = trim($("subject") && $("subject").value);
    if (!subject) {
      setFieldError("subject", "Enter a subject.");
      errors.push("Enter a subject.");
    } else if (subject.length < 4) {
      setFieldError("subject", "Subject must be at least 4 characters.");
      errors.push("Subject is too short.");
    } else if (subject.length > LIMITS.subject) {
      setFieldError("subject", "Subject must be " + LIMITS.subject + " characters or fewer.");
      errors.push("Subject is too long.");
    }

    var description = trim($("description") && $("description").value);
    if (!description) {
      setFieldError("description", "Enter a description.");
      errors.push("Enter a description.");
    } else if (description.length < 10) {
      setFieldError("description", "Description must be at least 10 characters.");
      errors.push("Description is too short.");
    } else if (description.length > LIMITS.description) {
      setFieldError("description", "Description must be " + LIMITS.description + " characters or fewer.");
      errors.push("Description is too long.");
    }

    var email = trim($("contact_email") && $("contact_email").value);
    if (email && !EMAIL_RE.test(email)) {
      setFieldError("contact_email", "Enter a valid email address or leave this blank.");
      errors.push("Contact email is not valid.");
    }

    var steps = trim($("reproduction_steps") && $("reproduction_steps").value);
    if (steps.length > LIMITS.reproduction_steps) {
      setFieldError("reproduction_steps", "Steps must be " + LIMITS.reproduction_steps + " characters or fewer.");
      errors.push("Steps to reproduce are too long.");
    }

    var token = getTurnstileToken();
    if (!token) {
      errors.push("Complete the security check.");
    }

    if (errors.length) {
      if (errorList) {
        errors.forEach(function (msg) {
          var li = document.createElement("li");
          li.textContent = msg;
          errorList.appendChild(li);
        });
      }
      show(errorSummary);
      errorSummary.focus();
      return null;
    }

    return {
      feedback_type: feedbackType,
      subject: subject,
      description: description,
      card_name: trim($("card_name") && $("card_name").value) || null,
      set_name: trim($("set_name") && $("set_name").value) || null,
      collector_number: trim($("collector_number") && $("collector_number").value) || null,
      app_version: trim($("app_version") && $("app_version").value) || null,
      android_version: trim($("android_version") && $("android_version").value) || null,
      device_model: trim($("device_model") && $("device_model").value) || null,
      contact_email: email || null,
      reproduction_steps: steps || null,
      turnstile_token: token,
      source: "legal_site"
    };
  }

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    clearErrors();

    var payload = validate();
    if (!payload) return;

    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.setAttribute("aria-busy", "true");
    }

    fetch(config.submitUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + config.supabaseAnonKey,
        apikey: config.supabaseAnonKey
      },
      body: JSON.stringify(payload)
    })
      .then(function (response) {
        return response.json().catch(function () {
          return {};
        }).then(function (data) {
          return { ok: response.ok, data: data };
        });
      })
      .then(function (result) {
        if (result.ok && result.data && result.data.public_reference) {
          form.hidden = true;
          var refEl = $("success-reference");
          if (refEl) refEl.textContent = result.data.public_reference;
          show(successEl);
          successEl.focus();
          return;
        }
        show(failureEl);
        failureEl.focus();
        resetTurnstile();
      })
      .catch(function () {
        show(failureEl);
        failureEl.focus();
        resetTurnstile();
      })
      .finally(function () {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.removeAttribute("aria-busy");
        }
      });
  });

  function renderTurnstile() {
    if (!window.turnstile || !turnstileWidget || !config.turnstileSiteKey) return;
    if (turnstileWidgetId !== null) return;
    try {
      turnstileWidgetId = window.turnstile.render(turnstileWidget, {
        sitekey: config.turnstileSiteKey,
        theme: "dark"
      });
    } catch (e) {
      /* widget may already be rendered */
    }
  }

  function onTurnstileReady() {
    renderTurnstile();
  }

  if (window.turnstile) {
    onTurnstileReady();
  } else {
    window.addEventListener("load", onTurnstileReady);
    // api.js may load after defer scripts; poll briefly
    var attempts = 0;
    var timer = window.setInterval(function () {
      attempts += 1;
      if (window.turnstile) {
        window.clearInterval(timer);
        onTurnstileReady();
      } else if (attempts > 40) {
        window.clearInterval(timer);
      }
    }, 250);
  }
})();
