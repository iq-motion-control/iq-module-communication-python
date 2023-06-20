import os
import json


def get_parent_dir(path, level=1):
    """ returns the absolute path to parent directory
    
    level -- How many levels up the tree you wish to go

    """
    parent = path

    for _ in range(level):
        parent = os.path.dirname(parent)

    return parent

def load_all_clients(path:str):
    """ returns a json of all clients from a provided path
    """
    clients = [client.replace(".json", "") for client in os.listdir(path) if ".json" in client]

    clients = {"clients":clients}

    return json.dumps(clients, indent=1)

