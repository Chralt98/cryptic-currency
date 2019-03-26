from models.wallet import db, Wallet
from uuid import uuid4


def handle(endpoint: list, data: dict) -> dict:
    """
    The handle method to get data from server to know what to do
    :param endpoint: the action of the server 'get', 'create', 'send'
    :param data: source_uuid, key, send_amount, destination_uuid ...
    :return: wallet response for actions
    """
    db.base.metadata.create_all(bind=db.engine)
    # endpoint[0] will be the action what to do in an array ['get', ...]
    if endpoint[0] == 'create':
        if 'user_uuid' not in data:
            return {"wallet_response": {"error": "Key 'user_uuid' has to be set for endpoint create."}}
        try:
            user_uuid: str = str(data['user_uuid'])
        except ValueError:
            return {"wallet_response": {"error": "Key 'user_uuid' has to be string for endpoint create."}}
        wallet_response: dict = Wallet.create(user_uuid)
    elif endpoint[0] == 'get':
        if 'source_uuid' not in data:
            return {"wallet_response": {"error": "Key 'source_uuid' has to be set for endpoint get."}}
        if 'key' not in data:
            return {"wallet_response": {"error": "Key 'key' has to be set for endpoint get."}}
        try:
            source_uuid: str = str(data['source_uuid'])
        except ValueError:
            return {"wallet_response": {"error": "Key 'source_uuid' has to be string for endpoint get."}}
        try:
            key: str = str(data['key'])
        except ValueError:
            return {"wallet_response": {"error": "Key 'key' has to be string for endpoint get."}}
        wallet_response: dict = Wallet.get(source_uuid, key)
    elif endpoint[0] == 'send':
        if 'source_uuid' not in data:
            return {"wallet_response": {"error": "Key 'source_uuid' has to be set for endpoint send."}}
        if 'key' not in data:
            return {"wallet_response": {"error": "Key 'key' has to be set for endpoint send."}}
        if 'send_amount' not in data:
            return {"wallet_response": {"error": "Key 'send_amount' has to be set for endpoint send."}}
        if 'destination_uuid' not in data:
            return {"wallet_response": {"error": "Key 'destination_uuid' has to be set for endpoint send."}}
        if 'usage' not in data:
            usage = ''
        else:
            try:
                usage: str = str(data['usage'])
            except ValueError:
                return {"wallet_response": {"error": "Key 'usage' has to be string for endpoint send."}}
        try:
            source_uuid: str = str(data['source_uuid'])
        except ValueError:
            return {"wallet_response": {"error": "Key 'source_uuid' has to be string for endpoint send."}}
        try:
            key: str = str(data['key'])
        except ValueError:
            return {"wallet_response": {"error": "Key 'key' has to be string for endpoint send."}}
        try:
            send_amount: int = int(data['send_amount'])
        except ValueError:
            return {"wallet_response": {"error": "Key 'send_amount' has to be int for endpoint send."}}
        try:
            destination_uuid: str = str(data['destination_uuid'])
        except ValueError:
            return {"wallet_response": {"error": "Key 'destination_uuid' has to be string for endpoint send."}}
        wallet_response: dict = Wallet.send_coins(source_uuid, key, send_amount, destination_uuid, usage)
    elif endpoint[0] == 'reset':
        if 'source_uuid' not in data:
            return {"wallet_response": {"error": "Key 'source_uuid' has to be set for endpoint reset."}}
        try:
            source_uuid: str = str(data['source_uuid'])
        except ValueError:
            return {"wallet_response": {"error": "Key 'source_uuid' has to be string for endpoint reset."}}
        wallet_response: dict = Wallet.reset(source_uuid)
    elif endpoint[0] == 'gift':
        if 'source_uuid' not in data:
            return {"wallet_response": {"error": "Key 'source_uuid' has to be set for endpoint gift."}}
        if 'send_amount' not in data:
            return {"wallet_response": {"error": "Key 'send_amount' has to be set for endpoint gift."}}
        try:
            source_uuid: str = str(data['source_uuid'])
        except ValueError:
            return {"wallet_response": {"error": "Key 'source_uuid' has to be string for endpoint gift."}}
        try:
            send_amount: int = int(data['send_amount'])
        except ValueError:
            return {"wallet_response": {"error": "Key 'send_amount' has to be int for endpoint gift."}}
        wallet_response: dict = Wallet.gift(send_amount, source_uuid)
    elif endpoint[0] == 'delete':
        if 'source_uuid' not in data:
            return {"wallet_response": {"error": "Key 'source_uuid' has to be set for endpoint delete."}}
        try:
            source_uuid: str = str(data['source_uuid'])
        except ValueError:
            return {"wallet_response": {"error": "Key 'source_uuid' has to be string for endpoint delete."}}
        wallet_response: dict = Wallet.delete(source_uuid)
    else:
        wallet_response: dict = {"error": "Endpoint is not supported."}
    return {"wallet_response": wallet_response}


def handle_ms(ms: str, data: dict, tag: str) -> dict:
    return {"ms": ms, "data": data, "tag": tag}


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
    print(handle(['delete'], {"source_uuid": response2['wallet_response']['uuid']}))
    # m = MicroService('wallet', handle, handle_ms)
    # m.run()
