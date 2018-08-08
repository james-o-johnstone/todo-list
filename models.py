from extensions import db


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


class TodoItem(db.Document):
    user_id = db.ObjectIdField()
    title = db.StringField(max_length=120, required=True)
    description = db.StringField()
    completed = db.BooleanField()
