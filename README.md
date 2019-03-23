# cryptic-currency
Python Microservice for the community project Cryptic-Currency

Put the following code after:

    if __name__ == '__main__':

Example input to create wallet:

    empty_user = {"user_id": ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)]),
                      "source_uuid": "", "wallet_key": "",
                      "send_amount": 0, "destination_uuid": "", "usage": ""}
    wallet_response = handle(['create'], empty_user)

Get the current balance of the wallet and the transaction history:

    wallet_response = handle(['get'], empty_user)
    print(wallet_response)

Transfer morph coins:

    transfer_user = {"source_uuid": "679ca1a181af4bee887b5ef0a20ea626", "wallet_key": "ONh51aIXje",
       "send_amount": 69, "destination_uuid": "687371ec7f0c472bb0999189e385d1d5"}
    wallet_response = handle(['send'], transfer_user)
    print(wallet_response)

Create morph coins:

    wallet_response = send_gift(1000, "687371ec7f0c472bb0999189e385d1d5")
    print(wallet_response)

Delete wallet in database:

    delete_db_user("687371ec7f0c472bb0999189e385d1d5")

Print database:
    
    print_db()
