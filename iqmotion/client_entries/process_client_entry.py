# from iqmotion.client_entries.client_entry import ClientEntry
# from iqmotion.client_entries.client_entry_data import ClientEntryData

# from dataclasses import dataclass


# @dataclass
# class ProcessClientEntryData(ClientEntryData):
#     type_idn: bytes
#     payload_type: bytes
#     format: str
#     unit: str
#     name: str

#     def __init__(self, client_entry_dict: dict):
#         self.type_idn = client_entry_dict["type_idn"]
#         self.payload_type = client_entry_dict["payload_type"]
#         self.format = client_entry_dict["format"]
#         self.unit = client_entry_dict["unit"]
#         self.name = client_entry_dict["param"]

#     def __str__(self):
#         return "{0:10} | {2:32} {3:4} {4}".format(self.type_idn, self.name, self.format, self.unit)


# class ProcessClientEntry(ClientEntry):
#     def __init__(self, client_entry_data_dict: dict):
#         self._fresh = 0
#         self._value = None
#         self._data = ProcessClientEntryData(client_entry_data_dict)

#     def read_message(self, msg):
#         """ Takes in a message, parses it and save the payload as its value
#         """
#         pass

#     @property
#     def fresh(self):
#         return self._fresh

#     @property
#     def value(self):
#         return self._value

#     @value.setter
#     def value(self, value):
#         pass

#     @property
#     def data(self):
#         return self._data
