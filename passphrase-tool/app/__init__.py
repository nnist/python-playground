from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key-thing'

from app import routes
