window.addEventListener("DOMContentLoaded", function() {
  // Find the base URL from the current page
  var basePath = window.location.pathname;
  // Match version in path like /en/latest/, /en/dev/, /en/0.4.1/, or /latest/, /dev/
  var versionMatch = basePath.match(/(?:\/en)?\/([^\/]+)\//);
  var CURRENT_VERSION = versionMatch ? versionMatch[1] : 'latest';
  
  // For local development, we may not have a version in the path
  if (CURRENT_VERSION === '' || CURRENT_VERSION === 'index.html' || CURRENT_VERSION === 'en') {
    CURRENT_VERSION = 'latest';
  }

  // Determine if we're in a versioned deployment (production) or local single build
  var isVersionedPath = versionMatch !== null;
  var baseUrl = isVersionedPath ? basePath.substring(0, basePath.indexOf(CURRENT_VERSION)) : '/';
  
  // For local development without versioned paths, link to root
  if (!isVersionedPath) {
    baseUrl = '/';
  }

  // In local development (no versioned paths), all version links should point to root
  // since we only have a single build. In production (mike), versioned paths exist.
  var isLocalDev = !isVersionedPath;

  function makeDropdown(versions, selected) {
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
      // In local dev, all versions point to root since we only have one build
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
    
    // Toggle dropdown on button click
    button.addEventListener("click", function(e) {
      e.stopPropagation();
      var isOpen = dropdown.style.display === "block";
      dropdown.style.display = isOpen ? "none" : "block";
      button.setAttribute("aria-expanded", !isOpen);
    });
    
    // Close dropdown when clicking outside
    document.addEventListener("click", function(e) {
      if (!container.contains(e.target)) {
        dropdown.style.display = "none";
        button.setAttribute("aria-expanded", "false");
      }
    });
    
    // Handle keyboard navigation
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

  // Fetch versions.json
  fetch("/versions.json")
    .then(function(response) {
      if (!response.ok) throw new Error("Failed to load versions.json");
      return response.json();
    })
    .then(function(versions) {
      // Filter out hidden versions if present
      var visibleVersions = versions.filter(function(v) {
        return !v.properties || !v.properties.hidden;
      });
      
      // Find the real version - prioritize exact version match over alias
      var realVersionObj = versions.find(function(v) {
        return v.version === CURRENT_VERSION;
      });
      // If no exact match, check aliases
      if (!realVersionObj) {
        realVersionObj = versions.find(function(v) {
          return v.aliases && v.aliases.includes(CURRENT_VERSION);
        });
      }
      var realVersion = realVersionObj ? realVersionObj.version : CURRENT_VERSION;
      
      var dropdown = makeDropdown(visibleVersions, realVersion);
      
      // Insert at bottom-right of page (fixed position)
      document.body.appendChild(dropdown);
    })
    .catch(function(err) {
      console.warn("Version dropdown: Could not load versions.json", err);
    });
});