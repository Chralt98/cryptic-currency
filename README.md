# cryptic-currency
Python Microservice for Cryptic

   SQLite3 database structure:
   """TABLE wallet(source_uuid TEXT PRIMARY KEY, wallet_key TEXT, balance REAL)"""
  
   EXAMPLE INPUT TO CREATE WALLET:
   empty_user = {"source_uuid": "", "wallet_key": "", "send_amount": 0, "destination_uuid": ""}
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
