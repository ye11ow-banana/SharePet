class CreateInstanceError(Exception):
    """Do not allow to create an instance of the class."""
    def __init__(self, class_name: str):
        super().__init__(f'Instance of the class `{class_name}` '
                         f'cannot be created.')


class EmptyMessageError(Exception):
    """Do not allow to send empty messages in `chats`."""


class NoKeyInResponseContextError(KeyError):
    """`KeyError` in `response_context` dict."""
