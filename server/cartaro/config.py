import json

# Singleton class
class Config:
    """Class that represents configuration."""

    __instance = None

    def __init__(self, filename=None):
        if not Config.__instance:
            if filename == None:
                raise TypeError("Must Specify a Filename")
            Config.__instance = Config.__Instance(filename)

    def force_reload(self):
        Config.__instance.reload()

    def __getattr__(self, name):
        return getattr(Config.__instance, name)

    @classmethod
    def initialize(cls, conf):
        # Init singleton instance of Config
        cfg = Config(conf)
        return cfg

    # --------------------------------------------------------------------------
    class __Instance:
        def __init__(self, filename):
            self.__filename = filename
            self.__read_file()

        def __read_file(self):
            with open(self.__filename, 'r') as stream:
                try:
                    data = json.load(stream)
                    self.settings = data.copy()
                except Exception as exc:
                    raise Exception(F"Error reading config file {exc.message}")

        def reload(self):
            self.__read_file()

        def get(self, name, default=None):
            value = self.settings

            parts = name.split(':')
            for part_name in parts:
                value = value.get(part_name, default)
                if value == default:
                    break

            return value

        def get_all(self):
            return self.settings

        def set(self, name, value):
            settings = self.settings

            parts = name.split(':')
            key = parts.pop()
            for sub_section in parts:
                sub = settings.get(sub_section)
                if sub:
                    settings = sub
                # Create the sub-section if it does not exist
                else:
                    settings[sub_section] = {}
                    settings = settings[sub_section]

            settings[key] = value
