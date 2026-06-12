window.addEventListener("DOMContentLoaded", function() {
  var basePath = window.location.pathname;

  // Fetch versions first, then derive the current version from
  // path segments matched against known identifiers.  This handles
  // GitHub Pages subdirectory paths like /forging-blocks/dev/
  // where the first segment is the repo name, not a version.
  fetch("versions.json")
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

      // Walk path segments from right to left looking for a match
      var pathSegments = basePath.replace(/\/$/, '').split('/');
      var CURRENT_VERSION = 'latest';
      var versionIdx = -1;

      for (var i = pathSegments.length - 1; i >= 0; i--) {
        if (knownIds.indexOf(pathSegments[i]) !== -1) {
          CURRENT_VERSION = pathSegments[i];
          versionIdx = i;
          break;
        }
      }

      // If no version found in path, we are on the root (or an unversioned page)
      var isVersionedPath = versionIdx !== -1;
      var baseUrl = isVersionedPath
        ? pathSegments.slice(0, versionIdx).join('/') + '/'
        : '/';
      var isLocalDev = !isVersionedPath;

      // Resolve the canonical version (aliases → real version)
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
      link.href = isLocalDev ? '/' : (baseUrl + v.version + "/");
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
