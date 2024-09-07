// Function to handle login button click
function handleLoginClick(): void
{
  alert('Login button clicked! Implement your login logic here.');
}

// Utility function to toggle dark mode
function toggleDarkMode(): void
{
  document.body.classList.toggle('dark-mode');

  // Optionally, you can store the user's preference in localStorage
  const isDarkMode = document.body.classList.contains('dark-mode');
  localStorage.setItem('dark-mode', isDarkMode.toString());
}

// Function to initialize dark mode based on user preference
function initDarkMode(): void
{
  const savedDarkMode = localStorage.getItem('dark-mode') === 'true';
  if (savedDarkMode)
  {
    document.body.classList.add('dark-mode');
  }
}

// Function to initialize the page
function init(): void
{
  // Initialize dark mode based on user preference
  initDarkMode();

  // Attach event listener to dark mode toggle
  const darkModeToggle = document.querySelector('.dark-mode-toggle');
  darkModeToggle?.addEventListener('click', toggleDarkMode); // <?> checks whether darkModeToggle is not null or undefined before attempting to call the addEventListener method on it.

  // Attach event listener to login button
  const loginButton = document.querySelector('.btn');
  loginButton?.addEventListener('click', handleLoginClick);
}

// Run the initialization function after DOM content is loaded
document.addEventListener('DOMContentLoaded', init);


// registration button
const form = document.getElementById('registrationForm') as HTMLFormElement;

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  // Get input values
  const nameInput = (document.getElementById('name') as HTMLInputElement).value;
  const emailInput = (document.getElementById('email') as HTMLInputElement).value;
  const passwordInput = (document.getElementById('password') as HTMLInputElement).value;

  // Check if all fields are filled
  if (nameInput && emailInput && passwordInput) {
    try {
      const response = await fetch('/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: nameInput,
          email: emailInput,
          password: passwordInput
        }),
      });

      if (response.ok) {
        alert('Registration successful!');
      } else {
        alert('Failed to register.');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('An error occurred while registering.');
    }
  } else {
    alert('Please fill out all fields.');
  }
});


// RUN -> tsc --project tsconfig.json
