import logging

from bson import ObjectId

from todo_api.extensions import db


logger = logging.getLogger(__name__)


class User(db.Document):
    login = db.StringField(max_length=80, unique=True)
    email = db.StringField(max_length=120)
    password = db.StringField(max_length=64)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    @classmethod
    def find_user(cls, login):
        try:
            user = cls.objects(login=login).first()
        except Exception as e:
            logger.exception(e)
            raise DatabaseError
        else:
            return user


class TodoItem(db.Document):
    user_id = db.ObjectIdField()
    title = db.StringField(max_length=120, required=True)
    description = db.StringField()
    completed = db.BooleanField()

    @classmethod
    def find_user_items(cls, user_id):
        try:
            items = cls.objects(user_id=user_id)
        except Exception as e:
            logger.exception(e)
            raise DatabaseError
        else:
            return items

    @classmethod
    def find_item(cls, item_id):
        try:
            item = cls.objects(id=item_id).first()
        except Exception as e:
            logger.exception(e)
            raise DatabaseError
        else:
            return item

    @classmethod
    def create(cls, **kwargs):
        try:
            item = cls(**kwargs).save()
        except Exception as e:
            logger.exception(e)
            raise DatabaseError
        else:
            return item

    def update(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)

        try:
            self.save()
        except Exception as e:
            logger.exception(e)
            raise DatabaseError

    @classmethod
    def delete_item(cls, item_id):
        try:
            cls.objects(id=item_id).delete()
        except Exception as e:
            logger.exception(e)
            raise DatabaseError

    def jsonify(self):
        return {
            'item': {
                'completed': self.completed,
                'description': self.description,
                'id': str(self.id),
                'title': self.title,
                'user_id': str(self.user_id),
            }
        }


def validate_id(_id):
    return ObjectId.is_valid(_id)


class DatabaseError(Exception):
    def __str__(self):
        return "Database Error"
