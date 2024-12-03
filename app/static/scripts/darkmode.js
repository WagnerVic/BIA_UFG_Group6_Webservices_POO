document.addEventListener('DOMContentLoaded', () => {
    const body = document.querySelector('body');
    const toggleButton = document.querySelector('.toggle-darkmode');
  
    // Check if dark mode was previously enabled
    if (localStorage.getItem('darkMode') === 'enabled') {
        body.classList.add('dark-mode');
    }
  
    // Event listener for the toggle button
    toggleButton.addEventListener('click', () => {
        body.classList.toggle('dark-mode');
      
        // Save dark mode state to localStorage
        if (body.classList.contains('dark-mode')) {
            localStorage.setItem('darkMode', 'enabled');
        } else {
            localStorage.removeItem('darkMode');
        }
      
        // Log the current state of dark mode
        if (body.classList.contains('dark-mode')) {
            console.log('Dark mode enabled.');
        } else {
            console.log('Dark mode disabled.');
        }
    });
});
