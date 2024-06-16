from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

engine = create_engine("sqlite:///lib/data.db")
Session = sessionmaker(bind=engine)
session = Session()

def clear():
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('nt')
