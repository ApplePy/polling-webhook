import json
import sys
import os.path


class History(dict):
    def __init__(self, path=os.path.join(os.path.dirname(__file__), "history.json"), *args, **kwargs):
        super(History, self).__init__(*args, **kwargs)
        self._path = path
        history = self.load_history()
        self.update(history)

    def load_history(self):
        """Loads previous version history from file."""
        try:
            with open(self._path, "r") as history_file:
                return json.load(history_file)
        except FileNotFoundError:
            print("History file not found, starting fresh.", file=sys.stderr)
            return {}
        except json.decoder.JSONDecodeError:
            print("Corrupted history, starting fresh.", file=sys.stderr)  # TODO: Proper logging
            return {}

    def save(self):
        """Saves new version history to file."""
        with open(self._path, "w") as history_file:
            json.dump(self, history_file)
