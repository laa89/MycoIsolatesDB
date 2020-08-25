import re

from flask import current_app, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

from pdm_utils import AlchemyHandler, Filter

alchemist = AlchemyHandler()

def build_filter():
    db_filter = Filter(alchemist=alchemist)
    return db_filter

def isolate_sorting(isolate):
    isolate_name = isolate.IsolateID
    isolate_number = extract_isolate_number(isolate_name)
    return isolate_number

def extract_isolate_number(isolate_name):
    isolate_number = -1
    
    isolate_format = re.compile("GD(\d+)\D*")
    
    if not re.match(isolate_format, isolate_name) is None:
        isolate_name_split = re.split(isolate_format, isolate_name)
        isolate_number = int(isolate_name_split[1])

    return isolate_number
