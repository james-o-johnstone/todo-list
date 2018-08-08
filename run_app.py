from app import create_app
from config import Config


app = create_app(Config)
app.run(debug=True)

from models import User
User(login='test_user', password='password123').save()