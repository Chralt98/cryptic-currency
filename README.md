# cryptic-currency
### Python Microservice for the community project Cryptic-Currency
##### Explanation of dict keys:
1. **user_uuid** is the unique identifier for a user account in the game.
2. **source_uuid** is the unique identifier for a wallet.
3. **key** is to access the send and get the balance of Morph Coins feature.
4. **send_amount** is the transaction value to send Morph Coins to another wallet or to get a gift.
5. **destination_uuid** is the aim, where to send the Morph Coins. It has to be a source_uuid in the wallet.
6. **usage** is the optional information for a transaction.

* Use Endpoint **'create'** and the following dict format to create a wallet.

    ***input:***

        {"user_uuid": "7da46fff07d247b29e3f158a2d4431fa"}
        
    ***returns:***

        {'wallet_response': {'status': 'Your wallet has been created. ',
         'uuid': '883297366206414abca286f0a8f46f8d',
         'key': '9d57634877'}}

* Endpoint **'get'** is to get the current amount of Morph Coins and a transaction history.
    
    ***input:***
    
        {"source_uuid": "883297366206414abca286f0a8f46f8d",
         "key": "c7eee9d697"}

    ***returns:***
        
        {'wallet_response': {'amount': 100,
         'transactions': [{'time_stamp': '2019-03-25 16:54:10.723790',
                           'source_uuid': '883297366206414abca286f0a8f46f8d',
                           'amount': 3, 'destination_uuid': '5d3046d634c84394bca32e5555b63917', 
                           'usage': 'optional keyword for information about the transaction'}]}}

* Endpoint **'reset'** returns a new wallet key.
    
    ***input:***
    
        {"source_uuid": "883297366206414abca286f0a8f46f8d"}
        
    ***returns:***
    
        {'wallet_response': {'status': 'Your wallet key has been updated.',
                             'uuid': '883297366206414abca286f0a8f46f8d', 
                             'key': 'c7eee9d697'}}

* Endpoint **'send'** is to transfer coins from one wallet to another.
    
    ***input:***
    
        {"source_uuid": "883297366206414abca286f0a8f46f8d", 
         "send_amount": 3, 
         "key": "c7eee9d697", 
         "destination_uuid": "5d3046d634c84394bca32e5555b63917", 
         "usage": "optional keyword for information about the transaction"}
        
    ***returns:***
    
        {'wallet_response': {'status': 'Transfer of 3 morph coins from 883297366206414abca286f0a8f46f8d 
                                        to 5d3046d634c84394bca32e5555b63917 successful!'}}

* Endpoint **'gift'** is to generate Morph Coins.
    
    ***input:***
    
        {"source_uuid": "883297366206414abca286f0a8f46f8d", 
         "send_amount": 999}
        
    ***returns:***
    
        {'wallet_response': {'status': 'Gift of 999 to 883297366206414abca286f0a8f46f8d successful!'}}

* Endpoint **'delete'** is to remove a wallet.

    ***input:***

        {"source_uuid": "883297366206414abca286f0a8f46f8d"}
        
    ***returns:***
    
        {'wallet_response': {'status': 'Deletion of 883297366206414abca286f0a8f46f8d successful.'}}
