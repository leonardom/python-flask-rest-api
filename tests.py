import unittest
import json
from run import app

class TestHome(unittest.TestCase):

    def setUp(self):
        appclient = app.test_client()
        self.response = appclient.get('/')
        
    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_content_type(self):
        self.assertIn('application/json', self.response.content_type)

    def test_content(self):
        self.assertIn('"message": "Hello, World!"', self.response.data.decode('utf-8'))


class TestApi(unittest.TestCase):

    def setUp(self):
        self.appclient = app.test_client()


    @unittest.skip
    def test_user_registration(self):
        """Test API can register a user"""
        response = self.appclient.post('/registration', data={'username': 'test', 'password':'123'})
        self.assertIn('"message": "User test was created"', response.data.decode('utf-8'))


    def test_user_successful_login(self):
        """Test API successful login"""

        response = self.appclient.post('/login', data={'username': 'test', 'password':'123'})

        self.assertIn('"message": "Logged in as test"', response.data.decode('utf-8'))
        self.assertIn('access_token', response.data.decode('utf-8'))
        self.assertIn('refresh_token', response.data.decode('utf-8'))
        

    def test_user_unsuccessful_login(self):
        """Test API unsuccessful login"""

        response = self.appclient.post('/login', data={'username': 'test', 'password':'wrong'})
        self.assertIn('"message": "Wrong credentials"', response.data.decode('utf-8'))

    def test_token_refresh(self):
        """Test API token refresh"""

        response = self.appclient.post('/login', data={'username': 'test', 'password':'123'})
        json_res = json.loads(response.data.decode('utf-8'))

        response = self.appclient.post('/token/refresh', data={}, headers={'Authorization': 'Bearer ' + json_res['refresh_token']})
        self.assertIn('access_token', response.data.decode('utf-8'))
    
    def test_all_users(self):
        """Test API get all users"""

        response = self.appclient.get('/users')
        json_res = json.loads(response.data.decode('utf-8'))
        self.assertTrue(len(json_res) > 0)


    def test_secret(self):
        """Test API secret"""

        response = self.appclient.post('/login', data={'username': 'test', 'password':'123'})
        json_res = json.loads(response.data.decode('utf-8'))

        response = self.appclient.get('/secret', headers={'Authorization': 'Bearer ' + json_res['access_token']})
        self.assertIn('"answer": 42', response.data.decode('utf-8'))


    def test_logout_access(self):
        """Test API logout access"""

        response = self.appclient.post('/login', data={'username': 'test', 'password':'123'})
        json_res = json.loads(response.data.decode('utf-8'))

        response = self.appclient.post('/logout/access', headers={'Authorization': 'Bearer ' + json_res['access_token']})
        self.assertIn('"message": "Access token has been revoked"', response.data.decode('utf-8'))


    def test_logout_refresh(self):
        """Test API logout refresh"""

        response = self.appclient.post('/login', data={'username': 'test', 'password':'123'})
        json_res = json.loads(response.data.decode('utf-8'))

        response = self.appclient.post('/logout/refresh', headers={'Authorization': 'Bearer ' + json_res['refresh_token']})
        self.assertIn('"message": "Refresh token has been revoked"', response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()