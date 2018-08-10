# Todo List
[![Build Status](https://travis-ci.org/james-o-johnstone/todo-list.svg?branch=master)](https://travis-ci.org/james-o-johnstone/todo-list)[![Coverage Status](https://coveralls.io/repos/github/james-o-johnstone/todo-list/badge.svg?branch=master)](https://coveralls.io/github/james-o-johnstone/todo-list?branch=master)

## About 
REST API written in Python/Flask to manage a simple todo list.

Documents are persisted in [MongoDB](https://www.mongodb.com/).

## Installation
1. [Install MongoDB](https://docs.mongodb.com/manual/installation/)
2. cd to the project folder, create and activate a virtual env, e.g.: `python3 -m virtualenv env && source env/bin/activate`
3. `pip install -r requirements.txt && pip install .`

## Tests
To run the tests, a local instance of MongoDB must be running (e.g.: [running MongoDB on Linux](https://docs.mongodb.com/manual/tutorial/install-mongodb-enterprise-on-ubuntu/#run-mongodb-enterprise))

Ensure that you are in the virtualenv, cd to the project folder and: `python -m unittest discover -s tests`

## Documentation
To run the Flask app cd to the project folder and `python todo_api/main.py`

### Authentication
The app has been hardcoded with a single user (login = test_login, password = password123). 

After login the session value in the response cookie can be used to authenticate further api requests.

#### Example 
To obtain a session cookie for this user.

##### Request
`POST http://localhost:5000/login`

##### Request Body
```
{
    "login": "test_login",
    "password": "password123"
}
```

##### Response 
```
Status: 200 OK
Headers:
  Set-Cookie: session=.eJwlzrsNwzAMANFdVLsgRUqivEzAj4ikteMqyO4xkAEO7z7lkcc6n2V_H9fayuMVZS9TQ8h8uGjNGHWFuTqoKy0ZYZgAXWt1Vkaj5gGMXu8GeSZoBkjnLgNxdWuSvUsDJmhzVQ5CAUcEdkJ0t5vJfnuYU_FWrWzlOtfxn2nWrTanljMpzOrEucShfH-IRjYj.Dk5TQA.rDiobiHxUpvjFf7F8txh4-1Vvm4;
```

### Create a new todo item
A todo item requires a title, the description field is optional.

Returns a new todo item.

#### Example

##### Request
`POST http://localhost:5000/todo/todo_item`

##### Request Body
```
{
	"title": "title",
	"description": "description"
}
```

#### Response
```
{
    "item": {
        "completed": false,
        "description": "description",
        "id": "5b6cbd6a57fac3dbb6cb242f",
        "title": "title",
        "user_id": "5b6b25c35f9f3dbb2919e8c0"
    }
}
```

### List a user's set of todo items
`GET http://localhost:5000/todo/todo_item/:user_id`

Returns a list of todo items.

#### Example

##### Request
`GET http://localhost:5000/todo/todo_item/5b6b25c35f9f3dbb2919e8c0`

##### Response
```
[
    {
        "item": {
            "completed": true,
            "description": "description1",
            "id": "5b6b37245f9f3dbfda30cc7f",
            "title": "title1",
            "user_id": "5b6b25c35f9f3dbb2919e8c0"
        }
    },
    {
        "item": {
            "completed": false,
            "description": "description2",
            "id": "5b6b37585f9f3dbfef989bd2",
            "title": "title2",
            "user_id": "5b6b25c35f9f3dbb2919e8c0"
        }
    },
]
```

### Mark any single todo item as completed
`PUT http://localhost:5000/todo/todo_item/:item_id`

The same request can also be used to mark the todo item as not complete (by using `"completed": false` in the request body).

Returns the updated todo item.

#### Example

##### Request
`PUT http://localhost:5000/todo/todo_item/5b6b4f2d57fac3c5eac1aa6a`

##### Request Body
```
{
	"completed": true
}
```

##### Response
```
{
    "item": {
        "completed": true,
        "description": "description",
        "id": "5b6b4f2d57fac3c5eac1aa6a",
        "title": "title",
        "user_id": "5b6b25c35f9f3dbb2919e8c0"
    }
}
```

### Delete any single todo item
`DELETE http://localhost:5000/todo/todo_item/:item_id`

#### Example

##### Request
`DELETE http://localhost:5000/todo/todo_item/5b6b4f2d57fac3c5eac1aa6a`

##### Response
```
Status: 204 NO CONTENT
```

### Logout

#### Example

##### Request
`GET http://localhost:5000/logout`

##### Response
```
Status: 204 NO CONTENT
```



