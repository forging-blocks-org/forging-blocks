window.addEventListener("DOMContentLoaded", function() {
  // Find our own script tag to derive the correct base directory
  // for versions.json and the versioned path prefix.  This works
  // regardless of the page URL (root, nested, or directory-style).
  var scripts = document.getElementsByTagName("script");
  var scriptUrl = null;
  for (var i = 0; i < scripts.length; i++) {
    var src = scripts[i].src;
    if (src && src.indexOf("version-dropdown.js") !== -1) {
      scriptUrl = new URL(src);
      break;
    }
  }

  // Derive the site root from our own script URL so that
  // versions.json is found regardless of subpath (GitHub Pages)
  // or versioned directory depth.  The script always lives at
  //   <siteRoot>/[<version>/]assets/js/version-dropdown.js
  // so we strip 3 segments (versioned) or 2 segments (flat).
  var versionsJsonUrl = "/versions.json";  // fallback
  if (scriptUrl) {
    var scriptDir = scriptUrl.pathname.replace(/\/[^\/]*$/, "");
    // Try 3 levels up: <site>/<version>/assets/js/ → <site>
    var siteRoot = scriptDir.replace(/\/[^\/]+\/[^\/]+\/[^\/]+$/, "");
    // If the regex didn't match (flat build has only 2 levels),
    // try 2 levels up: <site>/assets/js/ → <site>
    if (siteRoot === scriptDir) {
      siteRoot = scriptDir.replace(/\/[^\/]+\/[^\/]+$/, "");
    }
    versionsJsonUrl = siteRoot + "/versions.json";
  }

  var basePath = window.location.pathname;

  fetch(versionsJsonUrl)
    .then(function(response) {
      if (!response.ok) throw new Error("Failed to load versions.json");
      return response.json();
    })
    .then(function(versions) {
      var visibleVersions = versions.filter(function(v) {
        return !v.properties || !v.properties.hidden;
      });

      // Build a set of all known version identifiers (names + aliases)
      var knownIds = [];
      versions.forEach(function(v) {
        knownIds.push(v.version);
        if (v.aliases) {
          knownIds = knownIds.concat(v.aliases);
        }
      });

      // Find version by scanning path segments right-to-left.
      // Falls back to the script URL path when the page path
      // doesn't contain a version (e.g. the root redirect page).
      function findVersionMatch(path) {
        var segments = path.replace(/\/$/, "").split("/");
        for (var i = segments.length - 1; i >= 0; i--) {
          if (knownIds.indexOf(segments[i]) !== -1) {
            return { version: segments[i], idx: i, segments: segments };
          }
        }
        return { version: "latest", idx: -1, segments: segments };
      }

      var match = findVersionMatch(basePath);
      if (match.idx === -1 && scriptUrl) {
        match = findVersionMatch(scriptUrl.pathname);
      }

      var pathSegments = match.segments;
      var CURRENT_VERSION = match.version;
      var versionIdx = match.idx;

      var isVersionedPath = versionIdx !== -1;
      var baseUrl = isVersionedPath
        ? pathSegments.slice(0, versionIdx).join("/") + "/"
        : "/";
      var isLocalDev = !isVersionedPath;

      // Resolve canonical version (aliases → real version)
      var realVersionObj = versions.find(function(v) {
        return v.version === CURRENT_VERSION;
      });
      if (!realVersionObj) {
        realVersionObj = versions.find(function(v) {
          return v.aliases && v.aliases.indexOf(CURRENT_VERSION) !== -1;
        });
      }
      var realVersion = realVersionObj
        ? realVersionObj.version
        : CURRENT_VERSION;

      document.body.appendChild(
        makeDropdown(visibleVersions, realVersion, isLocalDev, baseUrl)
      );
    })
    .catch(function(err) {
      console.warn("Version dropdown: Could not load versions.json", err);
    });

  function makeDropdown(versions, selected, isLocalDev, baseUrl) {
    var container = document.createElement("div");
    container.className = "django-version-dropdown";
    container.id = "django-version-dropdown";

    var button = document.createElement("button");
    button.className = "django-version-dropdown__button";
    button.type = "button";
    button.setAttribute("aria-haspopup", "listbox");
    button.setAttribute("aria-expanded", "false");

    var versionText = document.createElement("span");
    versionText.className = "django-version-dropdown__text";
    versionText.textContent = "Documentation version: " + selected;

    var arrow = document.createElement("span");
    arrow.className = "django-version-dropdown__arrow";
    arrow.innerHTML = "▼";

    button.appendChild(versionText);
    button.appendChild(arrow);

    var dropdown = document.createElement("div");
    dropdown.className = "django-version-dropdown__list";
    dropdown.setAttribute("role", "listbox");
    dropdown.style.display = "none";

    versions.forEach(function(v) {
      var link = document.createElement("a");
      link.className = "django-version-dropdown__item";
      link.href = isLocalDev ? "/" : (baseUrl + v.version + "/");
      link.textContent = v.title || v.version;
      link.setAttribute("role", "option");
      if (v.version === selected) {
        link.classList.add("django-version-dropdown__item--current");
        link.setAttribute("aria-selected", "true");
      } else {
        link.setAttribute("aria-selected", "false");
      }
      dropdown.appendChild(link);
    });

    container.appendChild(button);
    container.appendChild(dropdown);

    button.addEventListener("click", function(e) {
      e.stopPropagation();
      var isOpen = dropdown.style.display === "block";
      dropdown.style.display = isOpen ? "none" : "block";
      button.setAttribute("aria-expanded", !isOpen);
    });

    document.addEventListener("click", function(e) {
      if (!container.contains(e.target)) {
        dropdown.style.display = "none";
        button.setAttribute("aria-expanded", "false");
      }
    });

    button.addEventListener("keydown", function(e) {
      if (e.key === "Escape") {
        dropdown.style.display = "none";
        button.setAttribute("aria-expanded", "false");
        button.focus();
      } else if (e.key === "ArrowDown" && dropdown.style.display === "none") {
        e.preventDefault();
        dropdown.style.display = "block";
        button.setAttribute("aria-expanded", "true");
        dropdown.querySelector("a").focus();
      }
    });

    dropdown.addEventListener("keydown", function(e) {
      if (e.key === "Escape") {
        dropdown.style.display = "none";
        button.setAttribute("aria-expanded", "false");
        button.focus();
      } else if (e.key === "ArrowUp" && e.target === dropdown.querySelector("a")) {
        e.preventDefault();
        button.focus();
      }
    });

    return container;
  }
});
