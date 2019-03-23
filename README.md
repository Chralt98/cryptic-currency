# cryptic-currency
Python Microservice for the community project Cryptic-Currency

Put the following code after:

    if __name__ == '__main__':

Guide to understand the features of the wallet

user_id has to be set, because to create a wallet you have to have an unique identifier to lock the amount of wallets for each user

-> CREATE A WALLET

    creation_user: dict = {"user_id": ''.join([random.choice(string.ascii_letters + string.digits)
                           for n in range(32)]),
                           "source_uuid": "", "wallet_key": "",
                           "send_amount": 0, "destination_uuid": "", "usage": ""}
    resp: dict = handle(['create'], creation_user)
    print(resp)

-> RESET WALLET KEY
    
    update_user: dict = {"user_id": '',
                         "source_uuid": resp['wallet_response']['uuid'], "wallet_key": "",
                         "send_amount": 0, "destination_uuid": "", "usage": ""}
    resp: dict = handle(['reset'], update_user)

-> SEND COINS FROM ONE WALLET TO ANOTHER

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

-> SHOW THE BALANCE OF WALLET AND TRANSACTIONS

    balance_user: dict = {"user_id": '',
                          "source_uuid": resp['wallet_response']['uuid'], "wallet_key": resp['wallet_response']['key'],
                          "send_amount": 0, "destination_uuid": "", "usage": ""}
    print(handle(['get'], balance_user))

-> GENERATE COINS AND ADD THEM TO A WALLET

    send_gift(12345, balance_user['source_uuid'])
    print(handle(['get'], balance_user))

-> DELETE WALLET

    delete_db_user(balance_user['source_uuid'])

-> PRINT THE FIRST 5 WALLETS ORDERED BY BALANCE IN COMMAND LINE

    print_db()
