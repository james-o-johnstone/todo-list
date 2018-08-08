from app import create_app
from config import Config
from models import User

app = create_app(Config)

if User.objects(login='test_user').first() is None:
    User(login='test_user', password='password123').save()

app.run(debug=True)
