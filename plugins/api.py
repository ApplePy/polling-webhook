from . import _HOOK_PLUGINS as HOOKS, _POLL_PLUGINS as POLLS


def get_poll_plugin(name, url, extra_data=None):
    """Returns an instantiation of the requested poll plugin."""
    return POLLS[name.lower()].Poll(url, extra_data)


def get_hook_plugin(name, url, extra_data=None):
    """Returns an instantiation of the requested hook plugin."""
    return HOOKS[name.lower()].Hook(url, extra_data)
