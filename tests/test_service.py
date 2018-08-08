import unittest
import json

from app import create_app
from extensions import db
from models import User
from routes import login


TEST_DB_NAME = 'test'


class TestConfig(object):
    SECRET_KEY = '123456'
    MONGODB_SETTINGS = {'DB': TEST_DB_NAME}
    TESTING = True


class TestLogin(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.test_client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.connection.drop_database(TEST_DB_NAME)

    def test_login(self):
        login = 'login'
        password = 'password'
        User(login=login, password=password).save()

        response = self.test_client.post(
            '/login',
            data=json.dumps(
                {'login': login, 'password': password}
            ),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)

    def test_login_not_found(self):
        response = self.test_client.post(
            '/login',
            data=json.dumps(
                {'login': 'login', 'password': 'password'}
            ),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 401)

    def test_incorrect_login(self):
        password = 'password'
        User(login='test_login', password=password).save()

        response = self.test_client.post(
            '/login',
            data=json.dumps(
                {'login': 'incorrect_login', 'password': password}
            ),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 401)

    def test_incorrect_password(self):
        login = 'login'
        User(login=login, password='password').save()

        response = self.test_client.post(
            '/login',
            data=json.dumps(
                {'login': login, 'password': '123456'}
            ),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 401)

    def test_invalid_json(self):
        response = self.test_client.post(
            '/login',
            data=json.dumps(
                {'abc': 'test_login'}
            ),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)
