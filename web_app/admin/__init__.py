from flask import Flask,Blueprint


admin = Blueprint('admin',__name__)

from . import views


