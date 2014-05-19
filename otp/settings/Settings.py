import gzip
import json


class Settings:
    def __init__(self, filename):
        self.filename = filename

        self.data = {}
        self.read()

    def read(self):
        try:
            f = gzip.open(self.filename, 'rb')
            content = f.read()
            f.close()
            self.data = json.loads(content)
        except:
            self.write()

    def write(self):
        f = gzip.open(self.filename, 'wb')
        f.write(json.dumps(self.data))
        f.close()

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
