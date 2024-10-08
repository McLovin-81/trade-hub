/*********************
* Utility functions *
**********************/

// Utility function to toggle dark mode
function toggleDarkMode(): void
{
  document.body.classList.toggle('dark-mode');

  // Store the user's preference in localStorage
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



/**************************
* Authorization functions *
***************************/

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



/******************
* Depot functions *
*******************/

// Function to show stock symbol suggestions and allow selection
function showSuggestions(suggestions: { symbol: string, name: string }[]): void {
  const container = document.getElementById('suggestions-container');
  const symbolInput = document.getElementById('symbol') as HTMLInputElement;

  if (container) {
    container.innerHTML = ''; // Clear existing suggestions

    suggestions.forEach(suggestion => {
      const div = document.createElement('div');
      div.textContent = `${suggestion.symbol} - ${suggestion.name}`;
      
      // Add click event to select the suggestion
      div.addEventListener('click', () => {
        symbolInput.value = suggestion.symbol; // Fill input with the selected symbol
        container.innerHTML = ''; // Clear suggestions after selection
        handleStockSelection(suggestion.symbol); // Fetch and display stock price
      });

      container.appendChild(div);
    });
  }
}


// Function to handle stock symbol input
async function handleStockInput(event: Event): Promise<void> {
  const input = (event.target as HTMLInputElement).value;

  if (input.length > 1) {
    try {
      const response = await fetch(`/user/api/stocks?query=${encodeURIComponent(input)}`);
      const data = await response.json();

      if (Array.isArray(data.symbols)) {
        showSuggestions(data.symbols);
      } else {
        console.error('Unexpected response format:', data);
        showSuggestions([]);
      }
    } catch (error) {
      console.error('Error fetching stock symbols:', error);
      showSuggestions([]);
    }
  } else {
    showSuggestions([]);
  }
}


// Function to handle stock selection and fetch price from backend
async function handleStockSelection(symbol: string): Promise<void> {
  try {
    const response = await fetch(`/user/api/stock-price?symbol=${encodeURIComponent(symbol)}`);
    const stockInfo = await response.json();

    if (response.ok) {
      displayStockInfo(stockInfo); // Display stock price and name
    } else {
      console.error('Error fetching stock information:', stockInfo);
    }
  } catch (error) {
    console.error('Error fetching stock price:', error);
  }
}


// Function to display stock information
function displayStockInfo(stockInfo: { name: string, currentPrice: number }): void {
  const stockInfoDiv = document.getElementById('stockInfo') as HTMLDivElement;
  const stockNameSpan = document.getElementById('stockName') as HTMLSpanElement;
  const stockPriceSpan = document.getElementById('stockPrice') as HTMLSpanElement;

  if (stockInfoDiv && stockNameSpan && stockPriceSpan) {
    stockNameSpan.textContent = stockInfo.name;
    stockPriceSpan.textContent = stockInfo.currentPrice.toFixed(2);
    stockInfoDiv.style.display = 'block'; // Show the stock information div
  }
}


// Function to handle order submission
async function submitOrder() {
  const stockSymbol = (document.getElementById("symbol") as HTMLInputElement).value;
  const orderType = (document.getElementById("orderType") as HTMLSelectElement).value;
  const quantity = parseInt((document.getElementById("quantity") as HTMLInputElement).value);
  const responseMessage = document.getElementById("responseMessage") as HTMLParagraphElement;

  if (stockSymbol && quantity > 0 && orderType) {
      try {
          const response = await fetch(`/user/api/buy-stock`, {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify({ symbol: stockSymbol, quantity: quantity, orderType: orderType })
          });

          const data = await response.json();

          if (response.ok && data.success) {
              responseMessage.textContent = "Order placed successfully!";
              responseMessage.style.color = "green";
              // Reload the page after 1 second to show updated balance/depot data
              setTimeout(() => {
                window.location.reload();
              }, 1000);
          } else {
              responseMessage.textContent = "Failed to place the order. Insufficient balance or stock unavailable.";
              responseMessage.style.color = "red";
          }
      } catch (error) {
          console.error('Error submitting order:', error);
          responseMessage.textContent = "An error occurred. Please try again.";
          responseMessage.style.color = "red";
      }
  } else {
      responseMessage.textContent = "Please fill out all fields correctly.";
      responseMessage.style.color = "red";
  }
}



/*********************
* Settings functions *
*********************/

async function handleResetAccount(): Promise<void> {
  const confirmation = confirm("Are you sure you want to reset your account? This action cannot be undone.");

  if (confirmation) {
    try {
      const response = await fetch('/user/api/reset-account', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      });

      const result = await response.json();

      // Log the result to inspect what is being returned
      console.log('Response result:', result);

      // Check if the response is ok and contains the correct message
      if (response.ok && result.message) {
        alert(result.message); // Show the success message
        window.location.reload(); // Optionally reload the page
      } else if (result.error) {
        // Handle if there's an error message in the response
        alert(`Error: ${result.error}`);
      } else {
        // Handle undefined or unexpected result
        alert('Error: Unexpected response.');
      }
    } catch (error) {
      console.error('Error resetting account:', error);
      alert('An error occurred while resetting your account. Please try again.');
    }
  }
}


async function handleDeleteAccount(): Promise<void> {
  const confirmation = confirm("Are you sure you want to delete your account? This action cannot be undone!!!");

  if (confirmation) {
    try {
      const response = await fetch('/user/api/delete-account', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      });

      const result = await response.json();

      // Log the result to inspect what is being returned
      console.log('Response result:', result);

      // Check if the response is ok and contains the correct message
      if (response.ok && result.message) {
        alert(result.message); // Show the success message

        // Redirect the user to the index page after successful deletion
        window.location.href = "/"; // Redirect to the home page (index)
      } else if (result.error) {
        // Handle if there's an error message in the response
        alert(`Error: ${result.error}`);
      } else {
        // Handle undefined or unexpected result
        alert('Error: Unexpected response.');
      }
    } catch (error) {
      console.error('Error deleting account:', error);
      alert('An error occurred while deleting your account. Please try again.');
    }
  }
}



/****************
* Init function *
*****************/

// Function to initialize the page
function init(): void
{
  // Initialize dark mode based on user preference
  initDarkMode();

  // Attach event listener to dark mode toggle
  const DarkModeToggle = document.querySelector('.dark-mode-toggle');
  DarkModeToggle?.addEventListener('click', toggleDarkMode); // <?> checks whether darkModeToggle is not null or undefined before attempting to call the addEventListener method on it.

  // Attach event listener to the registration form
  const RegistrationForm = document.getElementById('registrationForm') as HTMLFormElement;
  RegistrationForm?.addEventListener('submit', handleRegistration); // Attach registration handler to the form submission

  // Attach event listener to the login form
  const LoginForm = document.getElementById('loginForm') as HTMLFormElement;
  LoginForm?.addEventListener('submit', handleLogin); // Attach registration handler to the form submission

  // Attach event listener to the stock symbol input for autocomplete
  const symbolInput = document.getElementById('symbol') as HTMLInputElement;
  symbolInput?.addEventListener('input', handleStockInput);

  // Add event listener to the Submit button
  document.getElementById("submitOrder")?.addEventListener("click", submitOrder);

  // Attach event listener to the Reset Account button
  const resetAccountButton = document.getElementById('btn-reset') as HTMLButtonElement;
  resetAccountButton?.addEventListener('click', handleResetAccount);

  // Attach event listener to the Delete Account button
  const DeleteAccountButton = document.getElementById('btn-delete') as HTMLButtonElement;
  DeleteAccountButton?.addEventListener('click', handleDeleteAccount);
}

// Run the initialization function after DOM content is loaded
document.addEventListener('DOMContentLoaded', init);


// RUN -> tsc --project tsconfig.json