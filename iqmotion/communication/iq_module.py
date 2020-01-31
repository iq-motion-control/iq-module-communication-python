
import json
import os
from abc import ABC, abstractmethod


class IqModule(ABC):
    """ IqModule is an interface class for all the modules made by iq

    The implemenation handles the specific of each methods and where to look for the clients
    """

    @abstractmethod
    def set(self, client_name: str, client_entry_name: str, *args):
        """ Sets a value to the module with a message formed by a client and client entry

        Args:
            client_name (str): name of client
            client_entry (str): name of client entry
            *args (): value(s) to be set
        """
        """ this property is too abstract to understand. """

    @abstractmethod
    def get(self, client_name: str, client_entry_name: str, timeout=1):
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
        """ this property is too abstract to understand. """

    @abstractmethod
    def get_all(self, client_name: str, client_entry_name: str, timeout=1):
        """ Gets all the value define by the client (all of its client entries).

        This call is blocking and will wait until it gets a reply or timeouts for every get call

        Args:
            client_name (str): name of client
            timeout=1 (int): blocking timeout while waiting for a reply

        Returns:
            replies (dict{str:format}): all the successful replies of the module
        """
        """ this property is too abstract to understand. """

    @abstractmethod
    def save(self, client_name: str, client_entry_name: str):
        """ Saves a the client and client entry value already set on the module

        Args:
            client_name (str): name of client
            client_entry (str): name of client entry
        """
        """ this property is too abstract to understand. """

    @abstractmethod
    def save_all(self, client_name: str):
        """ Saves all the values of the client already set on the module

        Args:
            client_name (str): name of client
        """
        """ this property is too abstract to understand. """

    @abstractmethod
    def get_async(self, client_name: str, client_entry_name: str):
        """ Sends a asynchroniously get request to the module

        This call is non blocking, to read the reply you have to call "update reply" and then "get_reply" if that client entry is fresh

        Args:
            client_name (str): name of client
            client_entry (str): name of client entry
        """
        """ this property is too abstract to understand. """

    @abstractmethod
    def update_replies(self):
        """ Reads all the bytes available in the Communication queue and stores them in the right client entries
        """
        """ this property is too abstract to understand. """

    @abstractmethod
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
        """ this property is too abstract to understand. """

    @abstractmethod
    def get_reply(self, client_name: str, client_entry_name: str):
        """ Reads the reply stored in the client entry

        This method is normally called after checking if the value is fresh with "is_fresh" 

        Args:
            client_name (str): name of client
            client_entry (str): name of client entry

        Return:
            reply (format): value stored in client_entry
        """
        """ this property is too abstract to understand. """

    @abstractmethod
    def list_clients(self):
        """ Displays all the clients available with this module 
        """
        """ this property is too abstract to understand. """

    @abstractmethod
    def list_client_entries(self, client_name: str):
        """ Displays all the client entries available for that client

        Args:
            client_name (str): name of client
        """
        """ this property is too abstract to understand. """
