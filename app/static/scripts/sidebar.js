// sidebar.js

// Get references to the sidebar and toggle button
const sidebar = document.querySelector('.sidebar');
const toggleButton = document.querySelector('.toggle-sidebar');
const siteTitle = document.querySelector('.site-title');

// Add event listener to the toggle button
toggleButton.addEventListener('click', () => {
  // Toggle the 'visible' class to show/hide the sidebar
  sidebar.classList.toggle('visible');
  
  // Toggle the button's movement class
  toggleButton.classList.toggle('shift-right-when-menu-visible');

  siteTitle.classList.toggle('shift-right-when-menu-visible');
});
