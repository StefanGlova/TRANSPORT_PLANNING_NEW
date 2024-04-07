import unittest
from postcode_parser import PostcodeParser


class TestPostcodeParser(unittest.TestCase):
    """
    Test suite for PostcodeParser class.
    """

    def test_postcode_parser(self) -> None:
        """
        Test parsing list of dictionaries.

        This test case verifies that PostcodeParser class correctly parse and organised input list of dictionaries and return dictionary, which correctly process latitude and longitude for each postcode.


        It checks:
        - Number of elements in postcode dict
        - Correct nasted datastructure of postcode dict where top level key is postcode with value of dict with two keys - latitude and longitude
        - Latitude of each postcode is correct value and type (float)
        - Longitude of each postcode is correct value and type (float)
        """
        # Create parsed_data list of dicts for testing purpose
        parsed_data = [
            {"Postcode": "ABC", "Latitude": "1.123456", "Longitude": "50.123456"},
            {"Postcode": "EFG", "Latitude": "1.987654", "Longitude": "50.654987"},
        ]
        # Initialize PostcodeParser object
        parser = PostcodeParser(parsed_data)
        # Parse the postcodes
        postcodes = parser.parse_postcodes()
        # Verify parsed data
        self.assertEqual(len(postcodes), 2)
        self.assertEqual(postcodes["ABC"]["Latitude"], 1.123456)
        self.assertEqual(postcodes["ABC"]["Longitude"], 50.123456)
        self.assertEqual(postcodes["EFG"]["Latitude"], 1.987654)
        self.assertEqual(postcodes["EFG"]["Longitude"], 50.654987)


if __name__ == "__main__":
    unittest.main()
