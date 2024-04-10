# TODO to be deleted


class InventoryParser:
    def __init__(self, parsed_data: list):
        """
        Constructor method for InventoryParser class.

        Paramethers:
            parsed_data (list): A list of dictionaries, where each dictionary represents row in parsed inventory file
        """
        self.parsed_data = parsed_data

    def parse_inventory(self) -> dict:
        """
        Parse data from parsed_data list into dictionary and group them by SKU.

        Returns:
            dictionary: An inventory dictionary of SKU and it qty, grouped by SKU.
        """
        # Initialize dict datastructure which stores inventry key value pairs
        inventory = dict()
        # Iterate over each item of the parsed_data list
        for row in self.parsed_data:
            # If SKU already exist in inventory dict, then it increment its value by Qty, if does not exist, it adds it with its initial Qty
            inventory[row["SKU"]] = inventory.get(row["SKU"], 0) + int(row["Qty"])

        return inventory
