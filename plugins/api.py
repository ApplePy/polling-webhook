from . import _HOOK_PLUGINS as HOOKS, _POLL_PLUGINS as POLLS


def get_poll_plugin(name, url, extra_data=None):
    return POLLS[name].Poll(url, extra_data)


def get_hook_plugin(name, url, extra_data=None):
    return HOOKS[name].Hook(url, extra_data)
