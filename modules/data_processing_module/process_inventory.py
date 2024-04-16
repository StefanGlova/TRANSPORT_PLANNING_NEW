from modules.errors import WrongKeysError, WrongValueTypeError, WrongNumericRange


class ProcessInventory:
    # Initialize global variable for ProcessInventory class
    CORRECT_KEYS = ["SKU", "Qty"]
    FIELDS = {"SKU": "string", "Qty": "number"}
    RANGE = {"Qty": "cannot be negative"}

    def __init__(self, parsed_data: list) -> None:
        """
        Initialize ProcessInventory object.
        """
        self.parsed_data = parsed_data

    def parse_inventory(self) -> dict:
        """
        Parse data from parsed_data list into dictionary and group them by SKU.

        Input:
            parsed_data: list
            Input list must not be empty - check before further process with parse_orderbook method and raises error if it is empty.
            The list must have these fields - validation of numeric fields is checked by private methods.
            Expected fields:
                "SKU": "string",
                "Qty": "number", "cannot be negative"

        Returns:
            dictionary: An inventory dictionary of SKU and it qty, grouped by SKU.
        """
        # Check if input is not empty list. Raise appropriate error if it is
        self._check_empty_list()

        # Initialize empty inventory
        inventory = dict()

        # Iterate over each item of the parsed_data list
        for row in self.parsed_data:
            # Check if row only contains correct keys
            self._check_correct_keys(row)

            # Check if Qty field has numeric non negative value
            qty = self._validate_number_value(row["Qty"], "Qty")

            # Update qty for each SKU
            inventory[row["SKU"]] = inventory.get(row["SKU"], 0) + qty

        return inventory

    def _check_empty_list(self) -> None:
        """
        Private method checking if input list is not empty. If it is, it raises error. For error details, please refer to errors.py file.
        """
        if self.parsed_data == []:
            raise WrongKeysError(
                method_called="parse_inventory", correct_keys=self.CORRECT_KEYS
            )

    def _check_correct_keys(self, row: dict) -> None:
        """
        Private method checking if every row(dictionary) in the input list has correct keys. If not, it raises error. For error details, please refer to errors.py file.
        """
        if sorted(list(set(key for key in row.keys()))) != sorted(self.CORRECT_KEYS):
            raise WrongKeysError(
                method_called="parse_inventory", correct_keys=self.CORRECT_KEYS
            )

    def _validate_number_value(self, value: str, field: str) -> float:
        """
        Private method checking if input value can be converted to floating point number and whether the number is not negative. If any of these fails, it raises appropriate error. For error details, please refer to errors.py file.
        """
        try:
            value = float(value)
            if value < 0:
                raise WrongNumericRange(field, self.RANGE)
            else:
                return value
        except ValueError:
            raise WrongValueTypeError(field, self.FIELDS)
