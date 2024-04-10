# TODO to be deleted

import unittest
from order_parser import OrderParser


class TestOrderParser(unittest.TestCase):
    """
    Test suite for OrderParser class.
    """

    def test_order_parser(self) -> None:
        """
        Test parsing list of dictionaries.

        This test case verifies that OrderParser class correctly parse and organised input list of dictionaries and return dictionary, which separate orders by vehicle type as trailer, rigid and ERROR.

        It checks:
        - The number of orders in the trailer list
        - The number of orders in rigid list
        - The number of orers in ERROR list
        - The correctness of specific order details for trailer and rigid
        - The existence and correctness of orders with invalid vehicle info
        """

        # Create parsed_data list of dicts for testing purpose
        parsed_data = [
            {
                "Customer Name": "Alice",
                "Customer Postcode": "E1W 2RG",
                "SKU": "SKU123",
                "Qty": "57",
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
            {
                "Customer Name": "Error Vehicle Type",
                "Customer Postcode": "E1W 2RG",
                "SKU": "SKU2",
                "Qty": "5",
                "Vehicle Type": "wrong vehicle",
                "Due Date": "2023-11-10",
            },
        ]

        # Initialize OrderParser object
        parser = OrderParser(parsed_data)
        # Parse the orderbook
        orders_by_vehicle = parser.parse_orderbook()
        # Verify the parsed data
        self.assertEqual(len(orders_by_vehicle["trailer"]), 1)
        self.assertEqual(len(orders_by_vehicle["rigid"]), 1)
        self.assertEqual(orders_by_vehicle["trailer"][0]["Customer Name"], "Alice")
        self.assertEqual(orders_by_vehicle["rigid"][0]["Customer Postcode"], "N9 9LA")
        self.assertEqual(len(orders_by_vehicle["ERROR"]), 1)
        self.assertEqual(
            orders_by_vehicle["ERROR"][0]["Customer Name"], "Error Vehicle Type"
        )


if __name__ == "__main__":
    unittest.main()
