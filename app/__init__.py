from flask import Flask
from config import Config
app.config.from_object(Config)

app = Flask(__name__)

from app import routes

