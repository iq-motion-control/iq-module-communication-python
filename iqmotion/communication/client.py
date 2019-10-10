
import json
import numpy as np
import sys
import os
import time
import struct
from dataclasses import dataclass

from iqmotion.communication.custom_error import ClientError
from iqmotion.communication.packet_maker import PacketMaker


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
            self._packet_maker = PacketMaker()
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

    def get(self, param: str):
        try:
            if param not in self._outbox.keys():
                raise ClientError("client entry does not exists")
            item = self._outbox[param]

            msg = {"sub": item["param_idn"],
                   "access": self._GET + self._obj_id*4}

            field = {"sub": np.uint8,
                     "access": np.uint8}

            spec = {"Type": item["type_idn"],
                    "Fields": field}

            self._packet_maker.Make(spec, msg)
            # print(msg)
            # self._com.SendMsg(spec, msg)

        except ClientError as e:
            print(e.message)

        except:
            print("Unexpected error:", sys.exc_info()[0])

        # return val
