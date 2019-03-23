from cryptic import MicroService
import uuid
import random
import string
import sqlite3
import os

"""
   EXAMPLE INPUT TO CREATE WALLET:
   empty_user = {"user_id": ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)]),
                      "source_uuid": "", "wallet_key": "",
                      "send_amount": 0, "destination_uuid": "", "usage": ""}
   wallet_response = handle(['create'], empty_user)

   GET THE CURRENT BALANCE OF WALLET:
   wallet_response = handle(['get'], empty_user)
   print(wallet_response)

   TRANSFER MORPH COINS:
   transfer_user = {"source_uuid": "679ca1a181af4bee887b5ef0a20ea626", "wallet_key": "ONh51aIXje",
       "send_amount": 69, "destination_uuid": "687371ec7f0c472bb0999189e385d1d5"}
   wallet_response = handle(['send'], transfer_user)
   print(wallet_response)

   CREATE MORPH COINS:
   wallet_response = send_gift(1000, "687371ec7f0c472bb0999189e385d1d5")
   print(wallet_response)

   DELETE RECORD/WALLET IN DATABASE:
   delete_db_user("687371ec7f0c472bb0999189e385d1d5")

   PRINT DATABASE:
   print_db()
   
   RESET PASSWORD !!!
"""


def connect_db():
    return sqlite3.connect("wallet.db")


def print_db():
    connection: sqlite3.Connection = connect_db()
    cursor: sqlite3.Cursor = connection.cursor()
    # print the first 5 wallets ordered by balance from database in console
    sql: str = """SELECT * FROM wallet ORDER BY balance DESC LIMIT 5"""
    cursor.execute(sql)
    print("–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––")
    print("------------------------------------------WALLET-DATABASE--------------------------------------------------")
    print("----------------------------------------------CRYPTIC------------------------------------------------------")
    print("-----------------------------------------------------------------------------------------------------------")
    print("------------source_uuid-------------|-wallet_key-|-------------user_id--------------|--------balance-------")
    print("––––––––––––––––––––––––––––––––––––|––––––––––––|–––––––––––––––––––––––––––––––––––––––––––––––––––––––––")
    for record in cursor:
        print("", record[1], record[2], record[4], record[3], sep=" | ")
    print("–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––")
    connection.close()


def get_wallet_count(user_id: str) -> int:
    # connection to wallet database
    connection: sqlite3.Connection = connect_db()
    # create data cursor
    cursor: sqlite3.Cursor = connection.cursor()
    # return count of wallets
    cursor.execute("""SELECT * FROM wallet WHERE user_id=?""", (user_id,))
    wallets: list[tuple: str, str, int, str] = []
    for record in cursor:
        wallets.append(record)
    return len(wallets)


def add_to_database(source_uuid: str, key: str, user_id: str):
    # connection to wallet database
    connection: sqlite3.Connection = connect_db()
    # create data cursor
    cursor: sqlite3.Cursor = connection.cursor()
    # put in database
    cursor.execute("""INSERT INTO wallet (source_uuid, wallet_key, balance, user_id) VALUES (?,?,?,?);"""
                   , (str(source_uuid), str(key), 100, str(user_id)))
    connection.commit()
    connection.close()


def get_db_balance(source_uuid: str, key: str) -> int:
    # connection to wallet database
    connection: sqlite3.Connection = connect_db()
    # create data cursor
    cursor: sqlite3.Cursor = connection.cursor()
    # Selection with strings
    cursor.execute("""SELECT balance FROM wallet WHERE source_uuid=? AND wallet_key=?""", (str(source_uuid), str(key)))
    balances: list[tuple: int] = []
    for record in cursor:
        balances.append(record[0])
    connection.close()
    return balances[0]


def get_db_transactions(source_uuid: str) -> list:
    # connection to the transactions database
    connection: sqlite3.Connection = connect_db()
    # create data cursor
    cursor: sqlite3.Cursor = connection.cursor()
    cursor.execute("""SELECT time_stamp, source_uuid, amount, destination_uuid, usage
                FROM transactions WHERE source_uuid=? OR destination_uuid=?""", (str(source_uuid), str(source_uuid)))
    # one element in list -> list with dicts
    transactions: list = []
    for record in cursor:
        transactions.append({"time_stamp": str(record[0]), "source_uuid": str(record[1]), "amount": record[2],
                            "destination_uuid": str(record[3]), "usage": str(record[4])})
    return transactions


def update_database(source_uuid: str, key: str, send_amount: int, destination_uuid: str, usage: str):
    # connection to wallet database
    connection: sqlite3.Connection = connect_db()
    # create data cursor
    cursor: sqlite3.Cursor = connection.cursor()
    cursor.execute("""INSERT INTO transactions (source_uuid, amount, destination_uuid, usage) VALUES (?,?,?,?);"""
                   , (str(source_uuid), send_amount, str(destination_uuid), str(usage)))
    connection.commit()
    balance_source: int = get_db_balance(source_uuid, key)
    # refresh record
    cursor.execute("""UPDATE wallet SET balance=? WHERE source_uuid=?"""
                   , (balance_source - send_amount, str(source_uuid)))
    connection.commit()
    cursor.execute("""SELECT balance FROM wallet WHERE source_uuid=?""", (str(destination_uuid),))
    balances: list = []
    for record in cursor:
        balances.append(record[0])
    balance_destination: int = balances[0]
    cursor.execute("""UPDATE wallet SET balance=? WHERE source_uuid=?"""
                   , (balance_destination + send_amount, str(destination_uuid)))
    connection.commit()
    connection.close()


def reset_db_user_key(source_uuid: str, key: str):
    # update password in database
    connection: sqlite3.Connection = connect_db()
    cursor: sqlite3.Cursor = connection.cursor()
    cursor.execute("""UPDATE wallet SET wallet_key=? WHERE source_uuid=?""", (str(key), str(source_uuid)))
    connection.commit()
    connection.close()


def delete_db_user(source_uuid: str):
    # connection to wallet database
    connection: sqlite3.Connection = connect_db()
    # create data cursor
    cursor: sqlite3.Cursor = connection.cursor()
    cursor.execute("""DELETE FROM wallet WHERE source_uuid=?""", (str(source_uuid),))
    connection.commit()
    connection.close()


def auth_db_user(source_uuid: str, key: str) -> bool:
    # connection to wallet database
    connection: sqlite3.Connection = connect_db()
    # create data cursor
    cursor: sqlite3.Cursor = connection.cursor()
    cursor.execute("""SELECT * FROM wallet WHERE source_uuid=? AND wallet_key=?""", (str(source_uuid), str(key)))
    wallets: list = []
    for record in cursor:
        wallets.append(record)
    connection.close()
    if len(wallets) > 0:
        return True
    else:
        return False


def destination_exists(destination_uuid: str) -> bool:
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM wallet WHERE source_uuid=?""", (str(destination_uuid),))
    wallets: list = []
    for record in cursor:
        wallets.append(record)
    connection.close()
    if len(wallets) > 0:
        return True
    else:
        return False


def send_gift(send_amount: int, destination_uuid: str) -> dict:
    # connection to wallet database
    connection: sqlite3.Connection = connect_db()
    # create data cursor
    cursor: sqlite3.Cursor = connection.cursor()
    cursor.execute("""SELECT balance FROM wallet WHERE source_uuid=?""", (str(destination_uuid),))
    balances: list = []
    for record in cursor:
        balances.append(record[0])
    balance_destination: int = balances[0]
    cursor.execute("""UPDATE wallet SET balance=? WHERE source_uuid=?"""
                   , (balance_destination + send_amount, str(destination_uuid)))
    connection.commit()
    connection.close()
    return {"status": "Gift of " + str(send_amount) + " to " + str(destination_uuid) + " successful!"}


class Wallet:
    """
    This is the wallet for the Cryptic currency for services like send, receive or get the balance of morph coins
    """
    # balance of the wallet
    amount: int = 0
    # if the wallet has not been created the key is not activated
    key: str = 'not activated'
    # identifier is the uuid of the wallet
    source_uuid: str = 'not activated'

    # personal key for sending or receive morph coins
    def get_key(self) -> str:
        return self.key

    # sets a personal key when wallet has been created
    def set_key(self, key: str):
        self.key = key

    def set_source_uuid(self, source_uuid: str):
        self.source_uuid = source_uuid

    def get_source_uuid(self) -> str:
        return self.source_uuid

    def set_amount(self, amount: int):
        self.amount = amount

    def get_amount(self) -> int:
        return self.amount

    # for checking the amount of morph coins
    def get_balance(self, source_uuid: str, key: str) -> dict:
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
        return {"balance": get_db_balance(source_uuid, key), "transactions": get_db_transactions(source_uuid)}

    # creates the wallet with creating a personal key and a uuid
    def create_wallet(self, user_id: str) -> dict:
        if user_id == "":
            return {"status": "You have to paste the user uuid to create a wallet."}
        # check if user got already a wallet
        if get_wallet_count(user_id) > 0:
            return {"error": "You have already got a wallet!"}
        # creates an unified unique identifier to identify each wallet
        self.set_source_uuid(str(uuid.uuid4()).replace("-", ""))
        # generate a personal key and set it for the wallet
        # key contains ascii letters and digits and is 10 chars long
        self.set_key(''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)]))
        # put the information in the sqlite3 database
        add_to_database(self.get_source_uuid(), self.get_key(), user_id)
        return {"status": "Your wallet has been created. ", "uuid": str(self.get_source_uuid()),
                "key": str(self.get_key())}

    # resets password in database
    def reset_wallet_key(self, source_uuid: str) -> dict:
        if source_uuid == "":
            return {"error": "Source UUID is empty."}
        if not destination_exists(source_uuid):
            return {"error": "Source UUID does not exist."}
        # key contains ascii letters and digits and is 10 chars long
        self.set_key(''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)]))
        self.set_source_uuid(source_uuid)
        reset_db_user_key(source_uuid, self.get_key())
        return {"status": "Your wallet key has been updated.", "uuid": str(source_uuid), "key": str(self.get_key())}

    def send_coins(self, source_uuid: str, key: str, send_amount: int, destination_uuid: str, usage: str = "") -> dict:
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
        update_database(source_uuid, key, send_amount, destination_uuid, usage)
        # successful status mail with transfer information
        return {"status": "Transfer of " + str(send_amount) + " morph coins from " + str(source_uuid) +
                          " to " + str(destination_uuid) + " successful!"}


def handle(endpoint: list, data: dict) -> dict:
    """
    The handle method to get data from server to know what to do
    :param endpoint: the action of the server 'get', 'create', 'send'
    :param data: source_uuid, wallet_key, send_amount, destination_uuid
    :return: wallet response for actions
    """
    # test the casting
    try:
        str(data['user_id'])
        str(data['source_uuid'])
        str(data['wallet_key'])
        int(data['send_amount'])
        str(data['destination_uuid'])
        str(data['usage'])
    except ValueError:
        return {"wallet_response": "Your input data is in a wrong format!", "user_id": "str", "source_uuid": "str",
                "wallet_key": "str", "send_amount": "int", "destination_uuid": "str",
                "usage": "str", "input_data": data}
    except KeyError:
        pass
    # every time the handle method is called, a new wallet object is created
    wallet: Wallet = Wallet()
    # endpoint[0] will be the action what to do in an array ['get', ...]
    if endpoint[0] == 'create':
        try:
            user_id: str = data['user_id']
        except KeyError:
            return {"wallet_response": "Key 'user_id' have to be set for endpoint create.", "input_data": data}
        wallet_response: dict = wallet.create_wallet(user_id)
    elif endpoint[0] == 'get':
        try:
            source_uuid: str = data['source_uuid']
            wallet_key: str = data['wallet_key']
        except KeyError:
            return {"wallet_response": "Keys 'source_uuid' and 'wallet_key' have to be set for endpoint get.",
                    "input_data": data}
        wallet_response: dict = wallet.get_balance(source_uuid, wallet_key)
    elif endpoint[0] == 'send':
        try:
            usage: str = data['usage']
        except KeyError:
            usage: str = ''
        try:
            source_uuid: str = data['source_uuid']
            wallet_key: str = data['wallet_key']
            send_amount: int = data['send_amount']
            destination_uuid: str = data['destination_uuid']
        except KeyError:
            return {"wallet_response": "Keys 'source_uuid' and 'wallet_key' and 'send_amount' "
                                       "and 'destination_uuid' have to be set for endpoint send."
                                       "You can also use key 'usage' for specify your transfer.",
                    "input_data": data}
        wallet_response: dict = wallet.send_coins(source_uuid, wallet_key, send_amount, destination_uuid, usage)
    elif endpoint[0] == 'reset':
        try:
            source_uuid: str = data['source_uuid']
        except KeyError:
            return {"wallet_response": "Key 'source_uuid' has to be set for the endpoint reset."}
        wallet_response: dict = wallet.reset_wallet_key(source_uuid)
    else:
        wallet_response: dict = {"error": "Endpoint is not supported."}
    return {"wallet_response": wallet_response, "input_data": data}


if __name__ == '__main__':
    if not os.path.exists("wallet.db"):
        # connection to database
        connect: sqlite3.Connection = sqlite3.connect("wallet.db")
        # create data cursor
        curs: sqlite3.Cursor = connect.cursor()
        # create table
        sql1: str = "CREATE TABLE wallet(" \
                    "release_time DATETIME DEFAULT CURRENT_TIMESTAMP," \
                    "source_uuid TEXT PRIMARY KEY, " \
                    "wallet_key TEXT, " \
                    "balance INTEGER, " \
                    "user_id TEXT); "
        # execute the sql
        curs.execute(sql1)
        sql2: str = "CREATE TABLE transactions(" \
                    "id INTEGER PRIMARY KEY AUTOINCREMENT," \
                    "time_stamp DATETIME DEFAULT CURRENT_TIMESTAMP," \
                    "source_uuid TEXT," \
                    "amount INTEGER," \
                    "destination_uuid TEXT," \
                    "usage TEXT); "
        curs.execute(sql2)
        connect.close()
        # TODO: Creates a superuser, when the database is created
        sudo: Wallet = Wallet()
        sudo_wallet: dict = sudo.create_wallet("7da46fff07d247b29e3f158a2d4431fa")
        sudo_uuid: str = sudo_wallet['uuid']
        sudo_key: str = sudo_wallet['key']
        send_gift(99999999999999, sudo_uuid)

    # TODO: Guide to understand the features of the wallet
    # user_id has to be set, because to create a wallet you have to have an unique
    # identifier to lock the amount of wallets for each user
    # -> CREATE A WALLET
    creation_user: dict = {"user_id": ''.join([random.choice(string.ascii_letters + string.digits)
                           for n in range(32)]),
                           "source_uuid": "", "wallet_key": "",
                           "send_amount": 0, "destination_uuid": "", "usage": ""}
    resp: dict = handle(['create'], creation_user)
    print(resp)

    # -> RESET WALLET KEY
    update_user: dict = {"user_id": '',
                         "source_uuid": resp['wallet_response']['uuid'], "wallet_key": "",
                         "send_amount": 0, "destination_uuid": "", "usage": ""}
    resp: dict = handle(['reset'], update_user)

    # -> SEND COINS FROM ONE WALLET TO ANOTHER
    destination_user: dict = {"user_id": ''.join([random.choice(string.ascii_letters + string.digits)
                              for n in range(32)]),
                              "source_uuid": resp['wallet_response']['uuid'],
                              "wallet_key": resp['wallet_response']['key'],
                              "send_amount": 0, "destination_uuid": "", "usage": ""}
    resp2: dict = handle(['create'], destination_user)
    destination_user_uuid: str = resp2['wallet_response']['uuid']
    destination_user_key: str = resp2['wallet_response']['key']

    send_user: dict = {"user_id": '',
                       "source_uuid": resp['wallet_response']['uuid'], "wallet_key": resp['wallet_response']['key'],
                       "send_amount": 11, "destination_uuid": str(destination_user_uuid), "usage": "A cool product"}
    print(handle(['send'], send_user))

    # -> SHOW THE BALANCE OF WALLET AND TRANSACTIONS
    balance_user: dict = {"user_id": '',
                          "source_uuid": resp['wallet_response']['uuid'], "wallet_key": resp['wallet_response']['key'],
                          "send_amount": 0, "destination_uuid": "", "usage": ""}
    print(handle(['get'], balance_user))

    # -> GENERATE COINS AND ADD THEM TO A WALLET
    send_gift(12345, balance_user['source_uuid'])
    print(handle(['get'], balance_user))

    # -> DELETE WALLET
    delete_db_user(balance_user['source_uuid'])

    # -> PRINT THE FIRST 5 WALLETS ORDERED BY BALANCE IN COMMAND LINE
    print_db()

    # m = MicroService('wallet', handle)
    # m.run()
