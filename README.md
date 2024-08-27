# Trade Hub

Das Projektziel besteht in der Entwicklung einer Simulationsplatform zum spielerischen Erlernen von praxisnahem und lehrreichen Verständnis für den Handel mit Wertpapieren. Die Plattform ermöglicht es den Benutzern, mithilfe von virtuellem Kapital, Käufe und Verkäufe von Wertpapieren durchzuführen. Das Gesamtkapital des Benutzers wird in Echtzeit basierend auf den aktuellen Börsenkursen berechnet und angepasst. Darüber hinaus soll die Simulation die Dynamiken des echten Börsenhandels visuell abbilden. 
Das Projekt ist erfolgreich abgeschlossen nach bestandenen Tests, Inbetriebnahme und Übergabe an den Kunden.

## Table of Contents

1. [General Requirements](#general-requirements)
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

## Kontoverwaltung

- **Kontoerstellung:**
  - Benutzer müssen einen Usernamen und ein Passwort angeben.
  - Nach erfolgreicher Registrierung wird jedem neuen Benutzer ein festgelegtes Startkapital gutgeschrieben.

- **Passwortverwaltung:**
  - Benutzer können ihr Passwort bei Bedarf zurücksetzen.

- **Kontolöschung:**
  - Benutzer können eine Anfrage auf Löschung ihres Kontos stellen.
  - Administratoren sind befugt, Konten auf Anfrage zu resetten oder vollständig zu löschen.

## Depotverwaltung

- **Order-Erstellung:**
  - Benutzer können Orders zum Kauf und Verkauf von Aktien erstellen.

- **Depotübersicht:**
  - Benutzer können den aktuellen Wert ihres Depots jederzeit einsehen.

- **Marktanalyse:**
  - Benutzer können den aktuellen Marktwert bestimmter Aktien abrufen, um fundierte Entscheidungen zu treffen.

## Bestenliste

- **Wöchentliche Bestenliste:**
  - Zeigt die Benutzer mit den meisten Gewinnen der aktuellen Woche in absteigender Reihenfolge an.

- **Gesamt-Bestenliste:**
  - Zeigt die Benutzer mit den meisten Gewinnen über die gesamte Zeit in absteigender Reihenfolge an.

- **Auswirkungen eines Resets:**
  - Bei einem Reset des Kontos wird der Benutzer aus den Bestenlisten entfernt, bis er erneut mit dem Handel beginnt.


## Testing

Tests sind ein wesentlicher Bestandteil von Trade Hub. Wir setzen die folgenden Strategien ein:

- **Unit Testing:** Testen einzelner Komponenten, um sicherzustellen, dass sie wie erwartet funktionieren.
- **Integration Testing:** Überprüfung, ob verschiedene Teile der Anwendung zusammen korrekt arbeiten.
- **End-to-End Testing:** Validierung kompletter Benutzerabläufe, von der Interaktion bis zur Datenverarbeitung.

Für detaillierte Testfälle und -verfahren siehe die Datei [TESTING.md](TESTING.md).