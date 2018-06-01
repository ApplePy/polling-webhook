import importlib.machinery
import os.path

# importlib variables
_SUFFIXES = list(set(
    importlib.machinery.SOURCE_SUFFIXES +
    importlib.machinery.DEBUG_BYTECODE_SUFFIXES +
    importlib.machinery.OPTIMIZED_BYTECODE_SUFFIXES +
    importlib.machinery.BYTECODE_SUFFIXES +
    importlib.machinery.EXTENSION_SUFFIXES
))
_BLACKLIST = {"__pycache__", "__init__.py", "api.py"}
_PLUGIN_FOLDER = os.path.dirname(__file__)

# Plugins and required properties
_POLL_PLUGINS = {}
_HOOK_PLUGINS = {}
_MIN_POLL_API_VERSION = 1
_MIN_HOOK_API_VERSION = 1

_ERROR_TEMPLATES = {
    "BAD_API": "Skipping '{0}' due to incompatible API version.",
    "BAD_HEADER": "Skipping '{0}' since it does not conform to plugin interface."
}


def _validate_module_name(name):
    """Check that the name of a file is a python file or the name of a python package."""
    location = os.path.join(_PLUGIN_FOLDER, name).lower()

    # Skip non-package directories
    if os.path.isdir(location) and "__init__.py" not in os.listdir(location):
        return False

    # Skip files with wrong suffix
    suffix_check_results = [name.endswith(x) for x in _SUFFIXES]
    if os.path.isfile(location) and True not in suffix_check_results:
        return False

    return True


def _extract_module_name(name):
    """Extract the name of the module/file from the name, stripping out extensions"""
    location = os.path.join(_PLUGIN_FOLDER, name).lower()

    # Extract package name
    module_name = name
    if os.path.isfile(location):
        pieces = module_name.split(".")
        module_name = ".".join(pieces[:-1])

    return module_name


def _setup():
    """Import all compatible plugins."""
    poll_plugins = []
    hook_plugins = []
    possible_plugins = set(os.listdir(_PLUGIN_FOLDER)).difference(_BLACKLIST)

    # Find plugins
    for i in possible_plugins:
        # Check that this is a valid module
        if not _validate_module_name(i):
            continue

        # Import module
        module_name = _extract_module_name(i)
        module = importlib.import_module("." + module_name, package=__name__)

        # Module sorting and validation
        try:
            if "poll" in module.TYPE:
                if module.API_VERSION >= _MIN_POLL_API_VERSION:
                    poll_plugins.append(module)
                else:
                    print(_ERROR_TEMPLATES["BAD_API"].format(module_name))
            if "hook" in module.TYPE:
                if module.API_VERSION >= _MIN_HOOK_API_VERSION:
                    hook_plugins.append(module)
                else:
                    print(_ERROR_TEMPLATES["BAD_API"].format(module_name))
        except AttributeError:
            print(_ERROR_TEMPLATES["BAD_HEADER"].format(module_name))
        except SyntaxError:
            print(_ERROR_TEMPLATES["BAD_HEADER"].format(module_name))

    return poll_plugins, hook_plugins


_polls, _hooks = _setup()

# Save all found plugins
for plugin in _polls:
    _POLL_PLUGINS[plugin.NAME] = plugin

for plugin in _hooks:
    _HOOK_PLUGINS[plugin.NAME] = plugin
