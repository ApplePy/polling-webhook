from . import _HOOK_PLUGINS as HOOKS, _POLL_PLUGINS as POLLS


class PluginNotFound(Exception):
    def __init__(self, *args, **kwargs):
        super(PluginNotFound, self).__init__(*args, **kwargs)


def get_poll_plugin(name, url, extra_data=None):
    """Returns an instantiation of the requested poll plugin."""
    try:
        return POLLS[name.lower()].Poll(url, extra_data)
    except KeyError as e:
        raise PluginNotFound(e)


def get_hook_plugin(name, url, extra_data=None):
    """Returns an instantiation of the requested hook plugin."""
    try:
        return HOOKS[name.lower()].Hook(url, extra_data)
    except KeyError as e:
        raise PluginNotFound(e)
