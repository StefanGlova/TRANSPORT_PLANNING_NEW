import unittest
from modules.data_processing_module.process_inventory import ProcessInventory
from modules.errors import WrongKeysError, WrongValueTypeError, WrongNumericRange


PARSER = ProcessInventory(None)
CORRECT_KEYS = ["SKU", "Qty"]


class TestInventoryParser(unittest.TestCase):

    def test_inventory_correct_input(self) -> None:
        """
        Test parsing list of dictionaries.

        This test case verifies that InventoryParser class correctly parse and organised input list of dictionaries and return dictionary, which correctly groupt sum value and group key, where key is SKU and value Qty.


        It checks:
        - Qty when SKU is in parsed_data once and qty is 0
        - Qty when SKU is in parsed_data once and qty is positive Int
        - Qty when SKU is in parased_data more then once and qty is positive Int
        - Whether each dictionary in input list only contains correct keys: 'SKU' and 'Qty' and if not raises custom WrongKeyError with correct message
        """
        print("test Inventory correct")

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
            # Correct keys but different order
            {"Qty": "10", "SKU": "ABC"},
        ]

        # Initialize InventoryParser object
        PARSER.parsed_data = parsed_data
        # Parse the inventory
        inventory = PARSER.parse_inventory()
        # Verify the parsed data
        self.assertEqual(len(inventory), 4)
        self.assertEqual(inventory["SKU1"], 20)
        self.assertEqual(inventory["SKU2"], 0)
        self.assertEqual(inventory["SKU3"], 8)
        self.assertEqual(inventory["ABC"], 10)

    def test_inventory_incorrect_input(self):
        """ """
        print("test Inventory incorrect")

        # Initialize different options of keys in parsed_data dictionary
        not_enough_keys_1 = [
            {"SKU": "SKU1"},
            {"SKU": "ABC"},
            {"SKU": "SKU2", "Qty": "15"},
        ]
        not_enough_keys_2 = [{"Qty": "15"}, {}, {"SKU": "SKU1", "Qty": "15"}]
        empty_dictionary = [{}]
        empty_list = []
        wrong_keys_1 = [
            {"SKU": "SKU1", "Qty": "15"},
            {"ABC": "SKU2", "Qty": "5"},
        ]
        wrong_keys_2 = [{"Qty": "10", "ABC": "SKU"}, {"SKU": "SKU2", "Qty": "15"}]
        too_many_keys = [
            {"SKU": "SKU2", "Qty": "15"},
            {"SKU": "SKU2", "Qty": "15", "ABC": "EFG"},
        ]

        all_wrong_keys = [
            not_enough_keys_1,
            not_enough_keys_2,
            empty_dictionary,
            empty_list,
            wrong_keys_1,
            wrong_keys_2,
            too_many_keys,
        ]

        # Iterate though list of lists with various wrong keys and asserting whether it raises correctly WrongKeyError
        for data in all_wrong_keys:
            keys_set = sorted(list(set(key for d in data for key in d.keys())))
            PARSER.parsed_data = data
            if keys_set != sorted(CORRECT_KEYS):
                with self.assertRaises(WrongKeysError) as context:
                    PARSER.parse_inventory()
                # Check for correct Error message
                self.assertEqual(
                    str(context.exception),
                    "Function parse_inventory only accepts these keys SKU, Qty!",
                )

    def test_inventory_wrong_value_type(self):
        print("test Inventory wrong value type")

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
                "Qty": "A",
            },
        ]

        PARSER.parsed_data = parsed_data

        with self.assertRaises(WrongValueTypeError) as context:
            PARSER.parse_inventory()
            self.assertEqual(
                str(context.exception),
                "Parameter Qty must be number",
            )

    def test_inventory_numbers_range(self):
        print("test Inventory numbers range")

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
                "Qty": "-5",
            },
            {
                "SKU": "SKU3",
                "Qty": "-10",
            },
        ]

        PARSER.parsed_data = parsed_data

        for line in parsed_data:
            if float(line["Qty"]) < 0:
                with self.assertRaises(WrongNumericRange) as context:
                    PARSER.parse_inventory()
                    self.assertEqual(
                        str(context.exception),
                        "Parameter Qty cannot be negative",
                    )


if __name__ == "__main__":
    unittest.main()
