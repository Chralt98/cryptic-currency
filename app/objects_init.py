from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base
from config import config
import sqlalchemy

base = declarative_base()

#  uri = 'mysql://'+config["MYSQL_USERNAME"] + ":" + str(config["MYSQL_PASSWORD"]) + '@'
#  + str(config["MYSQL_HOSTNAME"]) \
#       + ":" + str(config["MYSQL_PORT"]) + "/" + str(config["MYSQL_DATABASE"])

uri = 'sqlite:///wallet.db'
engine = sqlalchemy.create_engine(uri)
base.metadata.bind = engine
# session = orm.scoped_session(orm.sessionmaker())(bind=engine)
Session = orm.sessionmaker(bind=engine)
session = Session()
