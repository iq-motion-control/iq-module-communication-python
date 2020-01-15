
import json
import os
from abc import ABC, abstractmethod


class IqModule(ABC):

    @abstractmethod
    def set(self, client_name: str, client_entry_name: str, *args):
        """ this property is too abstract to understand. """

    @abstractmethod
    def get(self, client_name: str, client_entry_name: str, timeout=1):
        """ this property is too abstract to understand. """

    @abstractmethod
    def get_all(self, client_name: str, client_entry_name: str, timeout=1):
        """ this property is too abstract to understand. """

    @abstractmethod
    def save(self, client_name: str, client_entry_name: str):
        """ this property is too abstract to understand. """

    @abstractmethod
    def save_all(self, client_name: str):
        """ this property is too abstract to understand. """

    @abstractmethod
    def get_async(self, client_name: str, client_entry_name: str):
        """ this property is too abstract to understand. """

    @abstractmethod
    def update_replies(self):
        """ this property is too abstract to understand. """

    @abstractmethod
    def is_fresh(self, client_name: str, client_entry_name: str):
        """ this property is too abstract to understand. """

    @abstractmethod
    def get_reply(self, client_name: str, client_entry_name: str):
        """ this property is too abstract to understand. """

    @abstractmethod
    def list_clients(self):
        """ this property is too abstract to understand. """

    @abstractmethod
    def list_client_entries(self, client_name: str):
        """ this property is too abstract to understand. """
