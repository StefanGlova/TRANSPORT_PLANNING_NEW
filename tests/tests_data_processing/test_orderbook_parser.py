import unittest
from modules.data_processing_module.process_orderbook import ProcessOrderbook
from modules.errors import WrongKeysError, WrongValueTypeError, WrongNumericRange
from datetime import datetime
import re

PARSER = ProcessOrderbook(None)
CORRECT_KEYS = [
    "Customer Name",
    "Customer Postcode",
    "SKU",
    "Qty",
    "Vehicle Type",
    "Due Date",
    "Transport Volume (m3)",
]


class TestOrderbookParser(unittest.TestCase):

    def test_orderbook_correct_input(self) -> None:
        """
        Test parsing list of dictionaries.

        This test case verifies that OrderParser class correctly parse and organised input list of dictionaries and return dictionary, which separate orders by vehicle type as trailer, rigid and ERROR.

        It checks:
        - The number of orders in the trailer list
        - The number of orders in rigid list
        - The number of orers in ERROR list
        - The correctness of specific order details for trailer and rigid
        - The existence and correctness of orders with invalid vehicle info
        - Whether each dictionary in input list only contains correct keys and if not it checks for raising custome WrongKeyError with correct message
        """

        print("test Orderbook correct")

        # Create parsed_data list of dicts for testing purpose
        parsed_data = [
            {
                "Customer Name": "Alice",
                "Customer Postcode": "E1W 2RG",
                "SKU": "SKU123",
                "Qty": "57",
                "Vehicle Type": "trailer",
                "Due Date": "2024-04-10",
                "Transport Volume (m3)": "10",
            },
            {
                "Customer Name": "Bob",
                "Customer Postcode": "N9 9LA",
                "SKU": "SKU456",
                "Qty": "1000",
                "Vehicle Type": "rigid",
                "Due Date": "2023-11-10",
                "Transport Volume (m3)": "27",
            },
            # Correct keys but different order
            {
                "Customer Postcode": "E1W 2RG",
                "Customer Name": "Error Vehicle Type",
                "Due Date": "2023-11-10",
                "SKU": "SKU2",
                "Qty": "5",
                "Transport Volume (m3)": "18",
                "Vehicle Type": "wrong vehicle",
            },
            {
                "Transport Volume (m3)": "0.005",
                "Customer Name": "Abcd",
                "Customer Postcode": "N9 9LA",
                "SKU": "SKU456",
                "Qty": "10.53",
                "Vehicle Type": "rigid",
                "Due Date": "2023-11-10",
            },
        ]

        # Initialize OrderParser object
        PARSER.parsed_data = parsed_data
        # Parse the orderbook
        orders_by_vehicle = PARSER.parse_orderbook()
        # Verify the parsed data
        self.assertEqual(len(orders_by_vehicle["trailer"]), 1)
        self.assertEqual(len(orders_by_vehicle["rigid"]), 2)
        self.assertEqual(orders_by_vehicle["trailer"][0]["Customer Name"], "Alice")
        self.assertEqual(orders_by_vehicle["rigid"][0]["Customer Postcode"], "N9 9LA")
        self.assertEqual(len(orders_by_vehicle["ERROR"]), 1)
        self.assertEqual(
            orders_by_vehicle["ERROR"][0]["Customer Name"], "Error Vehicle Type"
        )

        # Verify that numeric value of qty and transport volume is correctly converted to number
        self.assertEqual(orders_by_vehicle["trailer"][0]["Qty"], 57)
        self.assertEqual(orders_by_vehicle["trailer"][0]["Transport Volume (m3)"], 10)

        # Verify that numeric valu eof qty and transport volume is correctly converted to number even with decimal place number
        self.assertEqual(orders_by_vehicle["rigid"][1]["Qty"], 10.53)
        self.assertEqual(orders_by_vehicle["rigid"][-1]["Transport Volume (m3)"], 0.005)

        # Verify that date value is correctly converted to datetime type
        # First Test
        date_string = parsed_data[0]["Due Date"]
        match = re.search(r"\d{4}-\d{2}-\d{2}", date_string)
        date = datetime.strptime(match.group(), "%Y-%m-%d").date()
        self.assertEqual(orders_by_vehicle["trailer"][0]["Due Date"], date)
        # Second Test
        date_string = parsed_data[1]["Due Date"]
        match = re.search(r"\d{4}-\d{2}-\d{2}", date_string)
        date = datetime.strptime(match.group(), "%Y-%m-%d").date()
        self.assertEqual(orders_by_vehicle["rigid"][0]["Due Date"], date)

    def test_orderbook_incorrect_inputs(self):

        print("test Orderbook incorrect")

        # Initialize different options of keys in parsed_data dictionary

        not_enough_keys_1 = [
            {
                "Customer Name": "Alice",
                "Customer Postcode": "E1W 2RG",
                "SKU": "SKU123",
                "Vehicle Type": "trailer",
                "Due Date": "2024-04-10",
            },
            {
                "Customer Name": "Bob",
                "Customer Postcode": "N9 9LA",
                "SKU": "SKU456",
                "Qty": "1000",
                "Vehicle Type": "rigid",
                "Due Date": "2023-11-10",
            },
        ]

        not_enough_keys_2 = [
            {
                "Customer Name": "Alice",
                "Customer Postcode": "E1W 2RG",
                "SKU": "SKU123",
                "Vehicle Type": "trailer",
                "Due Date": "2024-04-10",
            },
            {},
        ]

        empty_dictionary = [{}]
        empty_list = []

        wrong_keys_1 = [
            {
                "CustomerName": "Alice",
                "Customer Postcode": "E1W 2RG",
                "SKU": "SKU123",
                "Qty": "57",
                "Vehicle Type": "trailer",
                "Due Date": "2024-04-10",
                "Transport Volume": "50",
            },
            {
                "Customer Name": "Bob",
                "Customer Postcode": "N9 9LA",
                "SKU": "SKU456",
                "Qty": "1000",
                "Vehicle Type": "rigid",
                "Due Date": "2023-11-10",
            },
        ]

        wrong_keys_2 = [
            {
                "Customer Name": "Alice",
                "Customer Postcode": "E1W 2RG",
                "sku": "SKU123",
                "Qty": "57",
                "Vehicle Type": "trailer",
                "Due Date": "2024-04-10",
                "Transport Volume": "not right",
            },
            {
                "Customer Name": "Bob",
                "Customer Postcode": "N9 9LA",
                "SKU": "SKU456",
                "Qty": "1000",
                "Vehicle Type": "rigid",
                "Due Date": "2023-11-10",
                "Transport Volume (m3)": "15",
            },
        ]

        too_many_keys = [
            {
                "Customer Name": "Alice",
                "Customer Postcode": "E1W 2RG",
                "SKU": "SKU123",
                "Qty": "57",
                "Vehicle Type": "trailer",
                "Due Date": "2024-04-10",
                "Transport Volume (m3)": "50",
                "Extra columns": "wrong",
            },
            {
                "Customer Name": "Bob",
                "Customer Postcode": "N9 9LA",
                "SKU": "SKU456",
                "Qty": "1000",
                "Vehicle Type": "rigid",
                "Due Date": "2023-11-10",
                "Transport Volume (m3)": "50",
            },
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
                    PARSER.parse_orderbook()
                # Check for correct Error message
                self.assertEqual(
                    str(context.exception),
                    "Function parse_orderbook only accepts these keys Customer Name, Customer Postcode, SKU, Qty, Vehicle Type, Due Date!",
                )

    def test_orderbook_wrong_value_type(self):
        print("test Orderbook wrong value type")

        parsed_data = [
            {
                "Customer Name": "Alice",
                "Customer Postcode": "E1W 2RG",
                "SKU": "SKU123",
                "Qty": "ABC",
                "Vehicle Type": "trailer",
                "Due Date": "2024-04-10",
                "Transport Volume (m3)": "50",
            },
            {
                "Customer Name": "Bob",
                "Customer Postcode": "N9 9LA",
                "SKU": "SKU456",
                "Qty": "1000",
                "Vehicle Type": "rigid",
                "Due Date": "ABCD",
                "Transport Volume (m3)": "50",
            },
            {
                "Customer Name": "Bob",
                "Customer Postcode": "N9 9LA",
                "SKU": "SKU456",
                "Qty": "1000",
                "Vehicle Type": "rigid",
                "Due Date": "2024-04-10",
                "Transport Volume (m3)": "A",
            },
        ]

        PARSER.parsed_data = [parsed_data[0]]

        with self.assertRaises(WrongValueTypeError) as context:
            PARSER.parse_orderbook()
            self.assertEqual(
                str(context.exception),
                "Parameter Qty must be number",
            )

        PARSER.parsed_data = [parsed_data[1]]

        with self.assertRaises(WrongValueTypeError) as context:
            PARSER.parse_orderbook()
            self.assertEqual(
                str(context.exception),
                "Parameter Due Date must be date",
            )

        PARSER.parsed_data = [parsed_data[2]]

        with self.assertRaises(WrongValueTypeError) as context:
            PARSER.parse_orderbook()
            self.assertEqual(
                str(context.exception),
                "Parameter Transport Volume (m3) must be number",
            )

    def test_orderbook_numbers_range(self):
        print("test Orderbook numbers range")

        parsed_data = [
            {
                "Customer Name": "Alice",
                "Customer Postcode": "E1W 2RG",
                "SKU": "SKU123",
                "Qty": "-57",
                "Vehicle Type": "trailer",
                "Due Date": "2024-04-10",
            },
            {
                "Customer Name": "Bob",
                "Customer Postcode": "N9 9LA",
                "SKU": "SKU456",
                "Qty": "-10.53",
                "Vehicle Type": "rigid",
                "Due Date": "2023-11-10",
            },
        ]

        PARSER.parsed_data = parsed_data

        for line in parsed_data:
            if float(line["Qty"]) < 0:
                with self.assertRaises(WrongNumericRange) as context:
                    PARSER.parse_orderbook()
                    self.assertEqual(
                        str(context.exception), "Parameter Qty cannot be negative"
                    )


if __name__ == "__main__":
    unittest.main()
