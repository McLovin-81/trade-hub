// Utility function to toggle dark mode
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    // Optionally, you can store the user's preference in localStorage
    var isDarkMode = document.body.classList.contains('dark-mode');
    localStorage.setItem('dark-mode', isDarkMode.toString());
}
// Function to initialize dark mode based on user preference
function initDarkMode() {
    var savedDarkMode = localStorage.getItem('dark-mode') === 'true';
    if (savedDarkMode) {
        document.body.classList.add('dark-mode');
    }
}
/*   // Function to handle dropdown toggle
  function handleDropdownClick(event: MouseEvent): void {
    const target = event.target as HTMLElement;
    const dropdownMenu = target.nextElementSibling as HTMLElement;
  
    // Toggle 'aria-expanded' attribute
    const isExpanded = target.getAttribute('aria-expanded') === 'true';
    target.setAttribute('aria-expanded', (!isExpanded).toString());
  
    // Toggle dropdown menu visibility
    dropdownMenu.style.display = isExpanded ? 'none' : 'block';
  }
  
  // Function to initialize dropdowns
  function initDropdowns(): void {
    const dropdownLinks = document.querySelectorAll('.dropdown-link');
    dropdownLinks.forEach(link => {
      link.addEventListener('click', handleDropdownClick);
    });
  } */
// Function to handle login button click
function handleLoginClick() {
    alert('Login button clicked! Implement your login logic here.');
}
// Function to initialize the page
function init() {
    // Initialize dark mode based on user preference
    initDarkMode();
    // Attach event listener to dark mode toggle
    var darkModeToggle = document.querySelector('.dark-mode-toggle');
    darkModeToggle === null || darkModeToggle === void 0 ? void 0 : darkModeToggle.addEventListener('click', toggleDarkMode);
    // Initialize dropdowns
    // initDropdowns();
    // Attach event listener to login button
    var loginButton = document.querySelector('.btn');
    loginButton === null || loginButton === void 0 ? void 0 : loginButton.addEventListener('click', handleLoginClick);
}
// Run the initialization function after DOM content is loaded
document.addEventListener('DOMContentLoaded', init);
// RUN -> tsc index.ts
