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
            file.write("Alice,E1W 2RG,SKU123,57,trailer,2024-04-10\n")
            file.write("Bob,N9 9LA,SKU456,1000,rigid,2023-11-10\n")
            file.write("Error Vehicle Type,PostCode,SKU2,5,wrong vehicle,2023-11-10\n")

        with open("other_test_file.csv", "w") as other_file:
            other_file.write("SKU,Qty\n")
            other_file.write("abc,56\n")

        orderbook_file = ParseCSV("orderbook.csv")
        other_test_file = ParseCSV("other_test_file.csv")
        parsed_data_orderbook = orderbook_file.parse()
        parsed_data_other_test = other_test_file.parse()

        self.assertEqual(len(parsed_data_orderbook), 3)
        self.assertEqual(len(parsed_data_other_test), 1)

    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            parser = ParseCSV("nonexisting_file.csv")
            parser.parse()

    def test_empty_file(self):
        with open("empty.csv", "w") as empty_file:
            pass
        parser = ParseCSV("empty.csv")
        with self.assertRaises(EmptyFileError) as context:
            parser.parse()

        self.assertEqual(context.exception.filename, "empty.csv")


if __name__ == "__main__":
    unittest.main()
