from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path
from datetime import datetime
import subprocess
from os import environ

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.update(
        MAIL_SERVER=environ["MAIL_SERVER"],
        MAIL_USERNAME=environ["MAIL_USERNAME"],
        MAIL_PASSWORD=environ["MAIL_PASSWORD"],
        MAIL_PORT=environ["MAIL_PORT"],
        MAIL_USE_SSL=environ["MAIL_USE_SSL"],
        MAIL_USE_TSL=environ["MAIL_USE_TSL"],
        DB_NAME=environ["DB_NAME"],
        SECRET_KEY=environ["SECRET_KEY"],
        SQLALCHEMY_DATABASE_URI=environ["SQLALCHEMY_DATABASE_URI"],
        SQLALCHEMY_TRACK_MODIFICATIONS=environ["SQLALCHEMY_TRACK_MODIFICATIONS"],
        ACCOUNT_EXPIRE_VERIFY_TIME=environ["ACCOUNT_EXPIRE_VERIFY_TIME"],
        ADMIN_EMAIL=environ["ADMIN_EMAIL"],
        ADMIN_PASS=environ["ADMIN_PASS"],
    )

    db.init_app(app)

    from .view import view
    from .auth import auth

    app.register_blueprint(view, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    init_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from .models import ApptUsers

    @login_manager.user_loader
    def load_user(id):
        return ApptUsers.query.get(int(id))

    return app


def create_database(dbpath):
    subprocess.call(["sqlite3", dbpath, ".read initdb.sql"])
    return


def init_database(app):
    from .models import UserLevel
    from .models import ApptUsers

    with app.app_context():
        if len(UserLevel.query.all()) == 0:
            userlevels = []
            userlevels.append(UserLevel(ulevel=1, uname="Admin"))
            userlevels.append(UserLevel(ulevel=2, uname="Manager"))
            userlevels.append(UserLevel(ulevel=3, uname="Employee"))
            strptime = datetime.strptime
            try:
                for userlevel in userlevels:
                    db.session.add(userlevel)
                db.session.commit()
            except Exception as e:
                raise (e)

        if len(ApptUsers.query.all()) == 0:
            # create admin user if exists
            email = app.config.get("ADMIN_EMAIL")
            passwd = app.config.get("ADMIN_PASS")
            if email != "" and passwd != "":
                from werkzeug.security import generate_password_hash

                admin = ApptUsers(
                    userlevelid=1,
                    email=email,
                    upassword=generate_password_hash(passwd, "sha256"),
                    uname="admin",
                    verified=True,
                )
                try:
                    ApptUsers.query.delete()
                    db.session.commit()

                    db.session.add(admin)
                    db.session.commit()
                except Exception as e:
                    print(e)
                    print("adding admin account failed")
