from cryptic import MicroService
from uuid import uuid4
import objects_init as db
from sqlalchemy import Column, Integer, String, DateTime, TIMESTAMP, exists, and_
import datetime


class Transaction(db.base):
    __tablename__: str = "transaction"

    id: Column = Column(Integer, primary_key=True, autoincrement=True)
    time_stamp: Column(TIMESTAMP)
    # time_stamp: Column('last_updated', DateTime, onupdate=datetime.datetime.now) as evt. alternative
    source_uuid: Column = Column(String(32), unique=True)
    send_amount: Column = Column(Integer, nullable=False, default=0)
    destination_uuid: Column = Column(String(32), unique=True)
    usage: Column = Column(String(64), default='')

    # auf objekt serialize anwenden und dann kriege ich aus objekt ein dict zurueck
    @property
    def serialize(self) -> dict:
        _ = self.id
        return {**self.__dict__}

    @staticmethod
    def create(source_uuid: str, send_amount: int, destination_uuid: str, usage: str) -> 'Transaction':
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


class Wallet(db.base):
    __tablename__: str = "wallet"

    time_stamp: Column = Column(DateTime, nullable=False)
    source_uuid: Column = Column(String(32), primary_key=True, unique=True)
    key: Column = Column(String(16))
    amount: Column = Column(Integer, nullable=False, default=0)
    user_uuid: Column = Column(String(32), unique=True)

    # auf objekt serialize anwenden und dann kriege ich aus objekt ein dict zurueck
    @property
    def serialize(self) -> dict:
        _ = self.source_uuid
        return {**self.__dict__}

    def create(self, user_uuid: str) -> dict:
        """
        Creates a new wallet.
        :return: dict with status
        """
        # empty user uuid
        if user_uuid == "":
            return {"error": "You have to paste the user uuid to create a wallet."}

        source_uuid: str = str(uuid4()).replace("-", "")
        # uuid is 32 chars long -> now key is 10 chars long
        key: str = str(uuid4()).replace("-", "")[:10]

        # Create a new Wallet instance
        wallet: Wallet = Wallet(
            time_stamp=datetime.datetime.now(),
            source_uuid=source_uuid,
            key=key,
            amount=100,
            user_uuid=user_uuid
        )

        # Add the new wallet to the db
        db.session.add(wallet)
        db.session.commit()
        return {"status": "Your wallet has been created. ", "uuid": str(source_uuid), "key": str(key)}

    # for checking the amount of morph coins and transactions
    def get(self, source_uuid: str, key: str) -> dict:
        if source_uuid == "" or key == "":
            return {"error": "Source UUID or Key is empty."}
        # no valid key -> no status of balance
        if not self.auth_user(source_uuid, key):
            return {"error": "Your UUID or wallet key is wrong or you have to create a wallet."}
        amount: int = db.session.query(Wallet).get(source_uuid).amount
        # transactions = db.session.query(Wallet)
        return {"amount": amount, "transactions": ""}

    def send_coins(self, source_uuid: str, key: str, send_amount: int, destination_uuid: str, usage: str = "") -> dict:
        if source_uuid == "" or key == "":
            return {"error": "Source UUID or Key is empty."}
        # if no random key was generated and the key is still not activated the user will not send coins
        if not self.auth_user(source_uuid, key):
            return {"error": "Your UUID or wallet key is wrong or "
                             "you have to create a wallet before sending morph coins!"}
        if destination_uuid == "":
            return {"error": "Destination UUID is empty."}
        if not db.session.query(exists().where(Wallet.source_uuid == destination_uuid)).scalar():
            return {"error": "Destination does not exist."}
        if send_amount <= 0:
            return {"error": "You can only send more than 0 morph coins."}
        # if the wanted amount to send is higher than the current balance it will fail to transfer
        if send_amount > db.session.query(Wallet).filter(Wallet.source_uuid == source_uuid).first().amount:
            return {"error": "Transfer failed! You have not enough morph coins."}
        # TODO Update in Database
        # TODO insert transaction into table db transactions
        # TODO minus send_amount to source_uuid and plus send_amount to destination_uuid
        # successful status mail with transfer information
        return {"status": "Transfer of " + str(send_amount) + " morph coins from " + str(source_uuid) +
                          " to " + str(destination_uuid) + " successful!"}

    def auth_user(self, source_uuid: str, key: str) -> bool:
        return db.session.query(exists().where(and_(Wallet.source_uuid == source_uuid, Wallet.key == key))).scalar()

    # resets password in database
    def reset(self, source_uuid: str) -> dict:
        if source_uuid == "":
            return {"error": "Source UUID is empty."}
        if not db.session.query(exists().where(Wallet.source_uuid == source_uuid)).scalar():
            return {"error": "Source UUID does not exist."}
        key: str = str(uuid4()).replace("-", "")[:10]
        db.session.query(Wallet).filter(Wallet.source_uuid == source_uuid).update({'key': key})
        db.session.commit()
        return {"status": "Your wallet key has been updated.", "uuid": str(source_uuid), "key": str(key)}

    @staticmethod
    def delete_all_wallets():
        db.session.query(Wallet).delete()
        db.session.commit()

    @staticmethod
    def print_all_wallets():
        print("–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––")
        print("--------------------------------------WALLET-DATABASE--------------------------------------------------")
        print("------------------------------------------CRYPTIC------------------------------------------------------")
        print("-------------------------------------------------------------------------------------------------------")
        print("--------source_uuid--------------|-wallet_key-|-------------user_id--------------|--------amount-------")
        print("–––––––––––––––––––––––––––––––––|––––––––––––|––––––––––––––––––––––––––––––––––––––––––––––––––––––––")
        for user_wallet in db.session.query(Wallet).all():
            print(user_wallet.source_uuid, user_wallet.key, user_wallet.user_uuid, user_wallet.amount, sep=' | ')


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
    db.base.metadata.create_all(bind=db.engine)
    # endpoint[0] will be the action what to do in an array ['get', ...]
    if endpoint[0] == 'create':
        try:
            user_uuid: str = data['user_uuid']
        except KeyError:
            return {"wallet_response": "Key 'user_uuid' have to be set for endpoint create.", "input_data": data}
        wallet_response: dict = wallet.create(user_uuid)
    elif endpoint[0] == 'get':
        try:
            source_uuid: str = data['source_uuid']
            key: str = data['key']
        except KeyError:
            return {"wallet_response": "Keys 'source_uuid' and 'key' have to be set for endpoint get.",
                    "input_data": data}
        wallet_response: dict = wallet.get(source_uuid, key)
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
        wallet_response: dict = wallet.reset(source_uuid)
    else:
        wallet_response: dict = {"error": "Endpoint is not supported."}
    return {"wallet_response": wallet_response, "input_data": data}

# https://docs.sqlalchemy.org/en/latest/orm/tutorial.html explanation


wallet2 = Wallet()
db.base.metadata.create_all(bind=db.engine)
response = wallet2.create(str(uuid4()).replace("-", ""))
print(response)
print(wallet2.print_all_wallets())
response = wallet2.reset('bb1c801288f4494f9c9cb742b3d0b45a')
print(response)
print(wallet2.print_all_wallets())
