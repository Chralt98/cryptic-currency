from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base
from config import config
import sqlalchemy

base = declarative_base()

# "storage location" environment variables
uri = "sqlite:///" + config['STORAGE_LOCATION'] + "wallet.db"
engine = sqlalchemy.create_engine(uri)
base.metadata.bind = engine
Session = orm.sessionmaker(bind=engine)
session = Session()
