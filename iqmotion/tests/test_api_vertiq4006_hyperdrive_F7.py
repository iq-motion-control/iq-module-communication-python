import pytest
import iqmotion as iq
from time import sleep

class TestApiHyperdrive4006:

    @pytest.fixture
    def com_port(self):
        return iq.SerialCommunicator("COM4")

    @pytest.fixture
    def vertiq_4006(self, com_port):
        return iq.Vertiq4006(com_port, 0)

    @pytest.fixture
    def client_list(self, vertiq_4006):
        return vertiq_4006.return_clients()


    def test_esc_propeller_input_parser(self, vertiq_4006):
        print('\n')
        esc_propeller_input_parser = "esc_propeller_input_parser"
        esc_propeller_input_parser_entries = vertiq_4006.return_client_entries(esc_propeller_input_parser)
        torque_max = "torque_max"
        assert torque_max in esc_propeller_input_parser_entries

        print(f"Test getting {torque_max} default value")
        value = vertiq_4006.get_retry(esc_propeller_input_parser, torque_max)
        print(f"{torque_max}={value}")
        assert value is not None

        t_max = 0.34
        print(f"Test setting {torque_max}: {t_max}")
        status = vertiq_4006.set_verify(esc_propeller_input_parser, torque_max, t_max)
        assert status is True

        print(f"Test getting {torque_max}")
        value = round(vertiq_4006.get_retry(esc_propeller_input_parser, torque_max), 2)
        assert value == t_max


    def test_pmc(self, vertiq_4006):
        pmc = "propeller_motor_control"
        print(f"\n Testing {pmc}")
        ctrl_torque = "ctrl_torque"

        pmc_entries = vertiq_4006.get_all(client_name=pmc)

        print(f"Testing {ctrl_torque}")
        assert ctrl_torque in pmc_entries

        print(f"Testing get_retry {ctrl_torque} default value")
        value = vertiq_4006.get_retry(client_name=pmc, client_entry_name=ctrl_torque)
        print(f"{ctrl_torque} = {value}")
        assert value is not None

        new_value = 0.10
        print(f"Testing set_verify {ctrl_torque}: {new_value}")
        status = vertiq_4006.set_verify(client_name=pmc, client_entry_name=ctrl_torque, values=new_value)
        assert status is True

        print(f"Testing get_retry {ctrl_torque}")
        value = round(vertiq_4006.get_retry(client_name=pmc, client_entry_name=ctrl_torque), 2)
        print(f"{ctrl_torque} = {value}")
        assert value == new_value


        sleep(1) # Allows the motor to spin for 1 second using ctrl_torque
        print(f"Setting coast")
        vertiq_4006.coast()


    def test_get_all(self, vertiq_4006, client_list):
        print('\n')
        for client in client_list:
            print(f"\ntesting {client}")
            responses = vertiq_4006.get_all(client)
            assert responses is not None

            for response in responses:
                print(f"testing {response}: {responses[response]}")
                # assert responses[response] is not None
