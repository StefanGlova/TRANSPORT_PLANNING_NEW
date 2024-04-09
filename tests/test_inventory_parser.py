# TODO - to be deleted

import unittest
from inventory_parser import InventoryParser


class TestInventoryParser(unittest.TestCase):
    """
    Test suite for InventoryParser class.
    """

    def test_inventory_parser(self) -> None:
        """
        Test parsing list of dictionaries.

        This test case verifies that InventoryParser class correctly parse and organised input list of dictionaries and return dictionary, which correctly groupt sum value and group key, where key is SKU and value Qty.


        It checks:
        - Qty when SKU is in parsed_data once and qty is 0
        - Qty when SKU is in parsed_data once and qty is positive Int
        - Qty when SKU is in parased_data more then once and qty is positive Int
        """
        # Create parsed_data list of dicts for testing purpose
        parsed_data = [
            {
                "SKU": "SKU1",
                "Qty": "15",
            },
            {
                "SKU": "SKU2",
                "Qty": "0",
            },
            {
                "SKU": "SKU1",
                "Qty": "5",
            },
            {
                "SKU": "SKU3",
                "Qty": "8",
            },
        ]

        # Initialize InventoryParser object
        parser = InventoryParser(parsed_data)
        # Parse the inventory
        inventory = parser.parse_inventory()
        # Verify the parsed data
        self.assertEqual(len(inventory), 3)
        self.assertEqual(inventory["SKU1"], 20)
        self.assertEqual(inventory["SKU2"], 0)
        self.assertEqual(inventory["SKU3"], 8)


if __name__ == "__main__":
    unittest.main()
