import os
import json


def get_save_file(json_type, data=None):
    directory = "data"
    os.makedirs(directory, exist_ok=True)

    if json_type == 1:
        file_name = "user.json"
    elif json_type == 2:
        file_name = "system.json"
    elif json_type == 3:
        file_name = "server.json"

    file_path = os.path.join(directory, file_name)
    if data is None:
        return file_path

    # Write data to a JSON file
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
