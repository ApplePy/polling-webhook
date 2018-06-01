#! /usr/bin/env python3
from config import Config
import sys
import os.path
import plugins.api


def main(config_path):
    config_obj = Config(config_path)

    for poll in config_obj["polls"]:
        inbound = poll["inbound"]
        outbound = poll["outbound"]

        test = plugins.api.get_poll_plugin(inbound["plugin"], inbound["url"], inbound["plugin_data"])
        test.success()
        # TODO: Define plugin interface
        # TODO: Write update-checking (maybe offload to plugin as well?)
        # TODO: Write call to corresponding hook
        # TODO: Save result of process to log and/or InfluxDB

    test2 = plugins.api.get_hook_plugin("github", "stuff")
    test2.success()


if __name__ == "__main__":
    config_yaml = os.path.join(os.path.dirname(__file__), "config.yaml")

    # Catch if there's a custom configuration file
    if len(sys.argv) > 1:
        if os.path.isfile(sys.argv[1]):
            config_yaml = sys.argv[1]
        else:
            print("Invalid configuration file path!")
            sys.exit(1)

    main(config_yaml)


# TODO: Proper logging mechanism
