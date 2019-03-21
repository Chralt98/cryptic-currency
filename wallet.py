from cryptic import MicroService
import uuid
import random
import string
import sqlite3
import os
import sys


class Wallet:
    """
    This is the wallet for the Cryptic currency for services like send, receive or get the balance of morph coins
    """
    # balance of the wallet
    amount = 0
    # if the wallet has not been created the key is not activated
    key = 'not activated'
    # identifier is the uuid of the wallet
    identifier = 'not activated'

    # personal key for sending or receive morph coins
    def get_key(self):
        return self.key

    # sets a personal key when wallet has been created
    def set_key(self, key):
        self.key = key

    def set_identifier(self, identifier):
        self.identifier = identifier

    def get_identifier(self):
        return self.identifier

    # for checking the amount of morph coins
    def get_balance(self, user_name, key):
        # TODO: Get the amount out of the database
        # no valid key -> no status of balance
        if self.get_key() == 'not activated':
            return {"error": "You have to create a wallet before sending morph coins!"}
        return {"balance": self.amount}

    # creates the wallet with creating a personal key and a uuid
    def create_wallet(self, user_name):
        # creates an unified unique identifier to identify each wallet
        self.set_identifier(str(uuid.uuid4()))
        # generate a personal key and set it for the wallet
        # key contains ascii letters and digits and is 10 chars long
        self.set_key(''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)]))
        # TODO: put the information in the sqlite3 database
        return {"status": str(user_name) + " , your wallet has been created. ", "uuid": str(self.get_identifier()),
                "key": str(self.get_key())}

    def send_coins(self, user_name, key, destination, send_amount):
        # TODO: Check the user name and key in the sqlite3 database
        # if no random key was generated and the key is still not activated the user will not send coins
        if self.get_key() == 'not activated':
            return {"error": "You have to create a wallet before sending morph coins!"}
        # if the pasted key is not the valid key no transfer will be confirmed
        if str(key) != str(self.get_key()):
            return {"error": "Transfer failed! You key is not valid."}
        # if the wanted amount to send is higher than the current balance it will fail to transfer
        if send_amount > self.amount:
            return {"error": 'Transfer failed! You have not enough morph coins.'}
        # TODO: Update the amount in the database
        # the balance of the wallet is current amount minus send amount of morph coins
        self.amount -= send_amount
        # successful status mail with transfer information
        return {"status": "Transfer of " + str(send_amount) + " from " + str(self.identifier) +
                          " to " + str(destination) + " successful!"}

    def receive_coins(self, source, get_amount):
        # if no wallet has been created it will not be possible to receive points
        if self.get_key() == 'not activated':
            return {"error": "This wallet was not created."}
        # TODO: Update the amount in the database
        # if the wallet is valid the current amount plus the get_amount is the new amount
        self.amount += get_amount
        return {"status": str(self.get_identifier()) + " received " + str(get_amount) + " from " + str(source)}


def handle(endpoint, data):
    """
    :param endpoint: action of the server what to do
    :param data: nothing specified
    :return: Response of the wallet for status of requests create, get, send, receive
    """
    user_name = ""
    wallet_key = ""
    source = ""
    destination = ""
    get_amount = 0
    send_amount = 0

    data['user_name'] = user_name
    data['wallet_key'] = wallet_key
    data['source'] = source
    data['destination'] = destination
    data['get_amount'] = get_amount
    data['send_amount'] = send_amount
    # every time the handle method is called, a new wallet object is created
    wallet = Wallet()
    # endpoint[0] will be the action what to do in an array ['get', ...]
    if endpoint[0] == 'create':
        wallet_response = wallet.create_wallet(user_name)
    elif endpoint[0] == 'get':
        wallet_response = wallet.get_balance(user_name, wallet_key)
    elif endpoint[0] == 'send':
        wallet_response = wallet.send_coins(user_name, wallet_key, destination, send_amount)
    elif endpoint[0] == 'receive':
        wallet_response = wallet.receive_coins(source, get_amount)
    else:
        wallet_response = 'Endpoint is not supported.'
    return {"wallet_response": wallet_response, "input_data": data}


if __name__ == '__main__':
    """
    # connection to database
    connection = sqlite3.connect("wallet.db")

    # create data cursor
    cursor = connection.cursor()

    # create table
    sql = "CREATE TABLE wallet(" \
          "id INTEGER PRIMARY KEY, " \
          "user_name TEXT, " \
          "wallet_key TEXT, " \
          "uuid TEXT, " \
          "balance REAL) "
    
    # execute the sql
    cursor.execute(sql)
    """
    m = MicroService('wallet', handle)
    m.run()
