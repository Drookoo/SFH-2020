from flask import Flask

#If you see this, branch andrew works

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'
from app import routes

