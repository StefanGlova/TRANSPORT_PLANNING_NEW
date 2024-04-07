import unittest


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
                "SKU1": "15",
            },
            {
                "SKU2": "0",
            },
            {
                "SKU1": "5",
            },
            {
                "SKU3": "8",
            },
        ]

        # Initialize InventoryParser object
        parser = InventoryParser(parsed_data)

        # Parse the inventory
        inventory = parser.parse_invenvtory()

        # Verify the parsed data
        self.assertEqual(len(inventory), 3)
        self.assertEqual(inventory["SKU1"], 20)
        self.assertEqual(inventory["SKU2"], 0)
        self.assertEqual(inventory["SKU3"], 8)


if __name__ == "__main__":
    unittest.main()
