from cryptic import MicroService
import uuid
import random
import string
import sqlite3

"""
Database structure:

sql = "CREATE TABLE wallet(" \
  "source_uuid TEXT PRIMARY KEY, " \
  "wallet_key TEXT, " \
  "balance REAL) "
"""


def connect_db():
    return sqlite3.connect("wallet.db")


def print_db():
    connection = connect_db()
    cursor = connection.cursor()
    # print the complete database in console
    sql = """SELECT * FROM wallet"""
    cursor.execute(sql)
    print("--------------------------------------------------------")
    print("-------------------WALLET-DATABASE----------------------")
    print("----------------------CRYPTIC---------------------------")
    print("-----source_uuid------------------|-wallet_key-|-balance")
    for record in cursor:
        print(record[0], record[1], record[2], sep=" | ")
    print("--------------------------------------------------------")
    connection.close()


def add_to_database(source_uuid, key):
    # connection to wallet database
    connection = connect_db()
    # create data cursor
    cursor = connection.cursor()
    # put in database
    cursor.execute("""INSERT INTO wallet (source_uuid, wallet_key, balance) VALUES (?,?,?);"""
                   , (str(source_uuid), str(key), 0))
    connection.commit()
    connection.close()


def get_db_balance(source_uuid, key):
    # connection to wallet database
    connection = connect_db()
    # create data cursor
    cursor = connection.cursor()
    # Selection with strings
    cursor.execute("""SELECT balance FROM wallet WHERE source_uuid=? AND wallet_key=?""", (str(source_uuid), str(key)))
    balances = []
    for record in cursor:
        balances.append(record[0])
    connection.close()
    return balances[0]


def update_database(source_uuid, key, send_amount, destination_uuid):
    # connection to wallet database
    connection = connect_db()
    # create data cursor
    cursor = connection.cursor()
    balance_source = get_db_balance(source_uuid, key)
    # refresh record
    cursor.execute("""UPDATE wallet SET balance=? WHERE source_uuid=?"""
                   , (balance_source - send_amount, str(source_uuid)))
    connection.commit()
    cursor.execute("""SELECT balance FROM wallet WHERE source_uuid=?""", (str(destination_uuid),))
    balances = []
    for record in cursor:
        balances.append(record[0])
    balance_destination = balances[0]
    cursor.execute("""UPDATE wallet SET balance=? WHERE source_uuid=?"""
                   , (balance_destination + send_amount, str(destination_uuid)))
    connection.commit()
    connection.close()


def auth_db_user(source_uuid, key):
    # connection to wallet database
    connection = connect_db()
    # create data cursor
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM wallet WHERE source_uuid=? AND wallet_key=?""", (str(source_uuid), str(key)))
    wallets = []
    for record in cursor:
        wallets.append(record)
    connection.close()
    if len(wallets) > 0:
        return True
    else:
        return False


def destination_exists(destination_uuid):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM wallet WHERE source_uuid=?""", (str(destination_uuid),))
    wallets = []
    for record in cursor:
        wallets.append(record)
    connection.close()
    if len(wallets) > 0:
        return True
    else:
        return False


def send_gift(send_amount, destination_uuid):
    # connection to wallet database
    connection = connect_db()
    # create data cursor
    cursor = connection.cursor()
    # refresh record
    cursor.execute("""UPDATE wallet SET balance=? WHERE source_uuid=?"""
                   , (send_amount, str(destination_uuid)))
    connection.commit()
    connection.close()
    return {"status": "Gift of " + str(send_amount) + " to " + str(destination_uuid) + " successful!"}


class Wallet:
    """
    This is the wallet for the Cryptic currency for services like send, receive or get the balance of morph coins
    """
    # balance of the wallet
    amount = 0
    # if the wallet has not been created the key is not activated
    key = 'not activated'
    # identifier is the uuid of the wallet
    source_uuid = 'not activated'

    # personal key for sending or receive morph coins
    def get_key(self):
        return self.key

    # sets a personal key when wallet has been created
    def set_key(self, key):
        self.key = key

    def set_source_uuid(self, source_uuid):
        self.source_uuid = source_uuid

    def get_source_uuid(self):
        return self.source_uuid

    def set_amount(self, amount):
        self.amount = amount

    def get_amount(self):
        return self.amount

    # for checking the amount of morph coins
    def get_balance(self, source_uuid, key):
        if source_uuid == "":
            return {"error": "Source UUID is empty."}
        if key == "":
            return {"error": "Key is empty."}
        # no valid key -> no status of balance
        if not auth_db_user(source_uuid, key):
            return {"error": "Your UUID or wallet key is wrong or you have to create an account."}
        # user is now authentified -> set amount uuid and key in the class
        self.set_amount(get_db_balance(source_uuid, key))
        self.set_source_uuid(source_uuid)
        self.set_key(key)
        return {"balance": get_db_balance(source_uuid, key)}

    # creates the wallet with creating a personal key and a uuid
    def create_wallet(self):
        # creates an unified unique identifier to identify each wallet
        self.set_source_uuid(str(uuid.uuid4()))
        # generate a personal key and set it for the wallet
        # key contains ascii letters and digits and is 10 chars long
        self.set_key(''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)]))
        # put the information in the sqlite3 database
        add_to_database(self.get_source_uuid(), self.get_key())
        return {"status": "Your wallet has been created. ", "uuid": str(self.get_source_uuid()),
                "key": str(self.get_key())}

    def send_coins(self, source_uuid, key, send_amount, destination_uuid):
        if source_uuid == "":
            return {"error": "Source UUID is empty."}
        if key == "":
            return {"error": "Key is empty."}
        # if no random key was generated and the key is still not activated the user will not send coins
        if not auth_db_user(source_uuid, key):
            return {"error": "Your UUID or wallet key is wrong or "
                             "you have to create a wallet before sending morph coins!"}
        # user is now authentified -> set amount uuid and key in the class
        self.set_amount(get_db_balance(source_uuid, key))
        self.set_source_uuid(source_uuid)
        self.set_key(key)
        # if the pasted key is not the valid key no transfer will be confirmed
        if destination_uuid == "":
            return {"error": "Destination not specified."}
        if not destination_exists(destination_uuid):
            return {"error": "Destination does not exist."}
        if send_amount <= 0:
            return {"error": "You can only send more than 0 morph coins."}
        # if the wanted amount to send is higher than the current balance it will fail to transfer
        if send_amount > self.get_amount():
            return {"error": "Transfer failed! You have not enough morph coins."}
        update_database(source_uuid, key, send_amount, destination_uuid)
        # successful status mail with transfer information
        return {"status": "Transfer of " + str(send_amount) + " morph coins from " + str(source_uuid) +
                          " to " + str(destination_uuid) + " successful!"}


def handle(endpoint, data):
    """
    :param endpoint: action of the server what to do
    :param data: nothing specified
    :return: Response of the wallet for status of requests create, get, send, receive
    """

    source_uuid = data['source_uuid']
    wallet_key = data['wallet_key']
    send_amount = data['send_amount']
    destination_uuid = data['destination_uuid']

    # every time the handle method is called, a new wallet object is created
    wallet = Wallet()
    # endpoint[0] will be the action what to do in an array ['get', ...]
    if endpoint[0] == 'create':
        wallet_response = wallet.create_wallet()
    elif endpoint[0] == 'get':
        wallet_response = wallet.get_balance(source_uuid, wallet_key)
    elif endpoint[0] == 'send':
        wallet_response = wallet.send_coins(source_uuid, wallet_key, send_amount, destination_uuid)
    else:
        wallet_response = 'Endpoint is not supported.'
    return {"wallet_response": wallet_response, "input_data": data}


if __name__ == '__main__':
    """
    EXAMPLE:
    1. Create a wallet.db database
    
    # connection to database
    connection = sqlite3.connect("wallet.db")
    # create data cursor
    cursor = connection.cursor()
    # create table
    sql = "CREATE TABLE wallet(" \
          "source_uuid TEXT PRIMARY KEY, " \
          "wallet_key TEXT, " \
          "balance REAL) "
    # execute the sql
    cursor.execute(sql)
    connection.close()
    
    2. Transfer 10 morph coins to the other user
    
    # guest user0
    user0 = {"source_uuid": "qwertzu", "wallet_key": "123456", "send_amount": 999, "destination_uuid": "asdfgh"}
    user1 = {"source_uuid": "d86718bd-a8ad-4ae8-add7-a69fc922bfec", "wallet_key": "dGEbQgxsXe", "send_amount": 10,
             "destination_uuid": "fd5b42c5-e949-4657-87af-bcdea321ead3"}
    user2 = {"source_uuid": "fd5b42c5-e949-4657-87af-bcdea321ead3", "wallet_key": "FzKdwQIy4j", "send_amount": 50,
             "destination_uuid": "iomlk"}
    # print(send_gift(1000, "d86718bd-a8ad-4ae8-add7-a69fc922bfec"))
    print_db()
    print(handle(['send'], user1))
    # m = MicroService('wallet', handle)
    # m.run()
    """
    m = MicroService('wallet', handle)
    m.run()
