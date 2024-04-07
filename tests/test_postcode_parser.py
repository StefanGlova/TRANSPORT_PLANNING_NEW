import unittest


class TestPostcodeParser(unittest.TestCase):
    """
    Test suite for PostcodeParser class.
    """

    def test_postcode_parser(self) -> None:

        parsed_data = [
            {"Postcode": "ABC", "Latitude": "1.123456", "Longitude": "50.123456"},
            {"Postcode": "EFG", "Latitude": "1.987654", "Longitude": "50.654987"},
        ]

        parser = PostcodeParser(parsed_data)
        postcodes = parser.parse_postcodes()

        self.assertEqual(len(postcodes), 2)
        self.assertEqual(postcodes[0]["Postcode"], "ABC")
        self.assertEqual(postcodes[0]["Latitude"], 1.123456)
        self.assertEqual(postcodes[0]["Longitude"], 50.123456)
        self.assertEqual(postcodes[1]["Postcode"], "EFG")
        self.assertEqual(postcodes[1]["Latitude"], 1.987654)
        self.assertEqual(postcodes[1]["Longitude"], 50.654987)


if __name__ == "__main__":
    unittest.main()
