from cryptic import MicroService
import uuid
import random
import string


class Wallet:
    """
    This is the wallet for the Cryptic currency for services like send, receive or get the balance of morph coins
    """
    # balance of the wallet
    amount = 0
    # if the wallet has not been created the key is not activated
    key = 'not activated'

    # identifier is the uuid of the wallet
    def __init__(self, identifier):
        self.identifier = identifier

    # personal key for sending or receive morph coins
    def get_key(self):
        return self.key

    # sets a personal key when wallet has been created
    def set_key(self, key):
        self.key = key

    # for checking the amount of morph coins
    def get_balance(self):
        return self.amount

    # creates the wallet with creating a personal key
    def create_wallet(self):
        # generate a personal key and set it for the wallet
        # key contains ascii letters and digits and is 10 chars long
        self.set_key(''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)]))
        return 'Your wallet has been created. This is your personal key: ' + self.get_key()

    def send_coins(self, key, destination, send_amount):
        # if no random key was generated and the key is still not activated the user will not send coins
        if self.get_key() == 'not activated':
            return 'You have to create a wallet before sending morph coins!'
        # if the pasted key is not the valid key no transfer will be confirmed
        if str(key) != str(self.get_key()):
            return 'Transfer failed! You key is not valid.'
        # if the wanted amount to send is higher than the current balance it will fail to transfer
        if send_amount > self.amount:
            return 'Transfer failed! You have not enough morph coins.'
        # the balance of the wallet is current amount minus send amount of morph coins
        self.amount -= send_amount
        # successful status mail with transfer information
        return 'Transfer of ' + str(send_amount) + ' from ' + str(self.identifier) +\
               ' to ' + str(destination) + ' successful!'

    def receive_coins(self, source, get_amount):
        # if no wallet has been created it will not be possible to receive points
        if self.get_key() == 'not activated':
            return 'This wallet was not created.'
        # if the wallet is valid the current amount plus the get_amount is the new amount
        self.amount += get_amount
        return str(self.identifier) + ' received ' + str(get_amount) + ' from ' + str(source)


def handle(endpoint, data):
    """
    :param endpoint: action of the server what to do
    :param data: nothing specified
    :return: Response of the wallet for status of requests create, get, send, receive
    """
    # creates an unified unique identifier to identify each wallet, also not activated ones
    unique_id = str(uuid.uuid4())
    # every time the handle method is called, a new wallet object is been created with an uuid
    wallet = Wallet(unique_id)
    # endpoint[0] will be the action what to do in an array ['get', ...]
    if endpoint[0] == 'create':
        wallet_response = wallet.create_wallet()
    elif endpoint[0] == 'get':
        wallet_response = wallet.get_balance()
    elif endpoint[0] == 'send':
        wallet_response = wallet.send_coins('wallet_key', 'destination', 123454321)
    elif endpoint[0] == 'receive':
        wallet_response = wallet.receive_coins('source', 123454321)
    else:
        wallet_response = 'Endpoint is not supported.'
    return {"wallet_response": wallet_response, "data": data}


if __name__ == '__main__':
    m = MicroService('wallet', handle)
    m.run()
