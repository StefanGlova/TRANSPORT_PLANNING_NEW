import unittest
from order_parser import OrderParser
from parse_csv import ParseCSV


class TestOrderDetails(unittest.TestCase):
    """
    Test suite for OrderParser and ParserCSV classes.
    """

    def test_parse_orderbook(self) -> None:
        """
        Test parsing of orderbook CSV file.

        This test case verifies that ParseCSV class correctly parse file input and OrderParser then organised parsed date into dictionary of lists, separate fro traielr, rigid and ERROR.

        It checks:
        - The number of orders in the trailer list
        - The number of orders in rigid list
        - The number of orers in ERROR list
        - The correctness of specific order details for trailer and rigid
        - The existence and correctness of orders with invalid vehicle info
        """
        # Sample orderbook.csv file for testing
        with open("orderbook.csv", "w") as file:
            file.write(
                "Customer Name,Customer Postcode,SKU,Qty,Vehicle Type,Due Date\n"
            )
            file.write("Alice,E1W 2RG,SKU123,57,trailer,trailer,2024-04-10\n")
            file.write("Bob,N9 9LA,SKU456,1000,rigid,2023-11-10\n")
            file.write("Error Vehicle Type,SKU2,5,wrong vehicle,2023-11-10\n")

        # Parse csv file
        orderbook_file = ParseCSV("orderbook.csv")
        parsed_data = orderbook_file.parse()

        # Initialize OrderParser
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
