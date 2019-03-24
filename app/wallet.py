from cryptic import MicroService
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base
from config import config
import sqlalchemy
from sqlalchemy import Column, Integer, String
from objects import db

base = declarative_base()

uri = 'mysql://'+config["MYSQL_USERNAME"] + ":" + str(config["MYSQL_PASSWORD"]) + '@' + str(config["MYSQL_HOSTNAME"]) \
      + ":" + str(config["MYSQL_PORT"]) + "/" + str(config["MYSQL_DATABASE"])

engine = sqlalchemy.create_engine(uri)
base.metadata.bind = engine
session = orm.scoped_session(orm.sessionmaker())(bind=engine)
# session = orm.sessionmaker(bind=engine)


class Transaction(base):
    __tablename__: str = "transaction"

    id: db.Column = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time_stamp: db.Column(db.TIMESTAMP)
    source_uuid: db.Column = db.Column(db.String(32), unique=True)
    send_amount: db.Column = db.Column(db.Integer, nullable=False, default=0)
    destination_uuid: db.Column = db.Column(db.String(32), unique=True)
    usage: db.Column = db.Column(db.String(64), default='')

    # auf objekt serialize anwenden und dann kriege ich aus objekt ein dict zurueck
    @property
    def serialize(self) -> dict:
        _ = self.uuid
        return {**self.__dict__}

    @staticmethod
    def create(source_uuid: str, send_amount: int, destination_uuid: str, usage: str) -> 'TransactionModel':
        # create transaction and add it to database
        """
        Returns a transaction of a source_uuid.
        :return: transactions
        """
        # Create a new TransactionModel instance
        transaction: Transaction = Transaction(
            source_uuid=source_uuid,
            send_amount=send_amount,
            destination_uuid=destination_uuid,
            usage=usage
        )

        # Add the new wallet to the db
        db.session.add(transaction)
        db.session.commit()
        return transaction


class Wallet(base):
    __tablename__: str = "wallet"

    time_stamp: db.Column(db.TIMESTAMP)
    source_uuid: db.Column = db.Column(db.String(32), primary_key=True, unique=True)
    key: db.Column = db.Column(db.String(16))
    amount: db.Column = db.Column(db.Integer, nullable=False, default=0)
    user_uuid: db.Column = db.Column(db.String(32), unique=True)

    # auf objekt serialize anwenden und dann kriege ich aus objekt ein dict zurueck
    @property
    def serialize(self) -> dict:
        _ = self.uuid
        return {**self.__dict__}

    @staticmethod
    def create(user_uuid: str) -> dict:
        """
        Creates a new wallet.
        :return: dict with status
        """
        if user_uuid == "":
            return {"error": "You have to paste the user uuid to create a wallet."}

        source_uuid: str = str(uuid4()).replace("-", "")
        # uuid is 32 chars long -> now key is 16 chars long
        key: str = str(uuid4()).replace("-", "")[:16]

        # Create a new Wallet instance
        wallet: Wallet = Wallet(
            source_uuid=source_uuid,
            key=key,
            amount=100,
            user_uuid=user_uuid
        )

        # Add the new wallet to the db
        db.session.add(wallet)
        db.session.commit()
        wallet.query.filter_by(source_uuid=source_uuid).first()
        return {"status": "Your wallet has been created. ", "uuid": source_uuid, "key": key}


def handle(endpoint: list, data: dict) -> dict:
    """
    The handle method to get data from server to know what to do
    :param endpoint: the action of the server 'get', 'create', 'send'
    :param data: source_uuid, key, send_amount, destination_uuid ...
    :return: wallet response for actions
    """
    # test the casting
    try:
        str(data['user_uuid'])
        str(data['source_uuid'])
        str(data['key'])
        int(data['send_amount'])
        str(data['destination_uuid'])
        str(data['usage'])
    except ValueError:
        return {"wallet_response": "Your input data is in a wrong format!", "user_uuid": "str", "source_uuid": "str",
                "key": "str", "send_amount": "int", "destination_uuid": "str",
                "usage": "str", "input_data": data}
    except KeyError:
        pass
    # every time the handle method is called, a new wallet object is created
    wallet: Wallet = Wallet()
    # endpoint[0] will be the action what to do in an array ['get', ...]
    if endpoint[0] == 'create':
        try:
            user_uuid: str = data['user_uuid']
        except KeyError:
            return {"wallet_response": "Key 'user_uuid' have to be set for endpoint create.", "input_data": data}
        wallet_response: dict = wallet.create_wallet(user_uuid)
    elif endpoint[0] == 'get':
        try:
            source_uuid: str = data['source_uuid']
            key: str = data['key']
        except KeyError:
            return {"wallet_response": "Keys 'source_uuid' and 'key' have to be set for endpoint get.",
                    "input_data": data}
        wallet_response: dict = wallet.get_balance(source_uuid, key)
    elif endpoint[0] == 'send':
        try:
            usage: str = data['usage']
        except KeyError:
            usage: str = ''
        try:
            source_uuid: str = data['source_uuid']
            key: str = data['key']
            send_amount: int = data['send_amount']
            destination_uuid: str = data['destination_uuid']
        except KeyError:
            return {"wallet_response": "Keys 'source_uuid' and 'key' and 'send_amount' "
                                       "and 'destination_uuid' have to be set for endpoint send."
                                       "You can also use key 'usage' for specify your transfer.",
                    "input_data": data}
        wallet_response: dict = wallet.send_coins(source_uuid, key, send_amount, destination_uuid, usage)
    elif endpoint[0] == 'reset':
        try:
            source_uuid: str = data['source_uuid']
        except KeyError:
            return {"wallet_response": "Key 'source_uuid' has to be set for the endpoint reset."}
        wallet_response: dict = wallet.reset_wallet_key(source_uuid)
    else:
        wallet_response: dict = {"error": "Endpoint is not supported."}
    return {"wallet_response": wallet_response, "input_data": data}
