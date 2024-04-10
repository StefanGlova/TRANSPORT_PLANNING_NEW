import unittest
import threading
import os
from parse_csv import ParseCSV
from errors import EmptyFileError


# Crate path to directory where tesing files will be stored
current_dir = os.path.dirname(os.path.realpath(__file__))
TEST_FILES_PATH = os.path.join(current_dir, "test_files")
NUM_THREADS = 5

# Checking if directory exist and if not creating it
os.makedirs(TEST_FILES_PATH, exist_ok=True)

# Test data sample used by TextParseCSV object in various method when checking for correct outcome
TEST_DATA_SAMPLE = {
    "Customer Name": "Bob",
    "Customer Postcode": "N9 9LA",
    "SKU": "SKU456",
    "Qty": "1000",
    "Vehicle Type": "rigid",
    "Due Date": "2023-11-10",
}


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
        self.assertEqual(parsed_data_orderbook[1], TEST_DATA_SAMPLE)

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

        # Create ParseCSV objects from data in file
        different_delimiter = ParseCSV(different_delimiter_file, delimiter="-")
        # Apply parse method to both objects
        parsed_data_different_delimiter_file = different_delimiter.parse()

        # Check for correct outcome
        self.assertEqual(len(parsed_data_different_delimiter_file), 3)
        self.assertEqual(parsed_data_different_delimiter_file[1], TEST_DATA_SAMPLE)

    def test_encoding_issue(self):
        """
        Test parcing csv file into list of dictionaries using utf-8 encoding to ensure it handle non ascii characters correctly.

        It checks:
        - Number of elements in the list
        - Check for non ascii string Nameü
        - Check for non ascii string Mäkčeň
        - Check for non ascii string 复
        """
        # Create encoding.csv file where not all characters are ASCII
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
        # Create ParseCSV objects from data in file
        encoding = ParseCSV(encoding_test_file)
        # Apply parse method to the object
        parsed_data_encoding_test_file = encoding.parse()

        # Check for correct outcome
        self.assertEqual(len(parsed_data_encoding_test_file), 3)
        self.assertEqual(
            parsed_data_encoding_test_file[2]["Customer Name"], "Non-ASCII Nameü"
        )
        self.assertEqual(parsed_data_encoding_test_file[1]["Customer Name"], "复")
        self.assertEqual(parsed_data_encoding_test_file[0]["SKU"], "Mäkčeň")

    # def test_large_file_handling(self):
    #     """
    #     Test parcing csv file into list of dictionaries -testing with large file with more then 10_000_000 lines.

    #     It checks:
    #     - Number of elements in the list
    #     - Check that dictionary of last line is as expected
    #     """
    #     # Create file with more then 10_000_000 lines
    #     large_file = os.path.join(TEST_FILES_PATH, "large.csv")
    #     all_rows = "Alice,E1W 2RG,SKU123,57,trailer,2024-04-10\n"
    #     middle_row = "Error Vehicle Type,PostCode,SKU2,5,wrong vehicle,2023-11-10\n"
    #     last_row = "Bob,N9 9LA,SKU456,1000,rigid,2023-11-10\n"
    #     rows_number = 5_000_000

    #     with open(large_file, "w") as large:
    #         large.write(
    #             "Customer Name,Customer Postcode,SKU,Qty,Vehicle Type,Due Date\n"
    #         )
    #         for _ in range(rows_number):
    #             large.write(all_rows)

    #         large.write(middle_row)

    #         for _ in range(rows_number):
    #             large.write(all_rows)

    #         large.write(last_row)

    #     # Create ParseCSV objects from data in file
    #     large_file_object = ParseCSV(large_file)
    #     # Apply parse method to the object
    #     parsed_data_large_file = large_file_object.parse()

    #     # Check for correct outcome
    #     self.assertEqual(len(parsed_data_large_file), 10_000_002)
    #     self.assertEqual(parsed_data_large_file[10_000_001], TEST_DATA_SAMPLE)

    def test_concurrency(self):
        """
        Test parcing csv file into list of dictionaries -testing for concurrency usage of the csv file to ensure it parse data correctly, even if used simultaneously by more threads.

        It checks:
        - Number of elements in the list
        - Check that dictionary on possition 1 is as expected for each thread.
        """
        # Create test file
        test_concurrency_file = os.path.join(TEST_FILES_PATH, "concurrency.csv")
        with open(test_concurrency_file, "w") as concurrency_file:
            concurrency_file.write(
                "Customer Name,Customer Postcode,SKU,Qty,Vehicle Type,Due Date\n"
            )
            concurrency_file.write("Alice,E1W 2RG,SKU123,57,trailer,2024-04-10\n")
            concurrency_file.write("Bob,N9 9LA,SKU456,1000,rigid,2023-11-10\n")

        # Create ParseCSV objects from data in file
        parser = ParseCSV(test_concurrency_file)
        # Initialize 2 empty lists
        parsed_data_all_threads, threads = list(), list()

        # Define function which apply parse method and append parsed_data to the list
        def worker():
            parsed_data = parser.parse()
            parsed_data_all_threads.append(parsed_data)

        # Create threads and append each to the list
        for _ in range(NUM_THREADS):
            thread = threading.Thread(target=worker)
            threads.append(thread)

        # Run all threads
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        # Check of all threads has been processed
        self.assertEqual(len(parsed_data_all_threads), NUM_THREADS)
        # Check that each thread has correct outcome
        for parsed_data_thread in parsed_data_all_threads:
            self.assertEqual(parsed_data_thread[1], TEST_DATA_SAMPLE)

    def test_permission_error(self):
        """
        Test parcing csv file into list of dictionaries -testing for Permission error in case of parsing file without access permission

        It checks:
        - PermissionError raised
        """
        # Create test file
        file_without_permission = os.path.join(TEST_FILES_PATH, "permission.csv")
        os.chmod(file_without_permission, 0o644)
        with open(file_without_permission, "w") as no_permission:
            no_permission.write(
                "Customer Name,Customer Postcode,SKU,Qty,Vehicle Type,Due Date\n"
            )
            no_permission.write("Alice,E1W 2RG,SKU123,57,trailer,2024-04-10\n")
            no_permission.write("Bob,N9 9LA,SKU456,1000,rigid,2023-11-10\n")

        # Change permission access to the file
        os.chmod(file_without_permission, 0o000)

        # Check for raising PermissionError
        parser = ParseCSV(file_without_permission)  #
        with self.assertRaises(PermissionError):
            parser.parse()

        # Setting file to original state, so it can be deleted and rewritten when test is run next time

    def test_inventory_parser(self) -> None:
        """
        Test parsing list of dictionaries.

        This test case verifies that InventoryParser class correctly parse and organised input list of dictionaries and return dictionary, which correctly groupt sum value and group key, where key is SKU and value Qty.


        It checks:
        - Qty when SKU is in parsed_data once and qty is 0
        - Qty when SKU is in parsed_data once and qty is positive Int
        - Qty when SKU is in parased_data more then once and qty is positive Int
        """
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
        ]

        # Initialize InventoryParser object
        parser = ParseCSV(None)
        parser.parsed_data = parsed_data
        # Parse the inventory
        inventory = parser.parse_inventory()
        # Verify the parsed data
        self.assertEqual(len(inventory), 3)
        self.assertEqual(inventory["SKU1"], 20)
        self.assertEqual(inventory["SKU2"], 0)
        self.assertEqual(inventory["SKU3"], 8)

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
        parser = ParseCSV(None)
        parser.parsed_data = parsed_data
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
