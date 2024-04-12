from modules.errors import WrongKeysError, WrongValueTypeError, WrongNumericRange


class ProcessInventory:
    def __init__(self, parsed_data):
        self.parsed_data = parsed_data

    def parse_inventory(self) -> dict:
        """
        Parse data from parsed_data list into dictionary and group them by SKU.

        Returns:
            dictionary: An inventory dictionary of SKU and it qty, grouped by SKU.
        """
        # Initialize dict datastructure which stores inventry key value pairs and also variable correct_keys
        inventory, correct_keys = dict(), ["SKU", "Qty"]
        fields = {"SKU": "string", "Qty": "number"}
        range = {"Qty": "cannot be negative"}

        # Check if parsed_data is not empty list
        if self.parsed_data == []:
            raise WrongKeysError(
                method_called="parse_inventory", correct_keys=correct_keys
            )

        # Iterate over each item of the parsed_data list
        for row in self.parsed_data:
            # Check if row only contains correct keys
            if sorted(list(set(key for key in row.keys()))) != sorted(correct_keys):
                raise WrongKeysError(
                    method_called="parse_inventory", correct_keys=correct_keys
                )
            # Check if Qty field has numeric value
            try:
                qty = int(row["Qty"])
                if qty < 0:
                    raise WrongNumericRange("Qty", range)
            except ValueError:
                raise WrongValueTypeError("Qty", fields)
            # If SKU already exist in inventory dict, then it increment its value by Qty, if does not exist, it adds it with its initial Qty
            inventory[row["SKU"]] = inventory.get(row["SKU"], 0) + qty

        return inventory
