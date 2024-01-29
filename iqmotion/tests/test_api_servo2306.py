import pytest
import iqmotion as iq


class TestApiServo2306:

    @pytest.fixture
    def com_port(self):
        return iq.SerialCommunicator("COM4")

    @pytest.fixture
    def vertiq_2306(self, com_port):
        return iq.Vertiq2306(com_port, 0, "servo")

    @pytest.fixture
    def client_list(self, vertiq_2306):
        return vertiq_2306.return_clients()

    def test_get_all(self, vertiq_2306, client_list):
        print('\n')
        for client in client_list:
            print(f"\ntesting {client}")
            responses = vertiq_2306.get_all(client)
            assert responses is not None

            for response in responses:
                print(f"testing {response}: {responses[response]}")
                # assert responses[response] is not None
