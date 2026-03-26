import pytest
import iqmotion as iq

class TestApiServo4006:

    @pytest.fixture
    def com_port(self):
        return iq.SerialCommunicator("COM4")

    @pytest.fixture
    def vertiq_4006(self, com_port):
        return iq.Vertiq4006(com_port, 0, "servo")

    @pytest.fixture
    def client_list(self, vertiq_4006):
        return vertiq_4006.return_clients()


    def test_ifci(self, vertiq_4006):
        print("\n")
        ifci = "iquart_flight_controller_interface"
        servo_cvi = "servo_cvi"

        ifci_entries = vertiq_4006.get_all(client_name=ifci)

        print(f"Testing {servo_cvi}")
        assert servo_cvi in ifci_entries

        print(f"Testing get_retry {servo_cvi} default value")
        value = vertiq_4006.get_retry(client_name=ifci, client_entry_name=servo_cvi)
        print(f"{servo_cvi} = {value}")
        assert value is not None

        new_value = 6
        print(f"Testing set_verify {servo_cvi}: {new_value}")
        status = vertiq_4006.set_verify(client_name=ifci, client_entry_name=servo_cvi, values=new_value)
        assert status is True

        print(f"Testing get_retry {servo_cvi}")
        value = vertiq_4006.get_retry(client_name=ifci, client_entry_name=servo_cvi)
        print(f"{servo_cvi} = {value}")
        assert value == new_value

        vertiq_4006.flush_input_com_buffer()

    def test_uavcan_node(self, vertiq_4006):
        uavcan_node = "uavcan_node"
        print(f"\nTesting {uavcan_node}")
        actuator_id = "actuator_id"

        uavcan_node_entries = vertiq_4006.get_all(client_name=uavcan_node)

        print(f"Testing {actuator_id}")
        assert actuator_id in uavcan_node_entries

        print(f"Testing get_retry {actuator_id} default value")
        value = vertiq_4006.get_retry(client_name=uavcan_node, client_entry_name=actuator_id)
        print(f"{actuator_id} = {value}")
        assert value is not None

        new_value = 6
        print(f"Testing set_verify {actuator_id}: {new_value}")
        status = vertiq_4006.set_verify(client_name=uavcan_node, client_entry_name=actuator_id, values=new_value)
        assert status is True

        print(f"Testing get_retry {actuator_id}")
        value = vertiq_4006.get_retry(client_name=uavcan_node, client_entry_name=actuator_id)
        print(f"{actuator_id} = {value}")
        assert value == new_value

    def test_get_hobby_input(self, vertiq_4006):
        print("\n")
        hobby = "hobby_input"

        # hobby_entries = vertiq_4006.get_all(client_name=hobby)
        # assert hobby_entries is not None

        entry = "allowed_protocols"
        value = vertiq_4006.get_retry(client_name=hobby, client_entry_name=entry)
        print(f"{entry=}: {value}")
        assert value is not None

        entry = "protocol"
        value = vertiq_4006.get_retry(client_name=hobby, client_entry_name=entry)
        print(f"{entry=}: {value}")
        assert value is not None
