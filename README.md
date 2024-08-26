# Trade Hub

Das Projektziel besteht in der Entwicklung einer Simulationsplattform für Wertpapierdepots. Die Plattform ermöglicht es den Benutzern, mithilfe von virtuellem Kapital Käufe und Verkäufe von Wertpapieren durchzuführen. Das Gesamtkapital des Benutzers wird in Echtzeit basierend auf den aktuellen Börsenkursen berechnet und angepasst. Darüber hinaus soll die Simulation die Dynamiken des echten Börsenhandels abbilden und den Benutzern ein praxisnahes und lehrreiches Verständnis für den Handel mit Wertpapieren vermitteln.

## Table of Contents

1. [Requirements](#requirements)
2. [Project-related Requirements](#project-related-requirements)
3. [Testing](#testing)

## Requirements

### General Requirements

- **Plattformunabhängigkeit:** 
  - Alle Programme müssen betriebssystem-unabhängig compilierbar und ausführbar sein (bei stand-alone-Lösungen).
  - Web-Applikationen müssen browser-unabhängig aufrufbar sein.

- **Modularisierung:** 
  - Model und View müssen bei allen Programmen getrennt sein, sodass die View austauschbar ist.

- **Responsives Design:** 
  - Web-Applikationen müssen über ein responsive Design verfügen, das für Smartphones, Tablets und PCs optimiert ist.

- **Hilfebereich:** 
  - Alle Programme müssen einen Hilfe-Bereich enthalten, in dem die Funktionalität und Bedienung des Programms erklärt werden.

- **Kreativer Name und Logo:** 
  - Das Programm muss einen kreativen Namen und ein Logo haben, das stets sichtbar ist.

## Testmanagement
- **Testkonzept:** 
  - Für alle Projekte ist ein Testmanagement mit sinnvollen Tests durchzuführen, basierend auf einem Testkonzept, das verschiedene Entwicklungsstufen abdeckt.

## Versionskontrolle und Projektmanagement
- **Repository:** 
  - Für alle Dateien ist ein Repository zu verwenden.
  
- **Kanban-Board:** 
  - Für alle Aufgaben ist ein Kanban-Board zu verwenden.

## Dokumentation
- **Bedienungs- und Installationsanleitung:** 
  - Für alle Programme sind eine Bedienungsanleitung (für User) und eine Installationsanleitung (für Administratoren) zu erstellen.

## User-Verwaltung
- **User-Rollen:** 
  - Es gibt User und Administratoren. Ein Admin kann auch als User das Programm verwenden.
  
- **Registrierung und Freischaltung:** 
  - User können sich selbst registrieren, müssen aber von Admins freigeschaltet werden. Admins können User auch sperren.

- **Sicherheitsanforderungen:** 
  - User-Daten (Login-Name als E-Mail-Adresse und Passwort) werden in Datenbanken verschlüsselt gespeichert.
  - Datenübertragungen zwischen Server und Client (oder Front-End) sind zu verschlüsseln.
  - Daten sollen in einem definierten Format (z.B. JSON, XML) übertragen werden.

## Benutzerfreundlichkeit
- **Barrierefreiheit:** 
  - Alle Oberflächen sind barrierefrei zu implementieren.
  
- **Eingabesicherheit:** 
  - Alle Eingabemöglichkeiten sind möglichst DAU-sicher zu gestalten und, wenn möglich, mit regulären Ausdrücken zu prüfen.

## Project-related Requirements

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

Tests sind ein wesentlicher Bestandteil von Trade Hub. Wir setzen die folgenden Strategien ein:

- **Unit Testing:** Testen einzelner Komponenten, um sicherzustellen, dass sie wie erwartet funktionieren.
- **Integration Testing:** Überprüfung, ob verschiedene Teile der Anwendung zusammen korrekt arbeiten.
- **End-to-End Testing:** Validierung kompletter Benutzerabläufe, von der Interaktion bis zur Datenverarbeitung.

Für detaillierte Testfälle und -verfahren siehe die Datei [TESTING.md](TESTING.md).