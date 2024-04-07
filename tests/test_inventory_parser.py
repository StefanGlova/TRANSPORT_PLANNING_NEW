import unittest
from inventory_parser import InventoryParser


class TestInventoryParser(unittest.TestCase):
    """
    Test suite for InventoryParser class.
    """

    def test_inventory_parser(self) -> None:
        """
        Test parsing list of dictionaries.



        It checks:
        -
        """

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
