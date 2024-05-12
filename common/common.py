from os import environ


def get_env_bool(key: str, default: bool = False) -> bool:
    result = environ.get(key, default)
    return result.lower() == "true" if isinstance(result, str) else result
