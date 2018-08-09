from todo_api.app import create_app
from todo_api.config import Config
from todo_api.models import User


def run_app():
    app = create_app(Config)

    # creating multiple users out of scope so just
    # create a single hardcoded user and save to mongo
    if User.objects(login='test_user').first() is None:
        User(login='test_user', password='password123').save()

    app.run(debug=True)


if __name__ == '__main__':
    run_app()
