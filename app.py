from flask import Flask
from backend.models import *

app=None

def init_app():
    my_app=Flask(__name__)
    my_app.debug=True
    my_app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///myapp.sqlite3"
    my_app.config["SECRET_KEY"]="sayhello1234"
    my_app.app_context().push()
    db.init_app(my_app)
    return my_app

app=init_app()
from backend.controllers import *




if __name__=="__main__":
    db.create_all()
    app.run(debug=True)