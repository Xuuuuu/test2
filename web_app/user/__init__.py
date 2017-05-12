from flask import Flask,Blueprint

user = Blueprint('user',__name__)

from user import views
