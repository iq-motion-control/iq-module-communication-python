import json
import os


class IqModuleJsonParser:
    @staticmethod
    def parse(module_file_name: str):

        file_path = os.path.join(
            os.path.dirname(__file__), ("module_files/" + module_file_name)
        )

        with open(file_path) as json_file:
            module_file = json.load(json_file)

        return module_file
