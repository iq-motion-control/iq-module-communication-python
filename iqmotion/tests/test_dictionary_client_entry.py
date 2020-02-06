from iqmotion.client_entries.dictionary_client_entry import DictionaryClientEntry
from iqmotion.client_entries.dictionary_client_entry import DictionaryClientEntryData

import pytest

TEST_CLIENT_ENTRY_DICT = {
    "type_idn": 50,
    "param": "test",
    "param_idn": 0,
    "format": "B",
    "unit": "fake",
}


class TestDictionaryClientEntry:
    def test_read_message(self):
        message = bytearray([50, 0, 3, 99])
        dce = DictionaryClientEntry(TEST_CLIENT_ENTRY_DICT)

        dce.read_message(message)

        assert dce.fresh == True

    def test_read_message_wrong_access_type(self):
        message = bytearray([50, 0, 1, 99])
        dce = DictionaryClientEntry(TEST_CLIENT_ENTRY_DICT)

        dce.read_message(message)

        assert dce.fresh == False

    def test_fresh(self):
        dce = DictionaryClientEntry(TEST_CLIENT_ENTRY_DICT)

        assert dce.fresh == False

        dce.value = bytearray([11])
        assert dce.fresh == True

        _ = dce.value
        assert dce.fresh == False

    def test_value(self):
        dce = DictionaryClientEntry(TEST_CLIENT_ENTRY_DICT)

        assert dce.value == None

        dce.value = bytearray([11])
        assert dce.value == 11

    def test_data(self):
        dce = DictionaryClientEntry(TEST_CLIENT_ENTRY_DICT)

        expected_data = DictionaryClientEntryData(TEST_CLIENT_ENTRY_DICT)

        assert dce.data == expected_data

    def test_data__str__(self):
        dce = DictionaryClientEntry(TEST_CLIENT_ENTRY_DICT)

        expected_str = "{0:10} | {1:2}: {2:32} {3:4} {4}".format(
            TEST_CLIENT_ENTRY_DICT["type_idn"],
            TEST_CLIENT_ENTRY_DICT["param_idn"],
            TEST_CLIENT_ENTRY_DICT["param"],
            TEST_CLIENT_ENTRY_DICT["format"],
            TEST_CLIENT_ENTRY_DICT["unit"],
        )

        assert dce.data.__str__() == expected_str
