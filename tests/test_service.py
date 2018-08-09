import json
import unittest

from flask_login import AnonymousUserMixin

from todo_api.app import create_app
from todo_api.extensions import db, login_manager
from todo_api.models import User, TodoItem


TEST_DB_NAME = 'test'


class TestConfig(object):
    SECRET_KEY = '123456'
    MONGODB_SETTINGS = {'DB': TEST_DB_NAME}
    LOGIN_DISABLED = True
    TESTING = True


class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.id = "5b6b37245f9f3dbfda30cc7f"


class BaseTestService(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.test_client = self.app.test_client()

        login_manager.anonymous_user = Anonymous

    def tearDown(self):
        with self.app.app_context():
            db.connection.drop_database(TEST_DB_NAME)


class TestLogin(BaseTestService):
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
        self.assertEqual(response.status_code, 204)

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


class TestCreateTodo(BaseTestService):
    def test_create(self):
        response = self.test_client.post(
            '/todo/todo_items',
            data=json.dumps(
                {'title': 'title', 'description': 'description'}
            ),
            content_type='application/json',
        )

        expected_item = {
            'completed': False,
            'description': 'description',
            'title': 'title',
        }
        item = response.get_json()['item']

        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(item['id'])
        self.assertIsNotNone(item['user_id'])

        modified_item = item.copy()
        modified_item.pop('id')
        modified_item.pop('user_id')

        self.assertDictEqual(
            modified_item,
            expected_item,
        )

    def test_create_no_description(self):
        response = self.test_client.post(
            '/todo/todo_items',
            data=json.dumps(
                {'title': 'title'}
            ),
            content_type='application/json',
        )

        item = response.get_json()['item']
        self.assertEqual(item['description'], '')

    def test_create_invalid_json(self):
        response = self.test_client.post(
            '/todo/todo_items',
            data=json.dumps(
                {'description': 'description'}
            ),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)

    def test_create_no_json(self):
        response = self.test_client.post(
            '/todo/todo_items',
        )
        self.assertEqual(response.status_code, 400)


class TestUpdateTodo(BaseTestService):
    def test_update(self):
        item = TodoItem(
            user_id='5b6b37245f9f3dbfda30cc7f',
            title='title',
            description='description',
            completed=False,
        ).save()

        response = self.test_client.put(
            '/todo/todo_items/%s' % str(item.id),
            data=json.dumps({'completed': True}),
            content_type='application/json',
        )

        item = response.get_json()['item']

        self.assertEqual(response.status_code, 200)
        self.assertTrue(item['completed'])

    def test_no_json(self):
        response = self.test_client.put(
            '/todo/todo_items/item_id',
        )
        self.assertEqual(response.status_code, 400)

    def test_invalid_item_id(self):
        response = self.test_client.put(
            '/todo/todo_items/123456',
            data=json.dumps({'completed': True}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)

    def test_no_items(self):
        response = self.test_client.put(
            '/todo/todo_items/5b6b37245f9f3dbfda30cc7f',
            data=json.dumps({'completed': True}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 404)


class TestGetItems(BaseTestService):
    def test_get_user_items(self):
        user_id = '5b6b37245f9f3dbfda30cc7f'
        expected_items = []
        for i in range(2):
            title = 'title%s' % i
            desc = 'description%s' % i
            item = TodoItem(
                user_id=user_id,
                title=title,
                description=desc,
                completed=False,
            ).save()
            expected_items.append({
                'item': {
                    'completed': False,
                    'description': desc,
                    'id': str(item.id),
                    'title': title,
                    'user_id': user_id,
                }
            })

        response = self.test_client.get('/todo/todo_items/%s' % user_id)
        self.assertEqual(response.status_code, 200)

        response_items = response.get_json()
        for item, expected in zip(response_items, expected_items):
            self.assertDictEqual(item, expected)

    def test_no_items(self):
        response = self.test_client.get('/todo/todo_items/5b6b37245f9f3dbfda30cc7f')
        self.assertEqual(response.status_code, 200)

        items = response.get_json()
        self.assertEqual([], items)

    def test_invalid_user_id(self):
        response = self.test_client.get('/todo/todo_items/123456')
        self.assertEqual(response.status_code, 400)


class TestDeleteItem(BaseTestService):
    def test_delete(self):
        item = TodoItem(
            user_id='5b6b37245f9f3dbfda30cc7f',
            title='title',
            description='description',
            completed=False,
        ).save()

        response = self.test_client.delete('/todo/todo_items/%s' % str(item.id))
        self.assertEqual(response.status_code, 204)

    def test_invalid_item_id(self):
        response = self.test_client.delete('/todo/todo_items/abcdef')
        self.assertEqual(response.status_code, 400)

    def test_delete_missing_item(self):
        response = self.test_client.delete('/todo/todo_items/5b6b37245f9f3dbfda30cc7f')
        self.assertEqual(response.status_code, 204)
