class EmptyFileError(Exception):
    """
    Custom exception raised when the file is empty.
    """

    def __init__(self, filename):
        super().__init__(f"The file '{filename}' is empty.")
        self.filename = filename


class WrongKeysError(Exception):
    """
    Custom exception raised when dictionary does not have only correct keys.
    """

    def __init__(self, method_called: str, correct_keys: list):
        super().__init__(
            f"Function {method_called} only accepts these keys {', '.join(key for key in correct_keys)}!"
        )
        self.method_called = method_called
        self.correct_keys = correct_keys
