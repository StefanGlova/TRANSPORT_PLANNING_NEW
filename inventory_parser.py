class InventoryParser:
    def __init__(self, parsed_data: list):
        self.parsed_data = parsed_data

    def parse_inventory(self) -> dict:
        inventory = dict()

        for row in self.parsed_data:
            inventory[row["SKU"]] = inventory.get(row["SKU"], 0) + int(row["Qty"])

        return inventory
