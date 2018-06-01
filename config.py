import yaml


class Config(object):
    def __init__(self, config_path):
        super(Config, self).__init__()
        self._path = config_path
        self._config = self._get_config()

    def __getitem__(self, item):
        return self._config[item]

    @staticmethod
    def _valid_config(config):
        """Validate that a config file contains all necessary fields."""
        return "polls" in config and "config" in config

    def _get_config(self):
        """Retrieve the contents of a valid config file."""
        config = {"polls": []}

        # Retrieve configuration settings
        with open(self._path, "r") as config_stream:
            loaded_config = yaml.safe_load(config_stream)

            # Content sanity check
            if self._valid_config(loaded_config):
                config = loaded_config
            else:
                raise SyntaxError("Malformed configuration file!")

        return config
