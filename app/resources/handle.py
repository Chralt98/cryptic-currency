from models.wallet_db import Wallet


def handle(endpoint: list, data: dict) -> dict:
    """
    The handle method to get data from server to know what to do
    :param endpoint: the action of the server 'get', 'create', 'send'
    :param data: source_uuid, key, send_amount, destination_uuid ...
    :return: wallet response for actions
    """
    # endpoint[0] will be the action what to do in an array ['get', ...]
    if endpoint[0] == 'create':
        if 'user_uuid' not in data:
            return {"wallet_response": {"error": "Key 'user_uuid' has to be set for endpoint create."}}
        if type(data["user_uuid"]) is not str:
            return {"wallet_response": {"error": "Key 'user_uuid' has to be string for endpoint create."}}
        user_uuid = data['user_uuid']
        wallet_response: dict = Wallet.create(user_uuid)
    elif endpoint[0] == 'get':
        if 'source_uuid' not in data:
            return {"wallet_response": {"error": "Key 'source_uuid' has to be set for endpoint get."}}
        if 'key' not in data:
            return {"wallet_response": {"error": "Key 'key' has to be set for endpoint get."}}
        if type(data["source_uuid"]) is not str:
            return {"wallet_response": {"error": "Key 'source_uuid' has to be string for endpoint get."}}
        if type(data['key']) is not str:
            return {"wallet_response": {"error": "Key 'key' has to be string for endpoint get."}}
        source_uuid = data['source_uuid']
        key = data['key']
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
            usage: str = ''
        else:
            if type(data['usage']) is not str:
                return {"wallet_response": {"error": "Key 'usage' has to be string for endpoint send."}}
            usage: str = data['usage']
        if type(data['source_uuid']) is not str:
            return {"wallet_response": {"error": "Key 'source_uuid' has to be string for endpoint send."}}
        source_uuid: str = data['source_uuid']
        if type(data['key']) is not str:
            return {"wallet_response": {"error": "Key 'key' has to be string for endpoint send."}}
        key: str = data['key']
        if type(data['send_amount']) is not int:
            return {"wallet_response": {"error": "Key 'send_amount' has to be int for endpoint send."}}
        send_amount: int = data['send_amount']
        if type(data['destination_uuid']) is not str:
            return {"wallet_response": {"error": "Key 'destination_uuid' has to be string for endpoint send."}}
        destination_uuid: str = data['destination_uuid']
        wallet_response: dict = Wallet.send_coins(source_uuid, key, send_amount, destination_uuid, usage)
    elif endpoint[0] == 'reset':
        if 'source_uuid' not in data:
            return {"wallet_response": {"error": "Key 'source_uuid' has to be set for endpoint reset."}}
        if type(data['source_uuid']) is not str:
            return {"wallet_response": {"error": "Key 'source_uuid' has to be string for endpoint reset."}}
        source_uuid: str = data['source_uuid']
        wallet_response: dict = Wallet.reset(source_uuid)
    elif endpoint[0] == 'gift':
        if 'source_uuid' not in data:
            return {"wallet_response": {"error": "Key 'source_uuid' has to be set for endpoint gift."}}
        if 'send_amount' not in data:
            return {"wallet_response": {"error": "Key 'send_amount' has to be set for endpoint gift."}}
        if type(data['source_uuid']) is not str:
            return {"wallet_response": {"error": "Key 'source_uuid' has to be string for endpoint gift."}}
        if type(data['send_amount']) is not int:
            return {"wallet_response": {"error": "Key 'send_amount' has to be int for endpoint gift."}}
        source_uuid: str = data['source_uuid']
        send_amount: int = data['send_amount']
        wallet_response: dict = Wallet.gift(send_amount, source_uuid)
    elif endpoint[0] == 'delete':
        if 'source_uuid' not in data:
            return {"wallet_response": {"error": "Key 'source_uuid' has to be set for endpoint delete."}}
        if type(data['source_uuid']) is not str:
            return {"wallet_response": {"error": "Key 'source_uuid' has to be string for endpoint delete."}}
        source_uuid: str = data['source_uuid']
        wallet_response: dict = Wallet.delete(source_uuid)
    else:
        wallet_response: dict = {"error": "Endpoint is not supported."}
    return {"wallet_response": wallet_response}


def handle_ms(data: dict) -> dict:
    return data
