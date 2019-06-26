import inspect
from types import ModuleType

# Ignore PyImportSortBear, PyUnusedCodeBear
from typing import Dict, Any

# This function is not defined for Python < 3.5
iscoroutinefunction = getattr(inspect, "iscoroutinefunction", lambda f: False)
iscoroutine = getattr(inspect, "iscoroutine", lambda f: False)

# Sentinel value for cases when some options are not specified
# For example could help to distinguish cases when `None` is a desired value for `default`
NOT_SET = object()


def import_string(path):
    # type: (str) -> ModuleType
    """Import given string and return the module."""
    if "." not in path:
        return __import__(path)
    parents, module = path.rsplit(".", 1)
    imported = __import__(parents, fromlist=[module])
    return getattr(imported, module)


def flatten_dict(dictionary):
    """Iterate over dict levels with producing [k_1, k_2, ...], value where the first list is a path to the value."""
    for key, value in dictionary.items():
        if isinstance(value, dict) and value:
            for sub_key, sub_value in flatten_dict(value):
                yield [key] + sub_key, sub_value
        else:
            yield [key], value


def rebuild_dict(data, callback):
    """Re-build a dict with given callback applied to all values."""
    new = {}  # type: Dict[Any, Any]
    for key, value in flatten_dict(data):
        current_level = new
        # Could be better
        for k in key[:-1]:
            current_level = new.setdefault(k, {})
        current_level[key[-1]] = callback(value)
    return new
