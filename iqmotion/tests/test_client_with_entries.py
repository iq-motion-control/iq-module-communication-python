from iqmotion.clients.client_with_entries import ClientWithEntries
from iqmotion.custom_errors import ClientError

from iqmotion.tests.helpers import make_fake_message

import pytest
import os

from unittest.mock import patch, Mock, MagicMock, call, PropertyMock


class TestClientWithEntries:
    _DICTIONARY_MSG = (["dictionary_client_entry", 1, [1, 3, 99],], 99)
    _PROCESS_MSG = (["process_client_entry", 2, [98], 2], 98)

    @pytest.fixture(params=["client_test"])
    def client(self, request):
        client_file_name = request.param
        test_dir = os.path.dirname(__file__)

        with patch("os.path.dirname") as mock_class:
            mock_class.return_value = test_dir
            client = ClientWithEntries(client_file_name)
            yield client

    def test_client_jsons(self):
        dir_path = os.path.join(os.path.dirname(__file__), "../clients/client_files/")

        for file in os.listdir(dir_path):
            if file.endswith(".json"):
                client_name = file.split(".")[0]
                ClientWithEntries(client_name)

    def test_not_supported_client_entry(self):
        client_file_name = "fail_client_test"
        test_dir = os.path.dirname(__file__)

        with patch("os.path.dirname") as mock_class:
            mock_class.return_value = test_dir

            with pytest.raises(ClientError) as err:
                ClientWithEntries(client_file_name)

        err_str = err.value.message
        assert (
            "CLIENT ERROR: ClientWithEntries does not support this payload type\n"
            == err_str
        )

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            _DICTIONARY_MSG
            # _PROCESS_MSG
        ],
    )
    def test_read_message(self, client, test_input, expected):
        client_entry_name = test_input[0]
        type_idn = test_input[1]
        payload = test_input[2]
        msg = make_fake_message(payload, type_idn)

        client.read_message(msg)

        assert client.get_reply(client_entry_name) == expected

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            _DICTIONARY_MSG
            # _PROCESS_MSG
        ],
    )
    def test_is_fresh(self, client, test_input, expected):
        client_entry_name = test_input[0]
        type_idn = test_input[1]
        payload = test_input[2]
        msg = make_fake_message(payload, type_idn)

        assert client.is_fresh(client_entry_name) == False

        client.read_message(msg)

        assert client.is_fresh(client_entry_name) == True

    def test_default_module_idn(self, client):
        assert client.module_idn == 0

    def test_module_idn(self):
        client_file_name = "client_test"
        test_dir = os.path.dirname(__file__)

        module_idn = 5

        with patch("os.path.dirname") as mock_class:
            mock_class.return_value = test_dir
            client = ClientWithEntries(client_file_name, module_idn)

        assert client.module_idn == module_idn

    @pytest.mark.parametrize(
        "test_input",
        [
            _DICTIONARY_MSG,
            # _PROCESS_MSG
        ],
    )
    def test_client_entries(self, client, test_input):
        client_entry_name = test_input[0][0]
        client_entries = client.client_entries

        assert client_entry_name in client_entries.keys()
