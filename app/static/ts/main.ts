
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

// Add event listener to the Submit button
document.getElementById("submitOrder")?.addEventListener("click", submitOrder);












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

// Function to set up the auto-submit form
function setupAutoSubmitForm(): void {
  const symbolSearch = document.getElementById("symbol_search") as HTMLInputElement | null;
  const orderForm = document.getElementById("orderForm") as HTMLFormElement | null;

  if (symbolSearch && orderForm) {
    symbolSearch.addEventListener("change", () => {
      // Optional: Überprüfe hier, ob das Eingabefeld nicht leer ist oder andere Validierungen.
      if (symbolSearch.value) {
        orderForm.submit();
      }
    });
  }
}


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
  const symbol_searchInput = document.getElementById('symbol') as HTMLInputElement;
  symbol_searchInput?.addEventListener('input', handleStockInput);

  
  // Attach event listener to the stock symbol input for autocomplete
  const symbolInput = document.getElementById('symbol') as HTMLInputElement;
  symbolInput?.addEventListener('input', handleStockInput);


  // Setup auto-submit form functionality
  setupAutoSubmitForm(); 
}

// Run the initialization function after DOM content is loaded
document.addEventListener('DOMContentLoaded', init);


// RUN -> tsc --project tsconfig.json