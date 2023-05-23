import pytest
import iqmotion as iq


class TestAPI:
    @pytest.fixture
    def com_port(self):
        return iq.SerialCommunicator("COM4")

    @pytest.fixture
    def vertiq_8108(self, com_port):
        return iq.Vertiq8108(com_port, 0)

    @pytest.fixture
    def client_list(self, vertiq_8108):
        return vertiq_8108.return_clients()

    def test_brushless_drive_set(self, vertiq_8108, client_list):
        assert client_list is not None

        client_name = "brushless_drive"
        assert client_name in client_list

        client_entries = vertiq_8108.return_client_entries(client_name)
        assert client_entries is not None

        client_entry_name = "drive_mode"
        assert client_entry_name in client_entries

        print("\nSetting drive mode to 5 (coast)")
        status = vertiq_8108.set_verify(client_name, client_entry_name, 5)
        print(f"status: {status}")
        assert status is True
        print("Getting updated drive mode")
        response = vertiq_8108.get(client_name, client_entry_name)
        print(f"response: {response}")
        assert response is 5

    def test_get_all(self, vertiq_8108, client_list):
        print('\n')
        for client in client_list:
            print(f"\ntesting {client}")
            responses = vertiq_8108.get_all(client)
            assert responses is not None

            for response in responses:
                print(f"testing {response}: {responses[response]}")
                # assert responses[response] is not None
