from iqmotion.communication.client_entry_abstract import ClientEntryAbstract
from iqmotion.communication.client_entry_abstract import ClientEntryValues

from iqmotion.communication.client_entry_payload import AccessType
from iqmotion.communication.client_entry_payload import ClientEntryPayloadMaker
from iqmotion.communication.client_entry_payload import ClientEntryPayloadData


class ClientEntry(ClientEntryAbstract):
    def __init__(self, module_idn, client_entry_dict: dict):
        super(ClientEntry, self).__init__(module_idn,
                                          client_entry_dict,
                                          ClientEntryPayloadMaker())

    def make_get_payload(self):
        pass

    def make_set_payload(self, args=None):
        if not isinstance(args, (type(None), list, int, float, tuple)):
            raise TypeError

        # TODO: need to check if you are allowed to make packet first
        if args == None:
            print("NO VALUES")
            return None

        payload_data = self._concatenate_payload_data(
            self._module_idn, AccessType.SET, self._values, args)

        payload = self._payload_maker.make_payload(payload_data)

        return payload

    def make_save_payload(self, value):
        pass

    def list(self):
        return self._values.__str__()

    def _concatenate_payload_data(self, module_idn, access_type, client_entry_values, payload_values):
        payload_data = ClientEntryPayloadData(client_entry_values.param_idn,
                                              module_idn,
                                              access_type,
                                              client_entry_values.format,
                                              payload_values)

        return payload_data
