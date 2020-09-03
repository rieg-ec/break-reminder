import json

def json_hook(dict_):
    """
    object_hook to convert values to integer
    """
    if isinstance(dict_, str):
        try:
            return int(dict_)
        except ValueError:
            return dict_
    elif isinstance(dict_, dict):
        return {k: json_hook(v) for k, v in dict_.items()}
    elif isinstance(dict_, list):
        return [json_hook(v) for v in dict_]
    else:
        return dict_
