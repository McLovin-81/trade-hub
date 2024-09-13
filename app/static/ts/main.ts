
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


async function handleRegistration(event: Event): Promise<void>
{
  event.preventDefault();

  const nameInput = (document.getElementById('username') as HTMLInputElement).value;
  const emailInput = (document.getElementById('email') as HTMLInputElement).value;
  const passwordInput = (document.getElementById('password') as HTMLInputElement).value;
  const passwordConfirmInput = (document.getElementById('confirmPassword') as HTMLInputElement).value;

  if (passwordInput == passwordConfirmInput)
  {
    // The `fetch` function is asynchronous and returns a Promise
    const response = await fetch('/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: nameInput,
        email: emailInput,
        password: passwordInput
      }),
    });

    // Await the parsing of the response as JSON
    const result = await response.json();

    if (response.ok)
    {
      alert('Registration successful!');
      window.location.href = result.redirect;  // Redirect to login page
    }
    else
    {
      alert(`Error: ${result.error}`);
    }
  }
  else
  {
    alert('passwords do not match');
  }
}


async function handleLogin(event: Event): Promise<void>
{
  event.preventDefault();

  const nameInput = (document.getElementById('username') as HTMLInputElement).value;
  const passwordInput = (document.getElementById('password') as HTMLInputElement).value;

  try {
    const response = await fetch('/auth/login', {
      method: 'POST',  // Use POST for login requests
      headers: { 'Content-Type': 'application/json' },  // Correct the header
      body: JSON.stringify({
        name: nameInput,
        password: passwordInput,
      }),
    });

    // Parse the response
    const result = await response.json();

    if (response.ok) {
      alert(result.message);
      window.location.href = result.redirect;  // Redirect on success
    } else {
      alert(`Error: ${result.error}`);
    }
  } catch (error) {
    // Handle potential network errors
    console.error('Error during login:', error);
    alert('An error occurred while logging in. Please try again.');
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

  // Attach event listener to the registration form
  const registerForm = document.getElementById('registrationForm') as HTMLFormElement;
  registerForm?.addEventListener('submit', handleRegistration); // Attach registration handler to the form submission

  // Attach event listener to the registration form
  const loginForm = document.getElementById('loginForm') as HTMLFormElement;
  loginForm?.addEventListener('submit', handleLogin); // Attach registration handler to the form submission
}

// Run the initialization function after DOM content is loaded
document.addEventListener('DOMContentLoaded', init);


// RUN -> tsc --project tsconfig.json