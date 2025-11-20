// Bundled main JS: concatenation of dropdown.js (and other future JS)

// Dropdown toggle: toggles .show, updates aria-expanded/aria-hidden,
// closes on outside click or Esc key.
(function () {
  function closeDropdown(dropdownButton, dropdownContent) {
    dropdownContent.classList.remove('show');
    dropdownButton.setAttribute('aria-expanded', 'false');
    dropdownContent.setAttribute('aria-hidden', 'true');
  }

  function openDropdown(dropdownButton, dropdownContent) {
    dropdownContent.classList.add('show');
    dropdownButton.setAttribute('aria-expanded', 'true');
    dropdownContent.setAttribute('aria-hidden', 'false');
  }

  document.querySelectorAll('.dropdown').forEach(function (dropdown) {
    var btn = dropdown.querySelector('.dropdown-button');
    var content = dropdown.querySelector('.dropdown-content');

    if (!btn || !content) return;

    btn.addEventListener('click', function (ev) {
      var isOpen = content.classList.contains('show');
      if (isOpen) closeDropdown(btn, content);
      else openDropdown(btn, content);
    });

    // Close when focus moves away via keyboard Tab
    btn.addEventListener('blur', function () {
      // small timeout to allow focus to move into dropdown items
      setTimeout(function () {
        if (!dropdown.contains(document.activeElement)) {
          closeDropdown(btn, content);
        }
      }, 150);
    });
  });

  // Close when clicking outside any open dropdown
  document.addEventListener('click', function (e) {
    document.querySelectorAll('.dropdown').forEach(function (dropdown) {
      var btn = dropdown.querySelector('.dropdown-button');
      var content = dropdown.querySelector('.dropdown-content');
      if (!btn || !content) return;
      if (!dropdown.contains(e.target)) {
        closeDropdown(btn, content);
      }
    });
  });

  // Close on Escape key
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' || e.key === 'Esc') {
      document.querySelectorAll('.dropdown').forEach(function (dropdown) {
        var btn = dropdown.querySelector('.dropdown-button');
        var content = dropdown.querySelector('.dropdown-content');
        if (!btn || !content) return;
        closeDropdown(btn, content);
      });
    }
  });
})();
