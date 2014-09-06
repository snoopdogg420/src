import json
import os


class Settings:
    def __init__(self, filename):
        self.filename = filename

        self.data = {}
        self.read()

    def read(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                self.data = json.load(f)
        else:
            self.write()

    def write(self):
        with open(self.filename, 'w') as f:
            json.dump(self.data, f)

    def set(self, key, value):
        self.data[key] = value
        self.write()

    def remove(self, key, value):
        if key in self.data:
            del self.data[key]
            self.write()

    def get(self, key, default=None):
        if key in self.data:
            return self.data[key]
        return default

    def all(self):
        return self.data.keys()
