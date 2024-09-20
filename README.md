# Trade Hub

Trade Hub is a simulation platform designed to provide a hands-on, educational experience for trading securities. Users can engage in buying and selling of securities using virtual capital, with their total capital dynamically updated based on real-time market prices. The simulation visually represents the dynamics of real-world stock trading.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Project Setup](#project-setup)
3. [Project Run](#project-run)  

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

How to run the unit tests in ~:
    python3 -m unittest discover -s tests/unit_tests

How to run integration tests in ~:
    python3 -m unittest discover -s tests/integration_tests

## Project Setup
Installation von Abhängigkeiten aus `requirements.txt` in einer virtuellen Umgebung

Um die Abhängigkeiten aus einer `requirements.txt`-Datei automatisch in eine virtuelle Umgebung zu installieren, folge diesen Schritten:

## 1. Erstelle eine virtuelle Umgebung


```bash
python -m venv env
```
## 2. Aktiviere die virtuelle Umgebung

Windows:
```bash
.\env\Scripts\activate
```
Linux:
```bash
source env/bin/activate
```

## 3. Installiere die Abhängigkeiten
Installiere die Abhängigkeiten aus der requirements.txt mit folgendem Befehl:

```bash

pip install -r requirements.txt
```

## Project Run

## 1. Initiieren der Datenbank
```bash
flask init-db
```
## 2. Starten der Anwendung
Aus dem ~ Ordner 
```bash
python3 -m app.main
```