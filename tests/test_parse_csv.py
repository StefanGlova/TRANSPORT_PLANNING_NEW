import unittest
from parse_csv import ParseCSV


class TestParseCSV(unittest.TestCase):
    """
    Test suite for ParseCSV class.
    """

    def test_parse_csv(self):
        """
        Test parcing csv file into list of dictionaries.

        This test case verifies that parse method of ParseCSV object read csv file and parse data into lisst of dictionaries.

        It checks:
        - The number of elements of the list
        """
        with open("orderbook.csv", "w") as file:
            file.write(
                "Customer Name,Customer Postcode,SKU,Qty,Vehicle Type,Due Date\n"
            )
            file.write("Alice,E1W 2RG,SKU123,57,trailer,trailer,2024-04-10\n")
            file.write("Bob,N9 9LA,SKU456,1000,rigid,2023-11-10\n")
            file.write("Error Vehicle Type,SKU2,5,wrong vehicle,2023-11-10\n")

        orderbook_file = ParseCSV("orderbook.csv")
        parsed_data = orderbook_file.parse()

        self.assertEqual(len(parsed_data), 3)


if __name__ == "__main__":
    unittest.main()
