import pytest
import iqmotion as iq

class TestApiSpeed4006:

    @pytest.fixture
    def com_port(self):
        return iq.SerialCommunicator("COM4")

    @pytest.fixture
    def vertiq_4006(self, com_port):
        return iq.Vertiq4006(com_port, 0)

    @pytest.fixture
    def client_list(self, vertiq_4006):
        return vertiq_4006.return_clients()

    def test_uavcan_node(self, vertiq_4006):
        uavcan_node = "uavcan_node"
        print(f"\nTesting {uavcan_node}")
        warning_enable_bitmask = "warning_enable_bitmask"
        error_enable_bitmask = "error_enable_bitmask"
        critical_enable_bitmask = "critical_enable_bitmask"
        error_count_configuration = "error_count_configuration"

        uavcan_node_entries = vertiq_4006.get_all(client_name=uavcan_node)

        print(f"Testing {warning_enable_bitmask}")
        assert warning_enable_bitmask in uavcan_node_entries

        print(f"Testing get_retry {warning_enable_bitmask} default value")
        value = vertiq_4006.get_retry(client_name=uavcan_node, client_entry_name=warning_enable_bitmask)
        print(f"{warning_enable_bitmask} = {value}")
        assert value is not None

        new_value = 6
        print(f"Testing set_verify {warning_enable_bitmask}: {new_value}")
        status = vertiq_4006.set_verify(client_name=uavcan_node, client_entry_name=warning_enable_bitmask, values=new_value)
        assert status is True

        print(f"Testing get_retry {warning_enable_bitmask}")
        value = vertiq_4006.get_retry(client_name=uavcan_node, client_entry_name=warning_enable_bitmask)
        print(f"{warning_enable_bitmask} = {value}")
        assert value is new_value

        print("\n")

        print(f"Testing {error_enable_bitmask}")
        assert error_enable_bitmask in uavcan_node_entries

        print(f"Testing get_retry {error_enable_bitmask} default value")
        value = vertiq_4006.get_retry(client_name=uavcan_node, client_entry_name=error_enable_bitmask)
        print(f"{error_enable_bitmask} = {value}")
        assert value is not None

        new_value = 2
        print(f"Testing set_verify {error_enable_bitmask}: {new_value}")
        status = vertiq_4006.set_verify(client_name=uavcan_node, client_entry_name=error_enable_bitmask, values=new_value)
        assert status is True

        print(f"Testing get_retry {error_enable_bitmask}")
        value = vertiq_4006.get_retry(client_name=uavcan_node, client_entry_name=error_enable_bitmask)
        print(f"{error_enable_bitmask} = {value}")
        assert value is new_value

        print("\n")

        print(f"Testing {critical_enable_bitmask}")
        assert critical_enable_bitmask in uavcan_node_entries

        print(f"Testing get_retry {critical_enable_bitmask} default value")
        value = vertiq_4006.get_retry(client_name=uavcan_node, client_entry_name=critical_enable_bitmask)
        print(f"{critical_enable_bitmask} = {value}")
        assert value is not None

        new_value = 2
        print(f"Testing set_verify {critical_enable_bitmask}: {new_value}")
        status = vertiq_4006.set_verify(client_name=uavcan_node, client_entry_name=critical_enable_bitmask, values=new_value)
        assert status is True

        print(f"Testing get_retry {critical_enable_bitmask}")
        value = vertiq_4006.get_retry(client_name=uavcan_node, client_entry_name=critical_enable_bitmask)
        print(f"{critical_enable_bitmask} = {value}")
        assert value is new_value

        print("\n")

        print(f"Testing {error_count_configuration}")
        assert error_count_configuration in uavcan_node_entries

        print(f"Testing get_retry {error_count_configuration} default value")
        value = vertiq_4006.get_retry(client_name=uavcan_node, client_entry_name=error_count_configuration)
        print(f"{error_count_configuration} = {value}")
        assert value is not None

        new_value = 2
        print(f"Testing set_verify {error_count_configuration}: {new_value}")
        status = vertiq_4006.set_verify(client_name=uavcan_node, client_entry_name=error_count_configuration, values=new_value)
        assert status is True

        print(f"Testing get_retry {error_count_configuration}")
        value = vertiq_4006.get_retry(client_name=uavcan_node, client_entry_name=error_count_configuration)
        print(f"{error_count_configuration} = {value}")
        assert value is new_value

    def test_tsm(self, vertiq_4006):
        tsm = "throttle_source_manager"
        print(f"\n Testing {tsm}")
        current_active_throttle_source = "current_active_throttle_source"  # GET only

        tsm_entries = vertiq_4006.get_all(client_name=tsm)

        print(f"Testing {current_active_throttle_source}")
        assert current_active_throttle_source in tsm_entries

        print(f"Testing get_retry {current_active_throttle_source} default value")
        value = vertiq_4006.get_retry(client_name=tsm, client_entry_name=current_active_throttle_source)
        print(f"{current_active_throttle_source} = {value}")
        assert value is not None

    def test_mtac(self, vertiq_4006):
        mtac = "multi_turn_angle_control"
        print(f"\n Testing {mtac}")
        trajectory_queue_length = "trajectory_queue_length"  # GET only

        mtac_entries = vertiq_4006.get_all(client_name=mtac)
        print(f"Testing {trajectory_queue_length}")
        assert trajectory_queue_length in mtac_entries

        print(f"Testing get_retry {trajectory_queue_length} default value")
        value = vertiq_4006.get_retry(client_name=mtac, client_entry_name=trajectory_queue_length)
        print(f"{trajectory_queue_length} = {value}")
        assert value is not None



    def test_get_all(self, vertiq_4006, client_list):
        print('\n')
        for client in client_list:
            print(f"\ntesting {client}")
            responses = vertiq_4006.get_all(client)
            assert responses is not None

            for response in responses:
                print(f"testing {response}: {responses[response]}")
                # assert responses[response] is not None
