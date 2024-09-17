import os
import unittest
from app import create_app  # Deine App-Fabrik
from app.database.db import init_db  # Deine DB-Initialisierungsfunktion
from instance.test_config import TestConfig

class TestUserDbIntegration(unittest.TestCase):

    def setUp(self):
        # Test-App mit der Testkonfiguration erstellen
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

        # Context und Datenbank initialisieren
        with self.app.app_context():
            init_db()  # Initialisiert die Testdatenbank mit den Tabellen

    def tearDown(self):
        # Datenbank nach jedem Test aufräumen (optional)
        os.remove(self.app.config['DATABASE'])
    
    def test_register(self):
        response = self.client.post('/auth/register', json={
            'name': 'testuser_register',
            'email': 'testuser@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        # Zuerst registrieren wir einen Benutzer
        self.client.post('/auth/register', json={
            'name': 'testuser_login',
            'email': 'testuser@example.com',
            'password': '12345678'
        })

        # Danach versuchen wir, uns mit diesem Benutzer anzumelden
        response = self.client.post('/auth/login', json={
            'name': 'testuser_login',
            'password': '12345678'
        })
        self.assertEqual(response.status_code, 200)