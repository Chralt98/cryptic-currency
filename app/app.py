from cryptic import MicroService
from resources.handle import handle, handle_ms
from uuid import uuid4

if __name__ == '__main__':
    response1 = handle(['create'], {"user_uuid": str(uuid4()).replace("-", "")})
    print(response1)
    response2 = handle(['reset'], {"source_uuid": response1['wallet_response']['uuid']})
    print(response2)
    print(handle(['get'], {"source_uuid": response2['wallet_response']['uuid'],
                           "key": response2['wallet_response']['key']}))
    response3 = handle(['create'], {"user_uuid": str(uuid4()).replace("-", "")})
    print(response3)
    response4 = handle(['send'], {"source_uuid": response1['wallet_response']['uuid'],
                                  "send_amount": 3, "key": response2['wallet_response']['key'],
                                  "destination_uuid": response3['wallet_response']['uuid'],
                                  "usage": "hallo bro du bist cool"})
    print(response4)
    print(handle(['get'], {"source_uuid": response2['wallet_response']['uuid'],
                           "key": response2['wallet_response']['key']}))
    print(handle(['gift'], {"source_uuid": response2['wallet_response']['uuid'], "send_amount": 999}))
    response5 = handle(['send'], {"source_uuid": response2['wallet_response']['uuid'],
                                  "send_amount": 77, "key": response3['wallet_response']['key'],
                                  "destination_uuid": response3['wallet_response']['uuid'],
                                  "usage": "Hacking coins"})
    print(response5)
    print(handle(['delete'], {"source_uuid": response2['wallet_response']['uuid']}))
    # m: MicroService = MicroService('wallet', handle, handle_ms)
    # m.run()
