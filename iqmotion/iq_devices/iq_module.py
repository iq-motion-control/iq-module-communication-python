from iqmotion.iq_devices.iq_module_json_parser import IqModuleJsonParser
from iqmotion.communication.communicator import Communicator
from iqmotion.clients import client_with_entries
from iqmotion.custom_errors import IqModuleError
from iqmotion.message_making.dictionary_message_maker import DictionaryMessageMaker
from iqmotion.client_entries.dictionary_client_entry import AccessType
from iqmotion.message_making.client_with_entries_message import ClientWithEntriesMessage


import time


class IqModule:
    """ IqModule is an asbstract interface class for all the modules made by iq
    """

    _MODULE_FILE_NAME = ""

    def __init__(self, com: Communicator, module_idn=0):
        self._client_dict = {}
        self._com = com
        self._module_idn = module_idn

        module_file_dict = IqModuleJsonParser.parse(self._MODULE_FILE_NAME)
        self._create_clients(module_file_dict)

    def _create_clients(self, module_file_dict: dict):
        # TODO: parse different clients ?
        for client_name in module_file_dict["clients"]:
            self._client_dict[client_name] = client_with_entries.ClientWithEntries(
                client_name, self._module_idn
            )

    def set(self, client_name: str, client_entry_name: str, *args):
        """ Sets a value to the module with a message formed by a client and client entry

        Args:
            client_name (str): name of client
            client_entry (str): name of client entry
            *args (): value(s) to be set
        """
        self._client_and_client_entry_exists(client_name, client_entry_name)

        client = self._client_dict[client_name]
        client_entry = client.client_entries[client_entry_name]

        if client_entry.data.format == "":
            raise IqModuleError(
                "This client entry '{0}' cannot be set".format(client_entry_name)
            )

        message_bytes = self._make_message_bytes(client_entry, AccessType.SET, args)

        self._com.send_message(message_bytes)

    def get(self, client_name: str, client_entry_name: str, time_out=0.1):
        """ Gets the value define by the client and client entry from the module.

        This call is blocking and will wait until it gets a reply or timeouts.

        Args:
            client_name (str): name of client
            client_entry (str): name of client entry
            timeout=1 (int): blocking timeout while waiting for a reply

        Returns:
            reply (format): the reply from the module
            None: if no reply was available (timeout)
        """
        self.get_async(client_name, client_entry_name)

        max_time = time.time() + time_out
        while not self.is_fresh(client_name, client_entry_name):
            self.update_replies()

            if time.time() > max_time:
                return None

        reply = self.get_reply(client_name, client_entry_name)
        return reply

    def get_all(self, client_name: str, time_out=0.1):
        """ Gets all the value define by the client (all of its client entries).

        This call is blocking and will wait until it gets a reply or timeouts for every "get" call

        Args:
            client_name (str): name of client
            timeout=1 (int): blocking timeout while waiting for a reply

        Returns:
            replies (dict{str:format}): all the successful replies of the module
        """
        self._client_exists(client_name)
        client = self._client_dict[client_name]

        replies = {}
        for client_entry_name in client.client_entries.keys():
            reply = self.get(client_name, client_entry_name, time_out)
            replies[client_entry_name] = reply

        return replies

    def save(self, client_name: str, client_entry_name: str):
        """ Saves a the client and client entry value already set on the module

        Args:
            client_name (str): name of client
            client_entry (str): name of client entry
        """
        self._client_and_client_entry_exists(client_name, client_entry_name)

        client = self._client_dict[client_name]
        client_entry = client.client_entries[client_entry_name]

        message_bytes = self._make_message_bytes(client_entry, AccessType.SAVE, [])

        self._com.send_message(message_bytes)

    def save_all(self, client_name: str):
        """ Saves all the values of the client already set on the module

        Args:
            client_name (str): name of client
        """
        self._client_exists(client_name)
        client = self._client_dict[client_name]

        for client_entry_name in client.client_entries.keys():
            self.save(client_name, client_entry_name)

    def get_async(self, client_name: str, client_entry_name: str):
        """ Sends a asynchroniously get request to the module

        This call is non blocking, to read the reply you have to call "update reply" and then "get_reply" if that client entry is fresh

        Args:
            client_name (str): name of client
            client_entry (str): name of client entry
        """
        self._client_and_client_entry_exists(client_name, client_entry_name)
        client = self._client_dict[client_name]
        client_entry = client.client_entries[client_entry_name]

        message_bytes = self._make_message_bytes(client_entry, AccessType.GET, [])

        self._com.send_message(message_bytes)

    def update_replies(self):
        """ Reads all the bytes available in the Communication queue and stores them in the right client entries
        """
        self._com.read_bytes()

        while self._com.bytes_left_in_queue:
            new_message = self._com.extract_message()
            if new_message != None:
                for client in self._client_dict.values():
                    client.read_message(new_message)

            self._com.read_bytes()

    def is_fresh(self, client_name: str, client_entry_name: str):
        """ Check if the value in client, client entry is new or not (fresh/not fresh)

        This method is usually called after "update_replies" to check if a client entry got updated

        Args:
            client_name (str): name of client
            client_entry (str): name of client entry

        Returns:
            True: value is fresh
            False: value is not fresh
        """
        self._client_and_client_entry_exists(client_name, client_entry_name)
        client = self._client_dict[client_name]
        return client.is_fresh(client_entry_name)

    def get_reply(self, client_name: str, client_entry_name: str):
        """ Reads the reply stored in the client entry

        This method is normally called after checking if the value is fresh with "is_fresh" 

        Args:
            client_name (str): name of client
            client_entry (str): name of client entry

        Return:
            reply (format): value stored in client_entry
        """
        self._client_and_client_entry_exists(client_name, client_entry_name)
        client = self._client_dict[client_name]

        return client.get_reply(client_entry_name)

    def list_clients(self):
        """ Displays all the clients available with the module 
        """
        print("\nClients available from '{0}':\n".format(self._MODULE_FILE_NAME))

        for client_name in self._client_dict.keys():
            print("\t{0}".format(client_name))

        return

    def list_client_entries(self, client_name: str):
        """ Displays all the client entries available for that client

        Args:
            client_name (str): name of client
        """
        self._client_exists(client_name)

        # TODO: Make a pretty table with indication of all values
        print("\nEntries available loaded from '{0}': \n".format(client_name))

        client = self._client_dict[client_name]
        for client_entry in client.client_entries.values():
            print(client_entry.data)

        return

    def _client_and_client_entry_exists(self, client_name: str, client_entry_name: str):
        self._client_exists(client_name)

        client = self._client_dict[client_name]

        if client_entry_name not in client.client_entries.keys():
            raise IqModuleError(
                "{0} does not support this client entry: {1}\n".format(
                    client_name, client_entry_name
                )
            )

        return 1

    def _client_exists(self, client_name: str):
        if client_name not in self._client_dict.keys():
            raise IqModuleError(
                "This module does not support this client: {0}\n".format(client_name)
            )
        return True

    def _make_message_bytes(self, client_entry, access_type: AccessType, args):
        message_maker = DictionaryMessageMaker(
            client_entry, self._module_idn, access_type, args
        )

        message = ClientWithEntriesMessage(message_maker)

        return message.make_bytes()
