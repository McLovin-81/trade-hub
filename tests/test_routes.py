
import unittest
from app import create_app

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_legend(self):
        response = self.client.get('/legend')
        self.assertEqual(response.status_code, 200)

    def test_get_data(self):
        response = self.client.get('/api/data')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello, World!', response.data)

    def test_post_data(self):
        response = self.client.post('/api/data', json={"key": "value"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'received', response.data)

if __name__ == '__main__':
    unittest.main()
