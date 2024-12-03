// search.js

const searchInput = document.getElementById('searchInput');
const searchDropdown = document.querySelector('.search-bar-suggestions');

// Search bar focus event
searchInput.addEventListener('focus', function() {
  searchDropdown.style.display = 'block';
});

// Search bar input event
searchInput.addEventListener('input', function() {
  if (searchInput.value) {
    searchDropdown.style.display = 'block';
  } else {
    searchDropdown.style.display = 'none';
  }
});

// Close search dropdown if clicking outside
document.addEventListener('click', function(event) {
  if (!searchInput.contains(event.target) && !searchDropdown.contains(event.target)) {
    searchDropdown.style.display = 'none';
  }
});

// Prevent dropdown closing when clicking inside the dropdown
searchDropdown.addEventListener('click', function(event) {
  event.stopPropagation();
});
