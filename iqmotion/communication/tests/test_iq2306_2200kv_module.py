
from iqmotion.communication.client_with_entries import ClientWithEntries
from iqmotion.communication import client_with_entries
from iqmotion.communication.speed_module import SpeedModule
from iqmotion.communication.iq_module_json_parser import IqModuleJsonParser
from iqmotion.communication.custom_error import IqModuleError
from iqmotion.communication.communication import Communication

from iqmotion.communication.tests.helpers import MockCommunication

import os
import json
import serial

import pytest
from unittest.mock import patch, Mock, MagicMock, call, PropertyMock


class TestSpeedModule():
    _CLIENT_NAME = "client_test"

    _MODULE_FILE_NAME = "iq2306_2200kv.json"

    _DICTIONARY_MSG_SET = (["dictionary_client_entry", 99], [1, 1, 1, 99])
    _PROCESS_MSG_SET = (["process_client_entry", 98], [2, 2, 1, 98])

    _DICTIONARY_MSG_GET = ("dictionary_client_entry", [1, 1, 0])

    _DICTIONARY_MSG_SAVE = ("dictionary_client_entry", [1, 1, 2])

    _DICTIONARY_MSG_REPLY = (["dictionary_client_entry", [1, 1, 3, 99]], 99)

    @pytest.fixture
    def mock_communication(self):
        mock_class = MockCommunication()
        return mock_class

    @pytest.fixture
    def mock_client(self, request):
        client_file_name = self._CLIENT_NAME
        test_dir = os.path.dirname(__file__)

        with patch('os.path.dirname') as mock_class:
            mock_class.return_value = test_dir
            test_client = client_with_entries.ClientWithEntries(
                client_file_name)

        with patch('iqmotion.communication.client_with_entries.ClientWithEntries') as mock_class:
            with patch.object(IqModuleJsonParser, 'parse') as mock_parser:
                mock_parser.return_value = {"clients": [self._CLIENT_NAME]}
                mock_class.return_value = test_client
                mock_client = mock_class.return_value
                yield mock_client

    def test__init__(self, mock_communication):
        SpeedModule(mock_communication)

    def test_wrong_client(self, mock_communication, mock_client):
        module = SpeedModule(mock_communication)
        client_name = "fake_client"
        client_entry_name = "fake_client_entry"

        with pytest.raises(IqModuleError) as err:
            module.set(client_name, client_entry_name, 0)

        err_str = err.value.message
        assert "IQ MODULE ERROR: This module does not support this client: {0}\n\n".format(
            client_name) == err_str

    def test_wrong_client_entry(self, mock_communication, mock_client):
        module = SpeedModule(mock_communication)
        client_name = self._CLIENT_NAME
        client_entry_name = "fake_client_entry"

        with pytest.raises(IqModuleError) as err:
            module.set(client_name, client_entry_name, 0)

        err_str = err.value.message
        assert "IQ MODULE ERROR: {0} does not support this client entry: {1}\n\n".format(
            client_name, client_entry_name) == err_str

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            _DICTIONARY_MSG_SET,
            # _PROCESS_MSG_SET
        ],
    )
    def test_set(self, mock_communication, mock_client, test_input, expected):
        mock_communication.send_message = MagicMock()
        module = SpeedModule(mock_communication)

        client_entry_name = test_input[0]
        value = test_input[1]
        module.set(self._CLIENT_NAME, client_entry_name, value)

        assert mock_communication.send_message.call_args == call(
            bytearray(expected))

    def test_set_no_format(self, mock_communication, mock_client):
        module = SpeedModule(mock_communication)
        client_entry_name = "dictionary_client_entry_no_format"

        with pytest.raises(IqModuleError) as err:
            module.set(self._CLIENT_NAME, client_entry_name, 0)

        err_str = err.value.message
        assert "IQ MODULE ERROR: This client entry '{0}' cannot be set\n".format(
            client_entry_name) == err_str

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            _DICTIONARY_MSG_REPLY,
            # _PROCESS_MSG_REPLY
        ],
    )
    def test_get(self, mock_communication, mock_client, test_input, expected):
        client_entry_name = test_input[0]
        valid_message = test_input[1]

        mock_communication.read_bytes = MagicMock()
        mock_communication.extract_message = MagicMock()
        mock_communication.extract_message.return_value = bytearray(
            valid_message)

        with patch('iqmotion.communication.tests.helpers.MockCommunication.bytes_left_in_queue', new_callable=PropertyMock) as mock_bytes_left:
            mock_bytes_left.side_effect = [4, 0]
            module = SpeedModule(mock_communication)
            module.update_replies()

            assert module.get(
                'client_test', client_entry_name) == expected

    @pytest.mark.parametrize(
        "test_input",
        [
            _DICTIONARY_MSG_REPLY,
            # _PROCESS_MSG_GET
        ],
    )
    def test_get_timeout(self, mock_communication, mock_client, test_input):
        client_entry_name = test_input[0][0]
        module = SpeedModule(mock_communication)

        assert module.get('client_test', client_entry_name) == None

    def test_get_all(self, mock_communication, mock_client):
        module = SpeedModule(mock_communication)
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
    def test_save(self, mock_communication, mock_client, test_input, expected):
        mock_communication.send_message = MagicMock()
        module = SpeedModule(mock_communication)

        client_entry_name = test_input
        module.save(self._CLIENT_NAME, client_entry_name)

        assert mock_communication.send_message.call_args == call(
            bytearray(expected))

    def test_save_all(self, mock_communication, mock_client):
        module = SpeedModule(mock_communication)
        module.save = MagicMock()
        module.save.return_value = "test"
        num_client_entries = len(mock_client.client_entries)

        module.save_all(self._CLIENT_NAME)

        assert module.save.call_count == num_client_entries

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            _DICTIONARY_MSG_GET,
            # _PROCESS_MSG_GET
        ],
    )
    def test_get_async(self, mock_communication, mock_client, test_input, expected):
        mock_communication.send_message = MagicMock()
        module = SpeedModule(mock_communication)

        client_entry_name = test_input
        module.get_async(self._CLIENT_NAME, client_entry_name)

        assert mock_communication.send_message.call_args == call(
            bytearray(expected))

    def test_update_replies(self, mock_communication, mock_client):
        mock_communication.read_bytes = MagicMock()
        mock_communication.extract_message = MagicMock()
        mock_communication.extract_message.return_value = bytearray([1, 2, 3])

        with patch('iqmotion.communication.tests.helpers.MockCommunication.bytes_left_in_queue', new_callable=PropertyMock) as mock_bytes_left:
            mock_bytes_left.side_effect = [5, 0]
            module = SpeedModule(mock_communication)
            module.update_replies()

        assert mock_communication.read_bytes.call_count == 2
        assert mock_communication.extract_message.called == True

    @pytest.mark.parametrize(
        "test_input",
        [
            _DICTIONARY_MSG_REPLY,
            # _PROCESS_MSG_REPLY
        ],
    )
    def test_is_fresh(self, mock_communication, mock_client, test_input):
        client_entry_name = test_input[0][0]
        valid_message = test_input[0][1]

        mock_communication.read_bytes = MagicMock()
        mock_communication.extract_message = MagicMock()
        mock_communication.extract_message.return_value = bytearray(
            valid_message)

        with patch('iqmotion.communication.tests.helpers.MockCommunication.bytes_left_in_queue', new_callable=PropertyMock) as mock_bytes_left:
            mock_bytes_left.side_effect = [4, 0]
            module = SpeedModule(mock_communication)
            assert module.is_fresh(
                self._CLIENT_NAME, client_entry_name) == False
            module.update_replies()
            assert module.is_fresh(
                self._CLIENT_NAME, client_entry_name) == True

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            _DICTIONARY_MSG_REPLY,
            # _PROCESS_MSG_REPLY
        ],
    )
    def test_get_reply(self, mock_communication, mock_client, test_input, expected):
        client_entry_name = test_input[0]
        valid_message = test_input[1]

        mock_communication.read_bytes = MagicMock()
        mock_communication.extract_message = MagicMock()
        mock_communication.extract_message.return_value = bytearray(
            valid_message)

        with patch('iqmotion.communication.tests.helpers.MockCommunication.bytes_left_in_queue', new_callable=PropertyMock) as mock_bytes_left:
            mock_bytes_left.side_effect = [4, 0]
            module = SpeedModule(mock_communication)
            module.update_replies()

            assert module.get_reply(
                'client_test', client_entry_name) == expected
