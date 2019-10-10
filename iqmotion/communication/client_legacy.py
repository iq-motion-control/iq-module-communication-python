import json
import numpy as np
import sys
import os
import time
import struct
from dataclasses import dataclass

from iqmotion.communication.custom_error import ClientError


class Client:
    # Private Members
    _inbox = {}
    _outbox = {}

    _GET = 0
    _SET = 1
    _SAVE = 2
    _REPLY = 3

    # Message specifications for typed setters and replies

    _fspec = {"Type": 0,
              "Fields": {'sub': 'uint8', 'access': 'uint8', 'value': 'single'}}
    _Ispec = {"Type": 0,
              "Fields": {'sub': 'uint8', 'access': 'uint8', 'value': 'uint32'}}
    _Hspec = {"Type": 0,
              "Fields": {'sub': 'uint8', 'access': 'uint8', 'value': 'uint16'}}
    _Bspec = {"Type": 0,
              "Fields": {'sub': 'uint8', 'access': 'uint8', 'value': 'uint8'}}
    _ispec = {"Type": 0,
              "Fields": {'sub': 'uint8', 'access': 'uint8', 'value': 'int32'}}
    _hspec = {"Type": 0,
              "Fields": {'sub': 'uint8', 'access': 'uint8', 'value': 'int16'}}
    _bspec = {"Type": 0,
              "Fields": {'sub': 'uint8', 'access': 'uint8', 'value': 'int8'}}
    _vspec = {"Type": 0,
              "Fields": {'sub': 'uint8', 'access': 'uint8'}}

    def __init__(self, com, filename, obj_id=0, timeout=0.2):
        try:
            self._com = com
            self._file_path = os.path.join(
                os.path.dirname(__file__), ('clients/' + filename))
            self._filename = filename
            self._obj_id = obj_id
            self._timeout = timeout

            with open(self._file_path) as json_file:
                input = json.load(json_file)

            # TODO: add argument checks

            # Fill ordered list of disp_entry objects.
            # Display entries are ordered as in json file
            self._disp_entry = input

            # TODO: % Fill map for checking whether param names are deprecated.

            # Fill inbox map with mail_entry objects.
            # The inbox map is keyed by type_idn/param_idn, and there is an
            # exact one-to-one correspondance between keys and objects.
            for entry in input:
                s = {"type_idn": entry["type_idn"],
                     "param_idn": entry["param_idn"],
                     "format": entry["format"]}

                if not entry["format"]:
                    s["format"] = " "

                if s["format"] == "f" or s["format"] == "I":
                    s["value"] = 0

                s["is_fresh"] = False

                long_idn = (np.uint32(s["type_idn"]) << 8
                            + np.uint32(s["param_idn"]))

                if long_idn not in self._inbox.keys():
                    self._inbox[long_idn] = s

            # Fill outbox map with mail_entry objects.
            # The outbox map is keyed by parameter name. Keys are unique,
            # but multiple keys may retrieve the same object.
            for entry in input:
                if entry["param"] not in self._outbox.keys():
                    long_idn = (np.uint32(entry["type_idn"]) << 8
                                + np.uint32(entry["param_idn"]))
                    value = self._inbox[long_idn]
                    self._outbox[entry["param"]] = value
                else:
                    pass
                    raise ClientError(
                        "Parameter list file invalid. Param name is repeated")

        except ClientError as e:
            print(e.message)

        except:
            print("Unexpected error:", sys.exc_info()[0])

    def list(self):
        print("\nParameter set loaded from: {0}".format(self._filename))
        print("This object ID: {0}".format(self._obj_id))

        for entry in self._disp_entry:
            m = self._outbox[entry["param"]]
            print("    {0:3} | {1:2}: {2:32} {3:4} {4}".format(
                m["type_idn"], m["param_idn"], entry["param"], m["format"], entry["unit"]))
        print("\n")

    def get(self, param):
        try:
            item = self._outbox[param]

            msg = {"sub": item["param_idn"],
                   "access": self._GET + self._obj_id*4}

            field = {"sub": "uint8",
                     "access": "uint8"}

            spec = {"Type": item["type_idn"],
                    "Fields": field}

            self._com.Flush()
            self._com.SendMsg(spec, msg)

            item["is_fresh"] = False
            val = None

            end_time = time.perf_counter() + self._timeout
            while time.perf_counter() < end_time:
                self.update()
                if(item["is_fresh"]):
                    val = item["value"]

            if val is None:
                raise ClientError(
                    "get({0}) timeout ({1}s)".format(param, self._timeout))

        except ClientError as e:
            print(e.message)

        except:
            print("Unexpected error:", sys.exc_info()[0])

        return val

    def get_retry(self, param, retries):
        pass

    def get_all(self):
        pass

    def set(self, param, varargin):
        pass

    def set_all(self, s):
        pass

    def set_verify_all(self, s):
        pass

    def set_verify(self, param, varargin):
        pass

    def save(self, param):
        pass

    def save_all(self):
        pass

    def update(self):
        """ Read from device and update parameter table"""

        self._com.GetBytes()
        type_idn, packet = self._com.PeekPacket()  # check for message

        if type_idn and packet:  # if we got a message, and that message is not empty
            param_idn = packet[0]
            # might be wrong, check matlab function
            long_idn = self._CalculateLongIdn(type_idn, param_idn)

            if long_idn in self._inbox.keys():
                item = self._inbox[long_idn]
                msg_obj_id = packet[1] >> 2
                access = packet[1] - 4 * msg_obj_id

                if access == self._REPLY and msg_obj_id == self._obj_id:
                    # TODO: make this a dictinary instead of elif clause
                    try:
                        if item["format"] == 'f':
                            spec = self._fspec
                        elif item["format"] == 'I':
                            spec = self._Ispec
                        elif item["format"] == 'B':
                            spec = self._Bspec
                        elif item["format"] == 'i':
                            spec = self._ispec
                        elif item["format"] == 'h':
                            spec = self._hspec
                        elif item["format"] == 'b':
                            spec = self._bspec
                        elif item["format"] == ' ':
                            spec = self._vspec
                        else:
                            raise ClientError("Format not yet supported")

                    except ClientError as e:
                        print(e.message)

                    except:
                        print("Unexpected error:", sys.exc_info()[0])

                    spec["Type"] = item.type_idn
                    msg = UnpackMsg(spec, packet)
                    item["value"] = msg["value"]  # make sure you make a dict
                    item["is_fresh"] = True

    def _CalculateLongIdn(self, type_idn, param_idn):
        return (np.uint32(type_idn) << 8 + np.uint32(param_idn))


def UnpackMsg(msg_spec, pkt):
    # TODO: maybe check that pkt is a uint8_t ?

    # TODO: change all handling to char
    type_string_char_pairs = {'uint8': 'B',
                              'int8': 'b',
                              'uint16': 'H',
                              'int16': 'h',
                              'uint32': 'I',
                              'int32': 'i',
                              'single': 'f',  # float
                              'double': 'd',
                              'uint64': 'Q',
                              'int64': 'q'}

    spec_fields = msg_spec["Fields"]
    ind = 0
    msg = {}

    # ordered dic only true in pyton 3.7, be careful
    for field in spec_fields.keys():
        numerical_type = type_string_char_pairs[spec_fields["field"]]

        # Get sizof numerical type
        nbytes = NumBytes(numerical_type)
        # typecast bytes in packet to correct type
        # TODO: check pkt indices
        val = struct.pack(numerical_type, pkt[ind:(ind+nbytes)])
        # pop elements from packet corresponding to val
        ind += nbytes
        # populate msg struct with correct value
        msg[field] = val

    return msg


def NumBytes(type_string):
    string_bytes_pairs = {'uint8': 1,
                          'int8': 1,
                          'uint16': 2,
                          'int16': 2,
                          'uint32': 4,
                          'int32': 4,
                          'single': 4,
                          'double': 8,
                          'int64': 8,
                          'uint64': 8}

    if type_string in string_bytes_pairs.keys():
        return string_bytes_pairs[type_string]
    else:
        return 0


def FakeMethod(self, a):
    print(a)
