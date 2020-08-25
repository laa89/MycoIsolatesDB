import os

from flask import Flask, current_app, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

from MycoIsolatesDB import alchemy
from MycoIsolatesDB.views import (
        contact, induction, isolate, home, plating, survival_assay)


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(SECRET_KEY="dev",
                #DATABASE=os.path.join(app.instance_path, "MycoIsolatesDB.sql"),
                SQLALCHEMY_DATABASE_URI=\
                    "mysql+pymysql://pdm_anon:pdm_anon@localhost/MycoIsolates",
                SQLALCHEMY_TRACK_MODIFICATIONS=False)

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])

    # To be removed upon pdm_utils update
    # -----------------------------------
    alchemy.alchemist.connected = True
    alchemy.alchemist.connected_database = True
    alchemy.alchemist.has_credentials = True
    alchemy.alchemist.has_database = True 
    alchemy.alchemist._engine = engine
    # -----------------------------------


    app.register_blueprint(home.bp)
    app.register_blueprint(isolate.bp) 
    app.register_blueprint(plating.bp)
    app.register_blueprint(survival_assay.bp)
    app.register_blueprint(induction.bp)
    app.register_blueprint(contact.bp)

    return app








