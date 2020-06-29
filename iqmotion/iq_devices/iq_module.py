import time
import os

from iqmotion.iq_devices.common_commands.ramper import Ramper
from iqmotion.client_entries.dictionary_client_entry import AccessType
from iqmotion.clients.client_with_entries import ClientWithEntries
from iqmotion.communication.communicator import Communicator
from iqmotion.custom_errors import IqModuleError
from iqmotion.iq_devices.iq_module_json_parser import IqModuleJsonParser
from iqmotion.message_making.client_with_entries_message import ClientWithEntriesMessage
from iqmotion.message_making.dictionary_message_maker import DictionaryMessageMaker


class IqModule:
    """ IqModule is an asbstract interface class for all the modules made by iq
    """

    _MODULE_FILE_NAME = ""
    _DEFAULT_CONTROL_CLIENT = ""
    _DEFAULT_VELOCITY_CLIENT_ENTRY = ""
    _DEFAULT_VOLTS_CLIENT_ENTRY = ""

    def __init__(
        self, com: Communicator, module_idn=0, extra_clients=None, module_file_path=None
    ):
        self._client_dict = {}
        self._com = com
        self._module_idn = module_idn

        if module_file_path is None:
            self._module_file_dict = IqModuleJsonParser.parse_default_modules(
                self._MODULE_FILE_NAME
            )
        else:
            self._module_file_dict = IqModuleJsonParser.parse_module(module_file_path)

        self._create_clients(self._module_file_dict)

        if extra_clients is not None:
            for extra_client in extra_clients:
                self.add_client(extra_client)

    def _create_clients(self, module_file_dict: dict):

        # parse different clients when new clients will be added
        for client_name in module_file_dict["clients"]:
            self._client_dict[client_name] = ClientWithEntries.from_default_clients(
                client_name, self._module_idn
            )

    def add_client(self, client_file_path: str):
        client_name = os.path.basename(client_file_path)
        if not client_name.endswith(".json"):
            raise IqModuleError(
                f"Path does not lead to a json file: {client_file_path}"
            )

        client_name = client_name.split(".")[0]

        self._client_dict[client_name] = ClientWithEntries(
            client_file_path, self._module_idn
        )

    def coast(self):
        """ Sends a coast command from the default control client to the module.
        You can check the success with "brushless_drive" "drive_mode".
        """
        self.set(self._DEFAULT_CONTROL_CLIENT, "ctrl_coast")

    def set(self, client_name: str, client_entry_name: str, values=None):
        """ Sets a value to the module with a message formed by a client and client entry
        
        Arguments:
            client_name {str} -- name of the client
            client_entry_name {str} -- name of the client entry
            values -- value(s) to be set
        """
        self._client_and_client_entry_exists(client_name, client_entry_name)

        client = self._client_dict[client_name]
        client_entry = client.client_entries[client_entry_name]

        message_bytes = self._make_message_bytes(client_entry, AccessType.SET, values)

        self._com.send_message(message_bytes)

    def set_verify(
        self,
        client_name: str,
        client_entry_name: str,
        values=None,
        get_values=None,
        time_out=0.1,
        retries=5,
        save=False,
    ):
        """ Sets a value to the module with a message formed by a client and client entry and checks 
        if value was set properly. You can also set "save=True" to save the value if the verify was 
        succesful.

        Arguments:
            client_name {str} -- name of the client
            client_entry_name {str} -- name of the client entry

        Keyword Arguments:
            values {int, list} -- value(s) to be set
            get_values {int, list} -- values to add in the get message (such as index for some client entries) (default: {None})
            time_out {float} -- blocking timeout while verifying the set (s) (default: {0.1})
            retries {int} -- num of times you want to retry (default: {5})
            save {bool} -- save the value if verify was successful (default: {False})

        Returns:
            bool -- if the value was correctly set
        """
        VERIFY_RANGE = 0.01

        success = False
        for _ in range(retries):
            self.flush_input_com_buffer()
            self.set(client_name, client_entry_name, values)

            returned_value = self.get(
                client_name, client_entry_name, get_values, time_out=time_out,
            )

            # checks when you do an empty set
            if values is None:
                if returned_value == 1:
                    success = True
                    break

            elif self._verify_value(values, returned_value, VERIFY_RANGE):
                success = True
                break

        if not success:
            return False

        if save:
            self.save(client_name, client_entry_name)

        return True

    def _verify_value(self, set_value, returned_value, verify_range=0.01):
        if returned_value is None:
            return False

        # some values might loose precision when being saved so check if it's within a 0.01 range
        if abs(set_value - returned_value) >= verify_range:
            return False

        return True

    def get(
        self, client_name: str, client_entry_name: str, get_values=None, time_out=0.1
    ):
        """ Gets the value define by the client and client entry from the module.

        This call is blocking and will wait until it gets a reply or timeouts.
        
        Arguments:
            client_name {str} -- name of the client
            client_entry_name {str} -- name of the client entry
        
        Keyword Arguments:
            get_values {int, list} -- values to add in the get message (such as index for some client entries) (default: {None})
            time_out {float} -- blocking timeout while waiting for a reply (s) (default: {0.1})
        
        Returns:
            the reply from the module, None if no reply was available (timeout)
        """
        self.get_async(client_name, client_entry_name, get_values)

        max_time = time.perf_counter() + time_out
        while not self.is_fresh(client_name, client_entry_name):
            if time.perf_counter() > max_time:
                return None

            self.update_replies()

        reply = self.get_reply(client_name, client_entry_name)
        return reply

    def get_retry(
        self,
        client_name: str,
        client_entry_name: str,
        get_values=None,
        time_out=0.1,
        retries=5,
    ):
        """ Sends multiple get requests to the module until a reply comes back or there are no more retries left
        
        Arguments:
            client_name {str} -- name of the client 
            client_entry_name {str} -- name of the client entry
        
        Keyword Arguments:
            get_values {int, list} -- values to add in the get message (such as index for some client entries) (default: {None})
            time_out {float} -- blocking timeout while waiting for a reply for every retry (s) (default: {0.1})
            retries {int} -- num of times you want to retry sending a get request if nothing came back (default: {5})
        
        Returns:
            the reply from the module, None if no reply was available (timeout and/or max num of retries)
        """
        for _ in range(retries):
            self.flush_input_com_buffer()
            reply = self.get(
                client_name, client_entry_name, get_values, time_out=time_out
            )
            if reply is not None:
                return reply

        return None

    def get_all(self, client_name: str, time_out=0.1):
        """ Gets all the value define by the client (all of its client entries).

        This call is blocking and will wait until it gets a reply or timeouts for every "get" call
        
        Arguments:
            client_name {str} -- name of client
        
        Keyword Arguments:
            time_out {float} --  blocking timeout while waiting for a reply (s) (default: {0.1})
        
        Returns:
            dict -- all the successful replies of the module
        """
        self._client_exists(client_name)
        client = self._client_dict[client_name]

        replies = {}
        for client_entry_name in client.client_entries.keys():
            reply = self.get(client_name, client_entry_name, time_out=time_out)
            replies[client_entry_name] = reply

        return replies

    def get_all_retry(self, client_name: str, time_out=0.1, retries=5):
        """[summary]

        Arguments:
            client_name {str} -- name of client

        Keyword Arguments:
            time_out {float} -- blocking timeout while waiting for a reply (s) (default: {0.1})
            retries {int} -- num of times you want to retry sending a get request if nothing came back (default: {5})

        Returns:
            dict -- all the successful replies of the module
        """
        self._client_exists(client_name)
        client = self._client_dict[client_name]

        replies = {}
        for client_entry_name in client.client_entries.keys():
            reply = self.get_retry(client_name, client_entry_name, time_out, retries)
            replies[client_entry_name] = reply

        return replies

    def save(self, client_name: str, client_entry_name: str):
        """ Saves the client and client entry values already set on the module
        
        Arguments:
            client_name {str} -- name of the client
            client_entry_name {str} -- name of the client entry
        """
        self._client_and_client_entry_exists(client_name, client_entry_name)

        client = self._client_dict[client_name]
        client_entry = client.client_entries[client_entry_name]

        message_bytes = self._make_message_bytes(client_entry, AccessType.SAVE)

        self._com.send_message(message_bytes)

    def save_all(self, client_name: str):
        """ Saves all the values of the client already set on the module
        
        Arguments:
            client_name {str} -- name of the client
        """
        self._client_exists(client_name)
        client = self._client_dict[client_name]

        for client_entry_name in client.client_entries.keys():
            self.save(client_name, client_entry_name)

    def get_async(self, client_name: str, client_entry_name: str, get_values=None):
        """ Sends a asynchroniously get request to the module

        This call is non blocking, to read the reply you have to call "update reply" or "update replies" and then "get_reply" if that client entry is fresh
        
        Arguments:
            client_name {str} -- name of the client
            client_entry_name {str} -- name of the client entry
            get_values {int, list} -- values to add in the get message (such as index for some client entries) (default: {None})
        """
        self._client_and_client_entry_exists(client_name, client_entry_name)
        client = self._client_dict[client_name]
        client_entry = client.client_entries[client_entry_name]

        message_bytes = self._make_message_bytes(
            client_entry, AccessType.GET, get_values
        )

        self._com.send_message(message_bytes)

    def flush_input_com_buffer(self):
        """ Flushes the input buffer of your communicator object (such as Serial) and queue
        """
        self._com.flush_input_buffer()

    def update_replies(self):
        """ Reads all the bytes possible in the Communication queue and stores them in the right client entries.
        If this returns False, you might want to run this function again (more bytes in the com queue that was possible to parse at once).

        Returns:
            bool -- True if every bytes were read from the Communication queue, False otherwise
        """
        all_bytes_read = self._com.read_bytes()

        new_message = self._com.extract_message()
        while new_message is not None:
            for client in self._client_dict.values():
                client.read_message(new_message)

            new_message = self._com.extract_message()

        return all_bytes_read

    def update_reply(self):
        """ Checks the packet queue (and communication queue if empty) for a new message
        """
        new_message = self._com.extract_message()

        # if no message in the packet queue, read from serial buffer and check again
        if new_message is None:
            self._com.read_bytes()
            new_message = self._com.extract_message()

        if new_message is not None:
            for client in self._client_dict.values():
                client.read_message(new_message)

    def is_fresh(self, client_name: str, client_entry_name: str):
        """ Check if the value in the client, client entry is new or not (fresh/not fresh)

        This method is usually called after "update_replies" to check if a client entry got updated
        
        Arguments:
            client_name {str} -- name of the client
            client_entry_name {str} -- name of the client entry
        
        Returns:
            bool -- True if value is fresh, False otherwise
        """
        self._client_and_client_entry_exists(client_name, client_entry_name)
        client = self._client_dict[client_name]
        return client.is_fresh(client_entry_name)

    def get_reply(self, client_name: str, client_entry_name: str):
        """ Reads the reply stored in the client entry

        This method is normally called after checking if the value is fresh with "is_fresh" 
        
        Arguments:
            client_name {str} -- name of the client
            client_entry_name {str} -- name of the client entry

        
        Returns:
            value stored in client entry
        """
        self._client_and_client_entry_exists(client_name, client_entry_name)
        client = self._client_dict[client_name]

        return client.get_reply(client_entry_name)

    def list_clients(self):
        """ Displays all the clients available with the module 
        """
        print("\nClients available from '{0}':\n".format(self._MODULE_FILE_NAME))

        for client_name in self._client_dict:
            print("\t{0}".format(client_name))

    def list_client_entries(self, client_name: str):
        """ Displays all the client entries available for that client

        Args:
            client_name {str} -- name of client
        """
        self._client_exists(client_name)

        print("\nEntries available loaded from '{0}': \n".format(client_name))

        client = self._client_dict[client_name]
        for client_entry in client.client_entries.values():
            print(client_entry.data)

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

    def _make_message_bytes(self, client_entry, access_type: AccessType, values=None):
        message_maker = DictionaryMessageMaker(
            client_entry, self._module_idn, access_type, values
        )

        message = ClientWithEntriesMessage(message_maker)

        return message.make_bytes()

    def ramp_velocity(self, final_velocity: float, total_time: float, time_steps=20):
        """ Ramps velocity of the module up to a target in set amount of seconds

        Arguments:
            final_velocity {float} -- final velocity goal
            total_time {float} -- time to reach velocity goal (s)

        Keyword Arguments:
            time_steps {int} -- num of velocity increments (default: {20})

        Returns:
            bool -- True if the ramp was successful
        """
        velocity_client = self._DEFAULT_CONTROL_CLIENT
        velocity_client_entry = self._DEFAULT_VELOCITY_CLIENT_ENTRY
        success = Ramper.ramp_velocity(
            self,
            velocity_client,
            velocity_client_entry,
            final_velocity,
            total_time,
            time_steps,
        )

        return success

    def ramp_volts(self, final_volts: float, total_time: float, time_steps=20):
        """ Ramps the volts of the module up to a target in set amount of seconds

        Arguments:
            final_volts {float} -- final volts goal
            total_time {float} -- time to reach volts goal (s)

        Keyword Arguments:
            time_steps {int} -- num of volts increment (default: {20})

        Returns:
            bool -- True if the ramp was successful
        """
        volts_client = self._DEFAULT_CONTROL_CLIENT
        volts_client_entry = self._DEFAULT_VOLTS_CLIENT_ENTRY
        success = Ramper.ramp_volts(
            self, volts_client, volts_client_entry, final_volts, total_time, time_steps,
        )

        return success

    def ramp_volts_slew(self, final_volts: float, slew_rate: float):
        """ Ramps the volts of the module up to a target following a slew rate

        Arguments:
            final_volts {float} -- final volts goal
            slew_rate {float} -- wanted slew rate

        Returns:
            bool -- True if the ramp was successful
        """
        success = Ramper.ramp_volts_slew(self, final_volts, slew_rate)

        return success
