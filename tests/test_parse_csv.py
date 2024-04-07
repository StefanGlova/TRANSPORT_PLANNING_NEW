import unittest
from parse_csv import ParseCSV, EmptyFileError


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
        # Create two csv files for testing purpose only
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

        # Create ParseCSV objects from data in files
        orderbook_file = ParseCSV("orderbook.csv")
        other_test_file = ParseCSV("other_test_file.csv")
        # Apply parse method to both objects
        parsed_data_orderbook = orderbook_file.parse()
        parsed_data_other_test = other_test_file.parse()
        # Check the outcome from test
        self.assertEqual(len(parsed_data_orderbook), 3)
        self.assertEqual(len(parsed_data_other_test), 1)

    def test_missing_file(self):
        """
        Test parcing csv file into list of dictionaries when file does not exist.

        It checks:
        - Test raises FileNotFoundError exception when file does not exist
        """
        # Try to crate ParseCSV object and apply parse method on it with none existing csv file and check for the outcome
        with self.assertRaises(FileNotFoundError):
            parser = ParseCSV("nonexisting_file.csv")
            parser.parse()

    def test_empty_file(self):
        """
        Test parcing csv file into list of dictionaries with empty csv file.

        It checks:
        - Test raises custom EmptyFileError exception when csv file is empty.
        """
        # Create empty csv file
        with open("empty.csv", "w") as empty_file:
            pass
        # Create ParseCSV object from empty file and test if it raise EmptyFileError exception when parse method is applied on it.
        parser = ParseCSV("empty.csv")
        with self.assertRaises(EmptyFileError) as context:
            parser.parse()
        # Check that EmptyFileError exception raises correct custom error message
        self.assertEqual(context.exception.filename, "empty.csv")


if __name__ == "__main__":
    unittest.main()
