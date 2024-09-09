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
// Function to handle login button click
function handleLoginClick() {
    alert('Login button clicked! Implement your login logic here.');
}
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
function handleRegistration(event) {
    return __awaiter(this, void 0, void 0, function* () {
        event.preventDefault();
        const nameInput = document.getElementById('username').value;
        const emailInput = document.getElementById('email').value;
        const passwordInput = document.getElementById('password').value;
        if (nameInput && emailInput && passwordInput) {
            try {
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
                }
                else {
                    alert('Failed to register.');
                }
            }
            catch (error) {
                console.error('Error:', error);
                alert('An error occurred while registering.');
            }
        }
        else {
            alert('Please fill out all fields.');
        }
    });
}
// Function to initialize the page
function init() {
    // Initialize dark mode based on user preference
    initDarkMode();
    // Attach event listener to dark mode toggle
    const darkModeToggle = document.querySelector('.dark-mode-toggle');
    darkModeToggle === null || darkModeToggle === void 0 ? void 0 : darkModeToggle.addEventListener('click', toggleDarkMode); // <?> checks whether darkModeToggle is not null or undefined before attempting to call the addEventListener method on it.
    // Attach event listener to login button
    const loginButton = document.querySelector('.btn');
    loginButton === null || loginButton === void 0 ? void 0 : loginButton.addEventListener('click', handleLoginClick);
    // Attach event listener to the registration form
    const form = document.getElementById('registrationForm');
    form === null || form === void 0 ? void 0 : form.addEventListener('submit', handleRegistration); // Attach registration handler to the form submission
}
// Run the initialization function after DOM content is loaded
document.addEventListener('DOMContentLoaded', init);
// RUN -> tsc --project tsconfig.json
