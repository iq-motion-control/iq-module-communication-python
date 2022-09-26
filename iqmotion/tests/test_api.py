import iqmotion as iq
import pprint as pp
import json


class TestAPI:
    com = iq.SerialCommunicator("COM7")
    vertiq = iq.Vertiq8108(com, 0)

    def test_get_set(self):
        client_name = "brushless_drive"
        client_entry_name = "drive_volts_addition"
        response = TestAPI.vertiq.get(client_name, client_entry_name)
        print(response)
        assert response is not None



    def test_get_all(self):
        # com = iq.SerialCommunicator("COM7")
        # vertiq = iq.Vertiq8108(com, 0)
        print('\n')
        pp.pprint(TestAPI.vertiq.get_all("brushless_drive"))
        responses = TestAPI.vertiq.get_all("brushless_drive")

        with open("test_resources/Vertiq8108DefaultUndefinedDefinitions.json", 'r') as undefined_definitions:
            undefined_defs = json.load(undefined_definitions)

        with open("test_resources/Vertiq8108DefaultDefinedDefinitions.json", 'r') as defined_definitions:
            defined_defs = json.load(defined_definitions)

        for response in responses:
            print(f"testing {response}")

            if response in undefined_defs:
                assert responses[response] is None
            # if response in defined_defs:
            #     if responses[response] is None:
            #         print(f"{response} returned None")
