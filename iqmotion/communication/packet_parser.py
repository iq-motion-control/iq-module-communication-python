from iqmotion.communication.packet_state import PacketState


class PacketParser():
    def __init__(self, state: PacketState):
        self._current_state = state
        self._parsing_successful = False

    @property
    def succesful(self):
        return self._current_state.is_succesful

    @property
    def message(self):
        return self._current_state.message

    def parse(self):
        while not self._current_state.is_done:
            self._find_next_state()

    def _find_next_state(self):
        self._current_state.parse()
        self._current_state = self._current_state.find_next_state()
