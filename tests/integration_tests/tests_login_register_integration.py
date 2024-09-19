import os
import unittest
from app import create_app  
from app.database.db import init_db  
from instance.test_config import TestConfig

class TestUserDbIntegration(unittest.TestCase):

    def setUp(self):
        # Test-App mit der Testkonfiguration erstellen
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

        # Context und Datenbank initialisieren
        with self.app.app_context():
            init_db()  # Initialisiert die Testdatenbank mit den Tabellen
        
            # registering a user for the@login required routes
            self.client.post('/auth/register', json={
                'name': 'testuser_required_routes',
                'email': 'testuser_required_routes@example.com',
                'password': 'HalloW3lt1337'
            })
            
        
            

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
        # first registering a user
        self.client.post('/auth/register', json={
            'name': 'testuser_login',
            'email': 'testuser@example.com',
            'password': '12345678'
        })

        # login the previously registered user
        response = self.client.post('/auth/login', json={
            'name': 'testuser_login',
            'password': '12345678'
        })
        self.assertEqual(response.status_code, 200)

# =============== GET TESTS =======================
        
    def test_get_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_get_register(self):
        response = self.client.get('/auth/register')
        self.assertEqual(response.status_code, 200)

    def test_get_index(self):
        response = self.client.get('/auth/login')
        self.assertEqual(response.status_code, 200)
    
    def test_get_detailPage(self):
        response = self.client.get('/detailPage')
        self.assertEqual(response.status_code, 200)
    
    def test_get_depot(self):
        login_response = self.client.post('/auth/login', json={
                'name': 'testuser_required_routes',
                'password': 'HalloW3lt1337'
            })

        response = self.client.get('/user/testuser_required_routes/depot')
        self.assertEqual(response.status_code, 200)

    def test_get_transactions(self):
        login_response = self.client.post('/auth/login', json={
                'name': 'testuser_required_routes',
                'password': 'HalloW3lt1337'
            })
        
        response = self.client.get('/user/testuser_required_routes/transactions')
        self.assertEqual(response.status_code, 200)

    def test_get_ordermanagement(self):
        login_response = self.client.post('/auth/login', json={
                'name': 'testuser_required_routes',
                'password': 'HalloW3lt1337'
            })
       
        response = self.client.get('/user/testuser_required_routes/ordermanagement')
        self.assertEqual(response.status_code, 200)

    