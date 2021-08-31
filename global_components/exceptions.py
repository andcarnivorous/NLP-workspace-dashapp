class InvalidRegEx(Exception):
    def __init__(self, msg='The regex provided is invalid', *args, **kwargs):
        super().__init__(msg, *args, **kwargs)
