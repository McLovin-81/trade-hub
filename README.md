# Trade Hub

The project aims to develop a simulation platform for stock portfolios. The platform allows users to conduct purchases and sales of securities using virtual capital. The user's total capital is calculated and adjusted in real-time based on current stock market prices. Additionally, the simulation is designed to replicate the dynamics of real-world trading, providing users with a practical and educational understanding of stock market operations.

Das Projektziel besteht in der Entwicklung einer Simulationsplattform für Wertpapierdepots. Die Plattform ermöglicht es den Benutzern, mithilfe von virtuellem Kapital Käufe und Verkäufe von Wertpapieren durchzuführen. Das Gesamtkapital des Benutzers wird in Echtzeit basierend auf den aktuellen Börsenkursen berechnet und angepasst. Darüber hinaus soll die Simulation die Dynamiken des echten Börsenhandels abbilden und den Benutzern ein praxisnahes und lehrreiches Verständnis für den Handel mit Wertpapieren vermitteln.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Requirements](#requirements)
3. [Features](#features)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Testing](#testing)
7. [Contributing](#contributing)
8. [License](#license)
9. [Contact](#contact)

## Project Overview

Trade Hub is a robust web application designed to facilitate trade exchanges between users. It ensures cross-browser compatibility and responsive design to deliver a consistent experience across smartphones, tablets, and PCs. Developed to meet the IT-Project 2024 requirements, Trade Hub features a modular architecture and incorporates advanced functionalities for an intuitive user experience.

## Requirements

### General Requirements

- **Cross-Platform Compatibility:** The application is designed to be browser-independent, working seamlessly across all modern web browsers.
- **MVC Architecture:** Adheres to the Model-View-Controller (MVC) design pattern, enabling modular code with a separable view layer.
- **Responsive Design:** Features a responsive design that adapts to various screen sizes and devices.
- **Help Section:** Includes a comprehensive help section explaining the application’s functionality and usage.
- **Creative Branding:** The platform features the name **Trade Hub** and a unique logo that is prominently displayed.
- **Test Management:** Includes test management with meaningful tests based on a test concept throughout different development stages.
- **Repository & Kanban Board:** Uses a version-controlled repository and a Kanban board for task management.
- **User & Admin Management:** 
  - Users and administrators have distinct roles.
  - Admins can also act as users.
  - User registration requires admin approval, with the ability for admins to activate or deactivate accounts.
  - User data is encrypted and securely stored in the database.
- **Data Security:** Ensures secure data transmission between server and client with encryption, using formats like JSON or XML for data transfer.
- **Accessibility:** Designed with accessibility in mind, including input validation with regular expressions for ease of use.
- **User Documentation:** Provides user manuals and installation guides in English.

## Features

### 1. User Management

#### Account Creation
- Users can create an account by providing the following information:
  - First Name
  - Last Name
  - Email Address
- Each new user receives a predefined starting capital.

#### Account Management
- Users can reset their password.
- Users can request to reset their account.
- Admins can reactivate suspended accounts.
- Admins can delete accounts upon request.

### 2. Portfolio Management

#### Order Management
- Users can place orders to buy and sell stocks.
- Users can view the current value of their own portfolio.

#### Capital and Value Calculation
- Each new user is assigned a starting capital.
- Users can view the current market value of specific stocks.
- Admins can calculate the total value of all portfolios.

### 3. Admin Functions

#### Admin Responsibilities
- Admins can view all user accounts.
- Admins can reactivate suspended accounts.
- Admins can calculate the total value of all portfolios.
- Admins can delete accounts upon request.



### 1. Benutzerverwaltung

#### Kontoerstellung
- Benutzer können ein Konto einrichten, indem sie folgende Informationen angeben:
  - Vorname
  - Nachname
  - E-Mail-Adresse
- Jeder neue Benutzer erhält ein festgelegtes Startkapital.

#### Kontoverwaltung
- Benutzer können ihr Passwort zurücksetzen.
- Benutzer können ihr Konto auf Wunsch zurücksetzen lassen.
- Administratoren können gesperrte Konten wieder freigeben.
- Administratoren können Konten auf Anfrage löschen.

### 2. Depotverwaltung

#### Order-Management
- Benutzer können Orders zum Kauf und Verkauf von Aktien erstellen.
- Benutzer können den aktuellen Wert ihres eigenen Depots anzeigen lassen.

#### Kapital- und Wertberechnung
- Das Startkapital wird jedem neuen Benutzer zugewiesen.
- Benutzer können den aktuellen Marktwert bestimmter Aktien anzeigen lassen.
- Administratoren können den Gesamtwert aller Depots berechnen.

### 3. Admin-Funktionen

#### Aufgaben der Administratoren
- Administratoren können alle Benutzerkonten einsehen.
- Administratoren können gesperrte Konten wieder freigeben.
- Administratoren können den Gesamtwert aller Depots berechnen.
- Administratoren können Konten auf Anfrage löschen.


## Testing

Testing is a key component of Trade Hub. We employ the following strategies:

- **Unit Testing:** Test individual components to ensure they work as expected.
- **Integration Testing:** Verify that different parts of the application function together correctly.
- **End-to-End Testing:** Validate complete user workflows from interaction to data handling.

For detailed test cases and procedures, see the [TESTING.md](TESTING.md) file.
