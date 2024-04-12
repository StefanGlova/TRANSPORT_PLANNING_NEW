import unittest
from modules.data_processing_module.process_postcodes import ProcessPostcodes
from modules.errors import WrongKeysError, WrongValueTypeError, WrongNumericRange

PARSER = ProcessPostcodes(None)
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

    def test_postcodes_wrong_value_type(self):
        print("test Postcode wrong value type")

        parsed_data = [
            {"Postcode": "ABC", "Latitude": "ABC", "Longitude": "50.123456"},
            {"Latitude": "1.987654", "Postcode": "EFG", "Longitude": "50.654987"},
        ]

        PARSER.parsed_data = parsed_data

        with self.assertRaises(WrongValueTypeError) as context:
            postcodes = PARSER.parse_postcodes()
            self.assertEqual(
                str(context.exception),
                "Parameter Latitude must be Decimal place number",
            )

    def test_postcodes_number_range(self):
        print("test Postcodes numbers range")

        parsed_data = [
            # Latitude edge cases
            {"Postcode": "ABC", "Latitude": "-90", "Longitude": "50.123456"},
            {"Postcode": "ABC", "Latitude": "90", "Longitude": "50.123456"},
            {"Postcode": "ABC", "Latitude": "-90.001", "Longitude": "50.123456"},
            {"Postcode": "ABC", "Latitude": "90.001", "Longitude": "50.123456"},
            {"Postcode": "ABC", "Latitude": "0", "Longitude": "50.123456"},
            {"Postcode": "ABC", "Latitude": "-1", "Longitude": "50.123456"},
            {"Postcode": "ABC", "Latitude": "1", "Longitude": "50.123456"},
            {"Postcode": "ABC", "Latitude": "-180", "Longitude": "50.123456"},
            {"Postcode": "ABC", "Latitude": "180", "Longitude": "50.123456"},
            # Longitude edge cases
            {"Postcode": "ABC", "Latitude": "1.987654", "Longitude": "-180"},
            {"Postcode": "ABC", "Latitude": "1.987654", "Longitude": "180"},
            {"Postcode": "ABC", "Latitude": "1.987654", "Longitude": "-180.001"},
            {"Postcode": "ABC", "Latitude": "1.987654", "Longitude": "180.001"},
            {"Postcode": "ABC", "Latitude": "1.987654", "Longitude": "0"},
            {"Postcode": "ABC", "Latitude": "1.987654", "Longitude": "-1"},
            {"Postcode": "ABC", "Latitude": "1.987654", "Longitude": "1"},
            {"Postcode": "ABC", "Latitude": "1.987654", "Longitude": "-200"},
            {"Postcode": "ABC", "Latitude": "1.987654", "Longitude": "200"},
        ]

        PARSER.parsed_data = parsed_data

        # latitude_range = [-90, 90]
        # longitude_range = [-180, 180]

        for line in parsed_data:
            lat = float(line["Latitude"])
            long = float(line["Longitude"])
            if lat < -90 or lat > 90:
                with self.assertRaises(WrongNumericRange) as context:
                    postcodes = PARSER.parse_postcodes()
                    self.assertEqual(
                        str(context.exception),
                        "Parameter Latitude must be in range from -90 to +90",
                    )
            if long < -180 or long > 180:
                with self.assertRaises(WrongNumericRange) as context:
                    postcodes = PARSER.parse_postcodes()
                    self.assertEqual(
                        str(context.exception),
                        "Parameter Longitude must be in range from -180 to +180",
                    )


if __name__ == "__main__":
    unittest.main()
