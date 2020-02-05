from iqmotion.message_making.dictionary_message_maker import DictionaryMessageMaker
from iqmotion.message_making.dictionary_message_maker import DictionaryMessageMakerData
from iqmotion.client_entries.dictionary_client_entry import DictionaryClientEntry
from iqmotion.client_entries.dictionary_client_entry import AccessType
from iqmotion.custom_errors import MessageMakerError


import pytest


class TestDictionaryMessageMaker:
    _FAKE_DICTIONARY_CLIENT_ENTRY_DATA_DICT = {
        "type_idn": 1,
        "param": "dictionary_client_entry",
        "param_idn": 1,
        "format": "B",
        "unit": "rad",
    }

    _FAKE_DICTIONARY_CLIENT_ENTRY_DATA_DICT_LIST = {
        "type_idn": 1,
        "param": "dictionary_client_entry",
        "param_idn": 1,
        "format": "BB*",
        "unit": "rad",
    }

    _TEST_VALUES_ACCESSTYPES = [
        ([AccessType.GET, 0], [1, 1, 0, 0]),
        ([AccessType.SET, 1], [1, 1, 1, 1]),
        ([AccessType.SAVE, 2], [1, 1, 2, 2]),
        ([AccessType.REPLY, 3], [1, 1, 3, 3]),
    ]

    _TEST_VALUES_ACCESSTYPES_LIST = [
        ([AccessType.GET, [0, 0]], [1, 1, 0, 0, 0]),
        ([AccessType.SET, [1, 1]], [1, 1, 1, 1, 1]),
        ([AccessType.SAVE, [2, 2, 2]], [1, 1, 2, 2, 2, 2]),
        ([AccessType.REPLY, [3, 3, 3, 3]], [1, 1, 3, 3, 3, 3, 3]),
    ]

    @pytest.fixture
    def test_input(self):
        """dummy fixture that changes with the pytest.mark.parametrize
        in the actual tests
        """
        return ([AccessType.GET, 0], 0)

    @pytest.fixture()
    def message_maker(self, test_input):
        client_entry = DictionaryClientEntry(
            self._FAKE_DICTIONARY_CLIENT_ENTRY_DATA_DICT
        )

        acces_type = test_input[0]
        value = test_input[1]

        message_maker = DictionaryMessageMaker(client_entry, 0, acces_type, value)

        return message_maker

    @pytest.fixture()
    def message_maker_with_list_client_entry(self, test_input):
        client_entry = DictionaryClientEntry(
            self._FAKE_DICTIONARY_CLIENT_ENTRY_DATA_DICT_LIST
        )

        acces_type = test_input[0]
        value = test_input[1]

        message_maker = DictionaryMessageMaker(client_entry, 0, acces_type, value)

        return message_maker

    @pytest.mark.parametrize("test_input, expected", _TEST_VALUES_ACCESSTYPES)
    def test_make(self, message_maker, test_input, expected):
        message = message_maker.make()

        assert message == bytearray(expected)

    @pytest.mark.parametrize("test_input, expected", _TEST_VALUES_ACCESSTYPES_LIST)
    def test_make_with_list_values(
        self, message_maker_with_list_client_entry, test_input, expected
    ):
        message = message_maker_with_list_client_entry.make()

        assert message == bytearray(expected)

    @pytest.mark.parametrize("test_input, expected", _TEST_VALUES_ACCESSTYPES_LIST)
    def test_make_values_too_long(self, message_maker, test_input, expected):

        with pytest.raises(MessageMakerError) as err:
            message_maker.make()

        err_str = err.value.message
        assert "MESSAGE MAKER ERROR: values too long for client entry\n" == err_str
