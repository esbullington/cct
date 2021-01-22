import os
import ujson


# this class holds a configuration for the device
# the configuration is stored to a file
class Config:

    # loads a configuration from the specified file,
    # and initializes an instance of Config
    def __init__(self, config_filename):
        self.filename = config_filename
        self.values = self.load_config(config_filename)

    # returns a value of the specified parameter if the parameter exists
    # otherwise, returns an empty string
    def get(self, name):
        if name in self.values:
            return self.values[name]
        return ''

    # updates the specified parameter
    def set(self, name, value):
        self.values[name] = value

    # stores the configuration to the specified file
    def store(self):
        with open(self.filename, 'w') as f:
            f.write(ujson.dumps(self.values))

    # loads a configuration from the specified file
    @staticmethod
    def load_config(config_filename):
        try:
            with open(config_filename) as f:
                return ujson.load(f)
        except Exception as exc:
            print("Error opening config file: {}".format(str(exc)))
