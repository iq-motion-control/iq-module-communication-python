from iqmotion.communication.client import Client
from iqmotion.communication.client_entry import ClientEntry
from iqmotion.communication.custom_error import ClientError

import pytest
import os
import json


def get_test_client_file():
    test_client_name = "brushless_drive"
    client_json = test_client_name + ".json"
    file_path = os.path.join(os.path.dirname(
        __file__), ('clients/' + client_json))

    with open(file_path) as json_file:
        client_file = json.load(json_file)

    return client_file


def get_test_client_entries_dict():
    client_file = get_test_client_file()
    test_client_entries_dict = {}
    for client_entry_dict in client_file:
        client_entry_name = client_entry_dict["param"]
        test_client_entries_dict[client_entry_name] = ClientEntry(
            client_entry_dict)

    return test_client_entries_dict


class TestClient():

    def test_get(self):
        pass

    def test_set_fake_client_entry(self):
        with pytest.raises(ClientError) as err:
            client = Client("brushless_drive")
            assert client.set("fake_client_entry")

        err_str = err.value.message
        assert "CLIENT ERROR: Client_entry not in Client\n" == err_str

    def test_set(self):
        client = Client("brushless_drive")
        test_client_entries_dic = get_test_client_entries_dict()

        for client_entry_name in test_client_entries_dic.keys():
            assert client.set(client_entry_name) == 1

    def test_save(self):
        pass

    def test_list(self):
        client = Client("brushless_drive")
        client_entries_dic = client.list()
        test_client_entries_dic = get_test_client_entries_dict()

        assert client_entries_dic.keys() == test_client_entries_dic.keys()
