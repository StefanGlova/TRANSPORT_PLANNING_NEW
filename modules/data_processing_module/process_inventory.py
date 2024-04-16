from modules.data_processing_module.general_file_parser import GeneralFileParser


class ProcessInventory(GeneralFileParser):
    # Initialize global variable for ProcessInventory class
    CORRECT_KEYS = ["SKU", "Qty"]
    FIELDS = {"SKU": "string", "Qty": "number"}
    RANGE = {"Qty": "cannot be negative"}

    def __init__(self, file_path: str, delimiter: str = ",") -> None:
        """
        Initialize ProcessInventory object.
        """
        super().__init__(file_path=file_path, delimiter=delimiter)

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
        self._check_empty_list(method_called="parse_inventory")

        # Initialize empty inventory
        inventory = dict()

        # Iterate over each item of the parsed_data list
        for row in self.parsed_data:
            # Check if row only contains correct keys
            self._check_correct_keys(row=row, method_called="parse_inventory")

            # Check if Qty field has numeric non negative value
            qty = self._validate_number_value(row["Qty"], "Qty")

            # Update qty for each SKU
            inventory[row["SKU"]] = inventory.get(row["SKU"], 0) + qty

        return inventory
