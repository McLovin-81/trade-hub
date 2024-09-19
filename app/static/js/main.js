"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var _a;
// Utility function to toggle dark mode
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    // Optionally, you can store the user's preference in localStorage
    const isDarkMode = document.body.classList.contains('dark-mode');
    localStorage.setItem('dark-mode', isDarkMode.toString());
}
// Function to initialize dark mode based on user preference
function initDarkMode() {
    const savedDarkMode = localStorage.getItem('dark-mode') === 'true';
    if (savedDarkMode) {
        document.body.classList.add('dark-mode');
    }
}
// Function to show stock symbol suggestions and allow selection
function showSuggestions(suggestions) {
    const container = document.getElementById('suggestions-container');
    const symbolInput = document.getElementById('symbol');
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
function handleStockInput(event) {
    return __awaiter(this, void 0, void 0, function* () {
        const input = event.target.value;
        if (input.length > 1) {
            try {
                const response = yield fetch(`/user/api/stocks?query=${encodeURIComponent(input)}`);
                const data = yield response.json();
                if (Array.isArray(data.symbols)) {
                    showSuggestions(data.symbols);
                }
                else {
                    console.error('Unexpected response format:', data);
                    showSuggestions([]);
                }
            }
            catch (error) {
                console.error('Error fetching stock symbols:', error);
                showSuggestions([]);
            }
        }
        else {
            showSuggestions([]);
        }
    });
}
// Function to handle stock selection and fetch price from backend
function handleStockSelection(symbol) {
    return __awaiter(this, void 0, void 0, function* () {
        try {
            const response = yield fetch(`/user/api/stock-price?symbol=${encodeURIComponent(symbol)}`);
            const stockInfo = yield response.json();
            if (response.ok) {
                displayStockInfo(stockInfo); // Display stock price and name
            }
            else {
                console.error('Error fetching stock information:', stockInfo);
            }
        }
        catch (error) {
            console.error('Error fetching stock price:', error);
        }
    });
}
// Function to display stock information
function displayStockInfo(stockInfo) {
    const stockInfoDiv = document.getElementById('stockInfo');
    const stockNameSpan = document.getElementById('stockName');
    const stockPriceSpan = document.getElementById('stockPrice');
    if (stockInfoDiv && stockNameSpan && stockPriceSpan) {
        stockNameSpan.textContent = stockInfo.name;
        stockPriceSpan.textContent = stockInfo.currentPrice.toFixed(2);
        stockInfoDiv.style.display = 'block'; // Show the stock information div
    }
}
// Function to handle order submission
function submitOrder() {
    return __awaiter(this, void 0, void 0, function* () {
        const stockSymbol = document.getElementById("symbol").value;
        const orderType = document.getElementById("orderType").value;
        const quantity = parseInt(document.getElementById("quantity").value);
        const responseMessage = document.getElementById("responseMessage");
        if (stockSymbol && quantity > 0 && orderType) {
            try {
                const response = yield fetch(`/user/api/buy-stock`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ symbol: stockSymbol, quantity: quantity, orderType: orderType })
                });
                const data = yield response.json();
                if (response.ok && data.success) {
                    responseMessage.textContent = "Order placed successfully!";
                    responseMessage.style.color = "green";
                    // Reload the page after 1 second to show updated balance/depot data
                    setTimeout(() => {
                        window.location.reload();
                    }, 1000);
                }
                else {
                    responseMessage.textContent = "Failed to place the order. Insufficient balance or stock unavailable.";
                    responseMessage.style.color = "red";
                }
            }
            catch (error) {
                console.error('Error submitting order:', error);
                responseMessage.textContent = "An error occurred. Please try again.";
                responseMessage.style.color = "red";
            }
        }
        else {
            responseMessage.textContent = "Please fill out all fields correctly.";
            responseMessage.style.color = "red";
        }
    });
}
// Add event listener to the Submit button
(_a = document.getElementById("submitOrder")) === null || _a === void 0 ? void 0 : _a.addEventListener("click", submitOrder);
function handleRegistration(event) {
    return __awaiter(this, void 0, void 0, function* () {
        event.preventDefault();
        const nameInput = document.getElementById('username').value;
        const emailInput = document.getElementById('email').value;
        const passwordInput = document.getElementById('password').value;
        const passwordConfirmInput = document.getElementById('confirmPassword').value;
        if (passwordInput == passwordConfirmInput) {
            // The `fetch` function is asynchronous and returns a Promise
            const response = yield fetch('/auth/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    name: nameInput,
                    email: emailInput,
                    password: passwordInput
                }),
            });
            // Await the parsing of the response as JSON
            const result = yield response.json();
            if (response.ok) {
                alert('Registration successful!');
                window.location.href = result.redirect; // Redirect to login page
            }
            else {
                alert(`Error: ${result.error}`);
            }
        }
        else {
            alert('passwords do not match');
        }
    });
}
function handleLogin(event) {
    return __awaiter(this, void 0, void 0, function* () {
        event.preventDefault();
        const nameInput = document.getElementById('username').value;
        const passwordInput = document.getElementById('password').value;
        try {
            const response = yield fetch('/auth/login', {
                method: 'POST', // Use POST for login requests
                headers: { 'Content-Type': 'application/json' }, // Correct the header
                body: JSON.stringify({
                    name: nameInput,
                    password: passwordInput,
                }),
            });
            // Parse the response
            const result = yield response.json();
            if (response.ok) {
                alert(result.message);
                window.location.href = result.redirect; // Redirect on success
            }
            else {
                alert(`Error: ${result.error}`);
            }
        }
        catch (error) {
            // Handle potential network errors
            console.error('Error during login:', error);
            alert('An error occurred while logging in. Please try again.');
        }
    });
}
// Function to initialize the page
function init() {
    // Initialize dark mode based on user preference
    initDarkMode();
    // Attach event listener to dark mode toggle
    const DarkModeToggle = document.querySelector('.dark-mode-toggle');
    DarkModeToggle === null || DarkModeToggle === void 0 ? void 0 : DarkModeToggle.addEventListener('click', toggleDarkMode); // <?> checks whether darkModeToggle is not null or undefined before attempting to call the addEventListener method on it.
    // Attach event listener to the registration form
    const RegistrationForm = document.getElementById('registrationForm');
    RegistrationForm === null || RegistrationForm === void 0 ? void 0 : RegistrationForm.addEventListener('submit', handleRegistration); // Attach registration handler to the form submission
    // Attach event listener to the login form
    const LoginForm = document.getElementById('loginForm');
    LoginForm === null || LoginForm === void 0 ? void 0 : LoginForm.addEventListener('submit', handleLogin); // Attach registration handler to the form submission
    // Attach event listener to the stock symbol input for autocomplete
    const symbolInput = document.getElementById('symbol');
    symbolInput === null || symbolInput === void 0 ? void 0 : symbolInput.addEventListener('input', handleStockInput);
}
// Run the initialization function after DOM content is loaded
document.addEventListener('DOMContentLoaded', init);
// RUN -> tsc --project tsconfig.json
