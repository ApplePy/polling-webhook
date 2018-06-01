#! /usr/bin/env python3
from config import Config
import sys
import os.path
from history import History
import plugins.api


def main(config_path):
    config_obj = Config(config_path)
    # TODO: Custom history.json location
    url_history = History()

    for poll in config_obj["polls"]:
        inbound = poll["inbound"]
        outbound = poll["outbound"]
        in_url = inbound["url"]

        # Get plugin and get latest version
        try:
            poll_plugin = plugins.api.get_poll_plugin(inbound["plugin"], in_url, inbound["plugin_data"])
            tag_name, version_number = poll_plugin.get_version()

            # Check if updates needed
            update_needed = in_url not in url_history or version_number > url_history[in_url]
            if not update_needed:
                print("No update required for {0}, version {1}.".format(in_url, version_number))
                continue

            # Call hook
            print("Update from {0} - old version: {1}, new version: {2}".format(
                in_url,
                url_history.get(in_url, "0.0.0"),
                version_number))
            hook_plugin = plugins.api.get_hook_plugin(outbound["plugin"], outbound["url"], inbound["plugin_data"])
            hook_plugin.trigger_webhook(tag_name)

            # Update history
            url_history[in_url] = version_number
            url_history.save()
        # TODO: Save result of process to log and/or InfluxDB
        # TODO: Proper logging mechanism
        except plugins.api.PluginNotFound as e:
            print("Plugin {0} not found, skipping update.".format(e))


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
