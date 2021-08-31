from global_components.exceptions import InvalidRegEx

def sanitize_regex(expression: str):
    if expression in ["[A-Z]", "[A-Z]*", "[A-Z]+", "[a-z]", "[a-z]*", "[a-z]+", ".+", ".*", ".", "\w+", "\b+", "\w*", "\b*"]:
        raise InvalidRegEx
    elif any(exp in expression for exp in [".+", ".*", ".", "\w+", "\b+", "\w*", "\b*"]):
        raise InvalidRegEx
    else:
        return expression