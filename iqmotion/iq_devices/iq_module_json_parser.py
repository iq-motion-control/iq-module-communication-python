import json
import os


class IqModuleJsonParser:
    @staticmethod
    def parse_default_modules(module_file_name: str):

        file_path = os.path.join(
            os.path.dirname(__file__), ("module_files/" + module_file_name)
        )

        with open(file_path) as json_file:
            module_file = json.load(json_file)

        return module_file

    @staticmethod
    def parse_module(module_file_path: str):

        with open(module_file_path) as json_file:
            module_file = json.load(json_file)

        return module_file
