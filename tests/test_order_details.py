import unittest
from order_parser import OrderParser


class TestOrderDetails(unittest.TestCase):
    def test_parse_orderbook(self):
        # sample orderbook.csv file for testing
        with open("orderbook.csv", "w") as file:
            file.write(
                "Customer Name, Customer Postcode, SKU, Qty, Vehicle Type, Due Date\n"
            )
            file.write("Alice,E1W 2RG,UG460,57,trailer,trailer,2024-04-10\n")
            file.write("Bob,N9 9LA,PB115,1000,rigid,2023-11-10\n")

        # initialize OrderParser
        parser = OrderParser("orderbook.csv")

        # parse the orderbook
        orders_by_vehicle = parser.parse_orderbook()

        # veryfy the parsed data
        self.assertEqual(len(orders_by_vehicle["trailer"]), 1)
        self.assertEqual(len(orders_by_vehicle["rigid"]), 1)
        self.assertEqual(orders_by_vehicle["trailer"][0]["Customer Name"], "Alice")
        self.assertEqual(orders_by_vehicle["rigid"][0]["Customer Postcode"], "N9 9LA")


if __name__ == "__main__":
    unittest.main()
