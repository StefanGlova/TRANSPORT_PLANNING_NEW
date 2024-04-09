class EmptyFileError(Exception):
    """
    Custom exception raised when the file is empty.
    """

    def __init__(self, filename):
        super().__init__(f"The file '{filename}' is empty.")
        self.filename = filename
