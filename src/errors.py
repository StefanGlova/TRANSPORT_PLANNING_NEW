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


class WrongValueTypeError(Exception):
    """
    Custom exception raised when value has wrong data type.
    """

    def __init__(self, parameter: str, field: dict):
        super().__init__(f"Parameter {parameter} must be {field[parameter]}")
        self.parameter = parameter
        self.field = field


class WrongNumericRange(Exception):
    """
    Custom exception raised when numeric value is not in expected range.
    """

    def __init__(self, parameter: str, range: dict):
        super().__init__(f"Parameter {parameter} {range[parameter]}")
        self.parameter = parameter
        self.range = range


class EmptyDatasetError(Exception):
    """
    Custom exception raised when input dataset is empty
    """

    def __init__(self):
        super().__init__("Orderbook and inventory must not be empty")


class WrongKeysAllocatorError(Exception):
    """
    Custom exception raised when orderbook or inventory dictionaries does not have a correct key, and allocate_inventory method of InventoryAllocation class is called.
    """

    def __init__(self):
        error_message = "Function allocate_inventory takes two dictionaries: orderbook and inventory.\nOrderbook must be outcome from parse_orderbook method called on OrderbookParser object.\nInventory must be outcome from parse_inventory method called on InventoryParser object.\nIf they are not, they may not have correct keys.\n"
        super().__init__(error_message)
