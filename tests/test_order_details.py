import unittest
from order_parser import OrderParser
from parse_csv import ParseCSV


class TestOrderDetails(unittest.TestCase):
    def test_parse_orderbook(self):
        # sample orderbook.csv file for testing
        with open("orderbook.csv", "w") as file:
            file.write(
                "Customer Name,Customer Postcode,SKU,Qty,Vehicle Type,Due Date\n"
            )
            file.write("Alice,E1W 2RG,SKU123,57,trailer,trailer,2024-04-10\n")
            file.write("Bob,N9 9LA,SKU456,1000,rigid,2023-11-10\n")
            file.write("Error Vehicle Type,SKU2,5,wrong vehicle,2023-11-10\n")

        # parse csv file
        orderbook_file = ParseCSV("orderbook.csv")
        parsed_data = orderbook_file.parse()

        # initialize OrderParser
        parser = OrderParser(parsed_data)

        # parse the orderbook
        orders_by_vehicle = parser.parse_orderbook()

        # veryfy the parsed data
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
