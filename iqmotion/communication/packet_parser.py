from iqmotion.communication.packet_state import PacketState


class PacketParser:
    """ PacketParser is the "context" class of a State Pattern for Packet States.
    It defines a single interface to parse a message from a packet using the correct State implementations
    """

    def __init__(self, state: PacketState):
        """ Creates a PacketParser object to interface with PacketState's implementation (depending on the com/packet queues)

        Arguments:
            state (PacketState): the PacketState implementation you want to use to parse your packet
        """
        self._current_state = state
        self._parsing_successful = False

    @property
    def succesful(self):
        return self._current_state.is_succesful

    @property
    def message(self):
        """ The message parsed by the PacketStates
        """
        return self._current_state.message

    def parse(self):
        """ Parse packet from initialized PacketState until PacketState is done
        """
        while not self._current_state.is_done:
            self._find_next_state()

    def _find_next_state(self):
        self._current_state.parse()
        self._current_state = self._current_state.find_next_state()
