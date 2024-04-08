import unittest
import os
from parse_csv import ParseCSV, EmptyFileError

# Crate path to directory where tesing files will be stored
current_dir = os.path.dirname(os.path.realpath(__file__))
TEST_FILES_PATH = os.path.join(current_dir, "test_files")
# Checking if directory exist and if not creating it
os.makedirs(TEST_FILES_PATH, exist_ok=True)


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
        test_orderbook_file = os.path.join(TEST_FILES_PATH, "orderbook.csv")
        with open(test_orderbook_file, "w") as file:
            file.write(
                "Customer Name,Customer Postcode,SKU,Qty,Vehicle Type,Due Date\n"
            )
            file.write("Alice,E1W 2RG,SKU123,57,trailer,2024-04-10\n")
            file.write("Bob,N9 9LA,SKU456,1000,rigid,2023-11-10\n")
            file.write("Error Vehicle Type,PostCode,SKU2,5,wrong vehicle,2023-11-10\n")

        test_inventory_file = os.path.join(TEST_FILES_PATH, "inventory.csv")
        with open(test_inventory_file, "w") as other_file:
            other_file.write("SKU,Qty\n")
            other_file.write("abc,56\n")

        # Create ParseCSV objects from data in files
        orderbook_file = ParseCSV(test_orderbook_file)
        other_test_file = ParseCSV(test_inventory_file)
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
        empty_file = os.path.join(TEST_FILES_PATH, "empty.csv")
        with open(empty_file, "w") as empty:
            pass
        # Create ParseCSV object from empty file and test if it raise EmptyFileError exception when parse method is applied on it.
        parser = ParseCSV(empty_file)
        with self.assertRaises(EmptyFileError) as context:
            parser.parse()
        # Check that EmptyFileError exception raises correct custom error message
        self.assertEqual(context.exception.filename, empty_file)

    def test_different_delimiter_and_format(self):
        """
        Test parcing csv file into list of dictionaries with if file is not in  csv format, but txt; also to test for different delimiter, replacing previously used ',' with '-'.

        It checks:
        - Number of elements in the list, when file is in txt format and delimiter is '-'.
        """
        # Create txt file with '-' as delimiter
        different_delimiter_file = os.path.join(
            TEST_FILES_PATH, "different_delimiter.txt"
        )
        with open(different_delimiter_file, "w") as different_delimiter:
            different_delimiter.write(
                "Customer Name-Customer Postcode-SKU-Qty-Vehicle Type-Due Date\n"
            )
            different_delimiter.write("Alice-E1W 2RG-SKU123-57-trailer-2024-04-10\n")
            different_delimiter.write("Bob-N9 9LA-SKU456-1000-rigid-2023-11-10\n")
            different_delimiter.write(
                "Error Vehicle Type-PostCode-SKU2-5-wrong vehicle-2023-11-10\n"
            )

        # Create ParseCSV objects from data in files
        different_delimiter = ParseCSV(different_delimiter_file)
        # Apply parse method to both objects
        parsed_data_different_delimiter_file = different_delimiter.parse()
        # Check for correct outcome
        self.assertEqual(len(parsed_data_different_delimiter_file), 3)

    def test_encoding_issue(self):
        encoding_test_file = os.path.join(TEST_FILES_PATH, "encoding.csv")
        with open(encoding_test_file, "w", encoding="utf-8") as encoding_file:
            encoding_file.write(
                "Customer Name,Customer Postcode,SKU,Qty,Vehicle Type,Due Date\n"
            )
            encoding_file.write("Alice,E1W 2RG,Mäkčeň,57,trailer,2024-04-10\n")
            encoding_file.write("复,N9 9LA,SKU456,1000,rigid,2023-11-10\n")
            encoding_file.write(
                "Non-ASCII Nameü,Non-ASCII Postcode,SKU789,10,trailer,2023-12-31\n"
            )
        # Create ParseCSV objects from data in files
        encoding = ParseCSV(encoding_test_file)
        # Apply parse method to both objects
        parsed_data_encoding_test_file = encoding.parse()
        # Check for correct outcome
        self.assertEqual(len(parsed_data_encoding_test_file), 3)
        self.assertEqual(
            parsed_data_encoding_test_file[2]["Customer Name"], "Non-ASCII Nameü"
        )
        self.assertEqual(parsed_data_encoding_test_file[1]["Customer Name"], "复")
        self.assertEqual(parsed_data_encoding_test_file[0]["SKU"], "Mäkčeň")


if __name__ == "__main__":
    unittest.main()
