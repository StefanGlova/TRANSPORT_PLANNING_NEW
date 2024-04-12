import unittest
from modules.data_processing_module.parse_csv import GeneralFileParser
from modules.errors import WrongKeysError

PARSER = GeneralFileParser(None)
CORRECT_KEYS = ["Postcode", "Latitude", "Longitude"]


class TestPostcodeParser(unittest.TestCase):

    def test_postcode_correct_input(self) -> None:
        """
        Test parsing list of dictionaries.

        This test case verifies that PostcodeParser class correctly parse and organised input list of dictionaries and return dictionary, which correctly process latitude and longitude for each postcode.


        It checks:
        - Number of elements in postcode dict
        - Correct nasted datastructure of postcode dict where top level key is postcode with value of dict with two keys - latitude and longitude
        - Latitude of each postcode is correct value and type (float)
        - Longitude of each postcode is correct value and type (float)
        - Whether each dictionary in input list only contains correct keys and if not it checks for raising custome WrongKeyError with correct message
        """

        print("test Postcode correct")

        # Create parsed_data list of dicts for testing purpose
        parsed_data = [
            {"Postcode": "ABC", "Latitude": "1.123456", "Longitude": "50.123456"},
            # Correct keys but different order
            {"Latitude": "1.987654", "Postcode": "EFG", "Longitude": "50.654987"},
        ]
        # Initialize PostcodeParser object
        PARSER.parsed_data = parsed_data
        # Parse the postcodes
        postcodes = PARSER.parse_postcodes()
        # Verify parsed data
        self.assertEqual(len(postcodes), 2)
        self.assertEqual(postcodes["ABC"]["Latitude"], 1.123456)
        self.assertEqual(postcodes["ABC"]["Longitude"], 50.123456)
        self.assertEqual(postcodes["EFG"]["Latitude"], 1.987654)
        self.assertEqual(postcodes["EFG"]["Longitude"], 50.654987)

    def test_postcodes_incorrect_inputs(self):

        print("test Postcode incorrect")

        # Initialize different options of keys in parsed_data dictionary
        not_enough_keys_1 = [
            {"Postcode": "ABC", "Longitude": "50.123456"},
            {"Latitude": "1.987654", "Postcode": "EFG", "Longitude": "50.654987"},
        ]

        not_enough_keys_2 = [
            {"Latitude": "1.987654", "Postcode": "EFG", "Longitude": "50.654987"},
            {},
        ]

        empty_dictionary = [{}]
        empty_list = []

        wrong_keys_1 = [
            {"postcode": "ABC", "Latitude": "1.123456", "Longitude": "50.123456"},
            {"Latitude": "1.987654", "Postcode": "EFG", "Longitude": "50.654987"},
        ]

        wrong_keys_2 = [
            {"Postcode": "ABC", "Latitude": "1.123456", "Longitude": "50.123456"},
            {"Postcode": "EFG", "Lat": "1.987654", "Long": "50.654987"},
        ]

        too_many_keys = [
            {"Postcode": "ABC", "Latitude": "1.123456", "Longitude": "50.123456"},
            {
                "Latitude": "1.987654",
                "Postcode": "EFG",
                "Longitude": "50.654987",
                "Distance": "125",
            },
        ]

        all_wrong_keys = [
            not_enough_keys_1,
            not_enough_keys_2,
            empty_dictionary,
            empty_list,
            wrong_keys_1,
            wrong_keys_2,
            too_many_keys,
        ]

        # Iterate though list of lists with various wrong keys and asserting whether it raises correctly WrongKeyError

        for data in all_wrong_keys:
            keys_set = sorted(list(set(key for d in data for key in d.keys())))
            PARSER.parsed_data = data
            if keys_set != sorted(CORRECT_KEYS):
                with self.assertRaises(WrongKeysError) as context:
                    orders_by_vehicle = PARSER.parse_postcodes()
                # Check for correct Error message
                self.assertEqual(
                    str(context.exception),
                    "Function parse_postcodes only accepts these keys Postcode, Latitude, Longitude!",
                )


if __name__ == "__main__":
    unittest.main()
