# Trade Hub

Trade Hub is a simulation platform designed to provide a hands-on, educational experience for trading securities. Users can engage in buying and selling of securities using virtual capital, with their total capital dynamically updated based on real-time market prices. The simulation visually represents the dynamics of real-world stock trading.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Project Setup](#project-setup)

## Project Overview

Trade Hub aims to teach users about stock trading in a practical and engaging manner. The platform allows users to simulate trading activities, providing real-time feedback on their investments and portfolio value.


Note:
    Open the SQLite Database
        sqlite3 trade_hub_database.sqlite
    To exit SQLite
        .exit

How to run the application for the first time

in trade-hub
    bash -> flask --app app init-db

How the certificates was created:
    openssl req -x509 -newkey rsa:4096 -keyout instance/certs/key.pem -out instance/certs/cert.pem -days 365

test