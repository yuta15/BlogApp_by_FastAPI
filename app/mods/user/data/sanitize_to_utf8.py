


def sanitize_to_utf8(**kwargs) -> dict:
    """
    受け取った値をUTF8へとサニタイズする。
    """
    sanitized_args = {}
    for key, val in kwargs.items():
        sanitized_args[key] = val.encode('utf-8')
    
    return sanitized_args