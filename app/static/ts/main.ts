
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
    try
    {
      // The `fetch` function is asynchronous and returns a Promise
      const response = await fetch('/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(
        {
          name: nameInput,
          email: emailInput,
          password: passwordInput
        }
        ),
      });

      // Await the parsing of the response as JSON
      const result = await response.json();

      if (response.ok)
      {
        alert('Registration successful!');
        window.location.href = '/auth/login';  // Redirect to login page
      }
      else
      {
        alert('Failed to register.');
      }
    }
    catch (error)
    {
      console.error('Error:', error);
      alert('An error occurred while registering.');
    }
  }
  else
  {
    alert('passwords do not match');
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
  const form = document.getElementById('registrationForm') as HTMLFormElement;
  form?.addEventListener('submit', handleRegistration); // Attach registration handler to the form submission
}

// Run the initialization function after DOM content is loaded
document.addEventListener('DOMContentLoaded', init);


// RUN -> tsc --project tsconfig.json