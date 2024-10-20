import json


class User:
    def __init__(self, name, password):
        self.name = name
        self.password = password

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)
