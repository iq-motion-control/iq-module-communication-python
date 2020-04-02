from iqmotion.clients import client_with_entries
from iqmotion.iq_devices.iq_module import IqModule
from iqmotion.iq_devices.iq_module_json_parser import IqModuleJsonParser
from iqmotion.communication.communicator import Communicator
from iqmotion.custom_errors import IqModuleError

from iqmotion.tests.helpers import MockCommunicator

import os
import json
import serial

import pytest
from unittest.mock import patch, Mock, MagicMock, call, PropertyMock


class TestIqModule:
    _CLIENT_NAME = "client_test"

    _MODULE_FILE_NAME = "iq2306_2200kv.json"

    _DICTIONARY_MSG_SET = (["dictionary_client_entry", 99], [1, 1, 1, 99])
    _EMPTY_DICTIONARY_MSG_SET = (
        ["dictionary_client_entry_no_format", []],
        [3, 3, 1],
    )

    _PROCESS_MSG_SET = (["process_client_entry", 98], [2, 2, 1, 98])

    _DICTIONARY_MSG_GET = ("dictionary_client_entry", [1, 1, 0])

    _DICTIONARY_MSG_SAVE = ("dictionary_client_entry", [1, 1, 2])

    _DICTIONARY_MSG_REPLY = (["dictionary_client_entry", [1, 1, 3, 99]], 99)

    @pytest.fixture
    def mock_communicator(self):
        mock_class = MockCommunicator()
        return mock_class

    @pytest.fixture
    def mock_client(self, request):
        client_file_name = self._CLIENT_NAME
        test_dir = os.path.dirname(__file__)

        with patch("os.path.dirname") as mock_class:
            mock_class.return_value = test_dir
            test_client = client_with_entries.ClientWithEntries(client_file_name)

        with patch(
            "iqmotion.clients.client_with_entries.ClientWithEntries"
        ) as mock_class:
            with patch.object(IqModuleJsonParser, "parse") as mock_parser:
                mock_parser.return_value = {"clients": [self._CLIENT_NAME]}
                mock_class.return_value = test_client
                mock_client = mock_class.return_value
                yield mock_client

    def test_wrong_client(self, mock_communicator, mock_client):
        module = IqModule(mock_communicator)
        client_name = "fake_client"
        client_entry_name = "fake_client_entry"

        with pytest.raises(IqModuleError) as err:
            module.set(client_name, client_entry_name, 0)

        err_str = err.value.message
        assert (
            "IQ MODULE ERROR: This module does not support this client: {0}\n\n".format(
                client_name
            )
            == err_str
        )

    def test_wrong_client_entry(self, mock_communicator, mock_client):
        module = IqModule(mock_communicator)
        client_name = self._CLIENT_NAME
        client_entry_name = "fake_client_entry"

        with pytest.raises(IqModuleError) as err:
            module.set(client_name, client_entry_name, 0)

        err_str = err.value.message
        assert (
            "IQ MODULE ERROR: {0} does not support this client entry: {1}\n\n".format(
                client_name, client_entry_name
            )
            == err_str
        )

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            _DICTIONARY_MSG_SET,
            _EMPTY_DICTIONARY_MSG_SET,
            # _PROCESS_MSG_SET
        ],
    )
    def test_set(self, mock_communicator, mock_client, test_input, expected):
        mock_communicator.send_message = MagicMock()
        module = IqModule(mock_communicator)

        client_entry_name = test_input[0]
        value = test_input[1]
        module.set(self._CLIENT_NAME, client_entry_name, value)

        assert mock_communicator.send_message.call_args == call(bytearray(expected))

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            _DICTIONARY_MSG_REPLY,
            # _PROCESS_MSG_REPLY
        ],
    )
    def test_get(self, mock_communicator, mock_client, test_input, expected):
        client_entry_name = test_input[0]
        valid_message = test_input[1]

        mock_communicator.read_bytes = MagicMock()
        mock_communicator.extract_message = MagicMock()
        mock_communicator.extract_message.side_effect = [bytearray(valid_message), None]

        module = IqModule(mock_communicator)

        assert module.get("client_test", client_entry_name) == expected

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            _DICTIONARY_MSG_REPLY,
            # _PROCESS_MSG_REPLY
        ],
    )
    def test_get_retry(self, mock_communicator, mock_client, test_input, expected):
        client_entry_name = test_input[0]
        valid_message = test_input[1]

        mock_communicator.read_bytes = MagicMock()
        mock_communicator.extract_message = MagicMock()
        mock_communicator.extract_message.side_effect = [bytearray(valid_message), None]

        module = IqModule(mock_communicator)

        retries = 5
        reply = module.get_retry("client_test", client_entry_name, retries=retries)

        assert reply == expected

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            _DICTIONARY_MSG_REPLY,
            # _PROCESS_MSG_REPLY
        ],
    )
    def test_get_retry_fail(self, mock_communicator, mock_client, test_input, expected):
        client_entry_name = test_input[0]

        module = IqModule(mock_communicator)

        module.get = MagicMock()
        module.get.return_value = None

        retries = 5
        _ = module.get_retry("client_test", client_entry_name, retries=retries)

        assert module.get.call_count == retries

    @pytest.mark.parametrize(
        "test_input",
        [
            _DICTIONARY_MSG_REPLY,
            # _PROCESS_MSG_GET
        ],
    )
    def test_get_timeout(self, mock_communicator, mock_client, test_input):
        client_entry_name = test_input[0][0]
        module = IqModule(mock_communicator)

        assert module.get("client_test", client_entry_name) == None

    def test_get_all(self, mock_communicator, mock_client):
        module = IqModule(mock_communicator)
        module.get = MagicMock()
        module.get.return_value = "test"
        num_client_entries = len(mock_client.client_entries)

        module.get_all(self._CLIENT_NAME)

        assert module.get.call_count == num_client_entries

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            _DICTIONARY_MSG_SAVE,
            # _PROCESS_MSG_SAVE
        ],
    )
    def test_save(self, mock_communicator, mock_client, test_input, expected):
        mock_communicator.send_message = MagicMock()
        module = IqModule(mock_communicator)

        client_entry_name = test_input
        module.save(self._CLIENT_NAME, client_entry_name)

        assert mock_communicator.send_message.call_args == call(bytearray(expected))

    def test_save_all(self, mock_communicator, mock_client):
        module = IqModule(mock_communicator)
        module.save = MagicMock()
        module.save.return_value = "test"
        num_client_entries = len(mock_client.client_entries)

        module.save_all(self._CLIENT_NAME)

        assert module.save.call_count == num_client_entries

    def test_flush_input_buffer(self, mock_communicator, mock_client):
        mock_communicator.flush_input_buffer = MagicMock()
        module = IqModule(mock_communicator)
        module.flush_input_com_buffer()

        assert mock_communicator.flush_input_buffer.called == True

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            _DICTIONARY_MSG_GET,
            # _PROCESS_MSG_GET
        ],
    )
    def test_get_async(self, mock_communicator, mock_client, test_input, expected):
        mock_communicator.send_message = MagicMock()
        module = IqModule(mock_communicator)

        client_entry_name = test_input
        module.get_async(self._CLIENT_NAME, client_entry_name)

        assert mock_communicator.send_message.call_args == call(bytearray(expected))

    def test_update_replies(self, mock_communicator, mock_client):
        mock_communicator.read_bytes = MagicMock()
        mock_communicator.extract_message = MagicMock()
        mock_communicator.extract_message.side_effect = [bytearray([1, 2, 3]), None]

        module = IqModule(mock_communicator)
        module.update_replies()

        assert mock_communicator.read_bytes.call_count == 1
        assert mock_communicator.extract_message.called == True

    def test_update_reply(self, mock_communicator, mock_client):
        mock_communicator.read_bytes = MagicMock()
        mock_communicator.extract_message = MagicMock()
        mock_communicator.extract_message.side_effect = [None, bytearray([1, 2, 3])]

        module = IqModule(mock_communicator)
        module.update_reply()

        assert mock_communicator.read_bytes.call_count == 1
        assert mock_communicator.extract_message.call_count == 2

    @pytest.mark.parametrize(
        "test_input",
        [
            _DICTIONARY_MSG_REPLY,
            # _PROCESS_MSG_REPLY
        ],
    )
    def test_is_fresh(self, mock_communicator, mock_client, test_input):
        client_entry_name = test_input[0][0]
        valid_message = test_input[0][1]

        mock_communicator.read_bytes = MagicMock()
        mock_communicator.extract_message = MagicMock()
        mock_communicator.extract_message.side_effect = [bytearray(valid_message), None]

        module = IqModule(mock_communicator)
        assert module.is_fresh(self._CLIENT_NAME, client_entry_name) == False
        module.update_replies()
        assert module.is_fresh(self._CLIENT_NAME, client_entry_name) == True

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            _DICTIONARY_MSG_REPLY,
            # _PROCESS_MSG_REPLY
        ],
    )
    def test_get_reply(self, mock_communicator, mock_client, test_input, expected):
        client_entry_name = test_input[0]
        valid_message = test_input[1]

        mock_communicator.read_bytes = MagicMock()
        mock_communicator.extract_message = MagicMock()
        mock_communicator.extract_message.side_effect = [bytearray(valid_message), None]

        module = IqModule(mock_communicator)
        module.update_replies()

        assert module.get_reply("client_test", client_entry_name) == expected

