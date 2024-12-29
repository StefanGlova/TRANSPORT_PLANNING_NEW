import unittest
from src.clarke_wright_saving_module.clarke_wright_saving_calculator import (
    ClarkeWrightSavingCalculator,
)
from src.errors import MissingPostcodeError, PairsCreationError

ORIGIN_LAT = 53.484253
ORIGIN_LONG = -1.18073
CIRCUITY_FACTOR = 1.2

class TestClarkeWrightSavingCalculator(unittest.TestCase):

    def test_used_postcodes_simple(self):

        all_postcodes = {
            "ABC123": {"Latitude": 1.123456, "Longitude": 50.123456},
            "EFG456": {"Latitude": 1.987654, "Longitude": 50.654987},
        }

        multidrop_loads_trailers = [
            {
                "Customer Name": "ABC",
                "Customer Postcode": "ABC123",
                "Total Volume": 5,
                "Line Details": {
                    "SKU": "SKU1",
                    "Qty": 60,
                    "Due Date": 2023 - 11 - 10,
                    "Allocated Volume": 5,
                },
            },
        ]

        saver = ClarkeWrightSavingCalculator(all_postcodes, multidrop_loads_trailers)
        postcodes = saver.select_used_postcodes()

        self.assertIn("ABC123", postcodes)
        self.assertNotIn("EFG456", postcodes)
        self.assertEqual(postcodes["ABC123"]["Latitude"], 1.123456)
        self.assertEqual(postcodes["ABC123"]["Longitude"], 50.123456)

    def test_used_postcodes_complex(self):

        all_postcodes = {
            "ABC123": {"Latitude": 1.123456, "Longitude": 50.123456},
            "DEF123": {"Latitude": 1.987654, "Longitude": 50.654987},
            "IJK123": {"Latitude": 1.123456, "Longitude": 50.123456},
            "LMN123": {"Latitude": 1.987654, "Longitude": 50.654987},
            "OPQ123": {"Latitude": 1.123456, "Longitude": 50.123456},
            "RST123": {"Latitude": 1.987654, "Longitude": 50.654987},
        }

        multidrop_loads_trailers = [
            {
                "Customer Name": "ABC",
                "Customer Postcode": "ABC123",
                "Total Volume": 5,
                "Line Details": {
                    "SKU": "SKU1",
                    "Qty": 60,
                    "Due Date": 2023 - 11 - 10,
                    "Allocated Volume": 5,
                },
            },
            {
                "Customer Name": "DEF",
                "Customer Postcode": "DEF123",
                "Total Volume": 5,
                "Line Details": {
                    "SKU": "SKU1",
                    "Qty": 60,
                    "Due Date": 2023 - 11 - 10,
                    "Allocated Volume": 5,
                },
            },
        ]
        multidrop_loads_rigids = [
            {
                "Customer Name": "ABC",
                "Customer Postcode": "ABC123",
                "Total Volume": 5,
                "Line Details": {
                    "SKU": "SKU1",
                    "Qty": 60,
                    "Due Date": 2023 - 11 - 10,
                    "Allocated Volume": 5,
                },
            },
            {
                "Customer Name": "IJK",
                "Customer Postcode": "IJK123",
                "Total Volume": 5,
                "Line Details": {
                    "SKU": "SKU1",
                    "Qty": 60,
                    "Due Date": 2023 - 11 - 10,
                    "Allocated Volume": 5,
                },
            },
        ]

        saver_trailers = ClarkeWrightSavingCalculator(
            all_postcodes, multidrop_loads_trailers
        )
        saver_rigids = ClarkeWrightSavingCalculator(
            all_postcodes, multidrop_loads_rigids
        )
        postcodes_trailers = saver_trailers.select_used_postcodes()
        postcodes_rigids = saver_rigids.select_used_postcodes()

        self.assertIn("ABC123", postcodes_trailers)
        self.assertIn("DEF123", postcodes_trailers)
        self.assertIn("ABC123", postcodes_rigids)
        self.assertIn("IJK123", postcodes_rigids)
        self.assertNotIn("LMN123", postcodes_rigids)
        self.assertNotIn("DEF123", postcodes_rigids)
        self.assertNotIn("IJK123", postcodes_trailers)
        self.assertEqual(postcodes_trailers["ABC123"]["Latitude"], 1.123456)
        self.assertEqual(postcodes_rigids["ABC123"]["Longitude"], 50.123456)
        counter = 0
        for _ in postcodes_rigids:
            counter += 1
        for _ in postcodes_trailers:
            counter += 1
        self.assertEqual(counter, 4)

    def test_used_postcodes_missing_postcode(self):

        all_postcodes = {
            "DEF123": {"Latitude": 1.987654, "Longitude": 50.654987},
            "IJK123": {"Latitude": 1.123456, "Longitude": 50.123456},
            "LMN123": {"Latitude": 1.987654, "Longitude": 50.654987},
            "OPQ123": {"Latitude": 1.123456, "Longitude": 50.123456},
            "RST123": {"Latitude": 1.987654, "Longitude": 50.654987},
        }

        multidrop_loads_trailers = [
            {
                "Customer Name": "ABC",
                "Customer Postcode": "ABC123",
                "Total Volume": 5,
                "Line Details": {
                    "SKU": "SKU1",
                    "Qty": 60,
                    "Due Date": 2023 - 11 - 10,
                    "Allocated Volume": 5,
                },
            },
            {
                "Customer Name": "DEF",
                "Customer Postcode": "DEF123",
                "Total Volume": 5,
                "Line Details": {
                    "SKU": "SKU1",
                    "Qty": 60,
                    "Due Date": 2023 - 11 - 10,
                    "Allocated Volume": 5,
                },
            },
        ]

        saver = ClarkeWrightSavingCalculator(all_postcodes, multidrop_loads_trailers)

        with self.assertRaises(MissingPostcodeError) as cm:
            saver.select_used_postcodes()

        self.assertEqual(
            str(cm.exception),
            "Postcode ABC123 is not in postcodes list. Please update postcodes database first",
        )

    def test_postcode_pairs_simple(self):
        """
        Simple test for method which creates postcode pairs.
        """

        postcodes = {
            "DEF123": {"Latitude": 1.987654, "Longitude": 50.654987},
            "IJK123": {"Latitude": 1.123456, "Longitude": 50.123456},
            "LMN123": {"Latitude": 1.987654, "Longitude": 50.654987},
            "OPQ123": {"Latitude": 1.123456, "Longitude": 50.123456},
            "RST123": {"Latitude": 1.987654, "Longitude": 50.654987},
        }

        saver = ClarkeWrightSavingCalculator.__new__(ClarkeWrightSavingCalculator)

        pairs = saver.create_pairs(postcodes)

        self.assertEqual(len(pairs), 10)
        self.assertIn(("DEF123", "IJK123"), pairs)
        self.assertIn(("DEF123", "LMN123"), pairs)
        self.assertIn(("DEF123", "OPQ123"), pairs)
        self.assertIn(("DEF123", "RST123"), pairs)
        self.assertIn(("IJK123", "LMN123"), pairs)
        self.assertIn(("IJK123", "RST123"), pairs)
        self.assertIn(("IJK123", "OPQ123"), pairs)
        self.assertIn(("LMN123", "RST123"), pairs)
        self.assertIn(("LMN123", "OPQ123"), pairs)
        self.assertIn(("OPQ123", "RST123"), pairs)
        self.assertNotIn(("DEF123", "DEF123"), pairs)
        self.assertNotIn(("IJK123", "IJK123"), pairs)
        self.assertNotIn(("LMN123", "LMN123"), pairs)
        self.assertNotIn(("OPQ123", "OPQ123"), pairs)
        self.assertNotIn(("RST123", "RST123"), pairs)
        self.assertIsInstance(pairs[0], tuple)
        self.assertIsInstance(pairs[1], tuple)
        self.assertIsInstance(pairs[2], tuple)
        self.assertIsInstance(pairs[3], tuple)
        self.assertIsInstance(pairs[4], tuple)
        self.assertIsInstance(pairs[5], tuple)
        self.assertIsInstance(pairs[6], tuple)
        self.assertIsInstance(pairs[7], tuple)
        self.assertIsInstance(pairs[8], tuple)
        self.assertIsInstance(pairs[9], tuple)

    def test_postcode_pairs_duplicated_postcodes(self):
        """
        Simple test for method which creates postcode pairs.
        """

        postcodes = {
            "DEF123": {"Latitude": 1.987654, "Longitude": 50.654987},
            "IJK123": {"Latitude": 1.123456, "Longitude": 50.123456},
            "LMN123": {"Latitude": 1.987654, "Longitude": 50.654987},
            "OPQ123": {"Latitude": 1.123456, "Longitude": 50.123456},
            "RST123": {"Latitude": 1.987654, "Longitude": 50.654987},
            "DEF123": {"Latitude": 1.987654, "Longitude": 50.654987},
            "IJK123": {"Latitude": 1.123456, "Longitude": 50.123456},
            "LMN123": {"Latitude": 1.987654, "Longitude": 50.654987},
            "OPQ123": {"Latitude": 1.123456, "Longitude": 50.123456},
            "RST123": {"Latitude": 1.987654, "Longitude": 50.654987},
        }

        saver = ClarkeWrightSavingCalculator.__new__(ClarkeWrightSavingCalculator)

        pairs = saver.create_pairs(postcodes)

        self.assertEqual(len(pairs), 10)
        self.assertIn(("DEF123", "IJK123"), pairs)
        self.assertIn(("DEF123", "LMN123"), pairs)
        self.assertIn(("DEF123", "OPQ123"), pairs)
        self.assertIn(("DEF123", "RST123"), pairs)
        self.assertIn(("IJK123", "LMN123"), pairs)
        self.assertIn(("IJK123", "RST123"), pairs)
        self.assertIn(("IJK123", "OPQ123"), pairs)
        self.assertIn(("LMN123", "RST123"), pairs)
        self.assertIn(("LMN123", "OPQ123"), pairs)
        self.assertIn(("OPQ123", "RST123"), pairs)
        self.assertNotIn(("DEF123", "DEF123"), pairs)
        self.assertNotIn(("IJK123", "IJK123"), pairs)
        self.assertNotIn(("LMN123", "LMN123"), pairs)
        self.assertNotIn(("OPQ123", "OPQ123"), pairs)
        self.assertNotIn(("RST123", "RST123"), pairs)
        self.assertIsInstance(pairs[0], tuple)
        self.assertIsInstance(pairs[1], tuple)
        self.assertIsInstance(pairs[2], tuple)
        self.assertIsInstance(pairs[3], tuple)
        self.assertIsInstance(pairs[4], tuple)
        self.assertIsInstance(pairs[5], tuple)
        self.assertIsInstance(pairs[6], tuple)
        self.assertIsInstance(pairs[7], tuple)
        self.assertIsInstance(pairs[8], tuple)
        self.assertIsInstance(pairs[9], tuple)

    def test_postcode_pairs_empty_input(self):
        """
        Tests for empty input
        """

        postcodes = dict()

        saver = ClarkeWrightSavingCalculator.__new__(ClarkeWrightSavingCalculator)

        with self.assertRaises(PairsCreationError) as cm:
            pairs = saver.create_pairs(postcodes)

        self.assertEqual(
            str(cm.exception), "To create pairs, there must be at least 2 postcodes."
        )

    def test_postcode_pairs_single_postcode(self):
        """
        Test for just 1 postcode
        """

        postcodes = {"DEF123": {"Latitude": 1.987654, "Longitude": 50.654987}}

        saver = ClarkeWrightSavingCalculator.__new__(ClarkeWrightSavingCalculator)

        with self.assertRaises(PairsCreationError) as cm:
            pairs = saver.create_pairs(postcodes)

        self.assertEqual(
            str(cm.exception), "To create pairs, there must be at least 2 postcodes."
        )

    def test_calculate_distance_between_postcodes_simple(self):
        """
        Test whether distance between two postcodes is calculated correctly.
        Output should be in format of list of dicts
        distance = [
        {
            "postcode_1": "DEF123"
            "postcode_2": "IJK123"
            "distance": some floating number
        },
        ]
        """

        postcodes = {
            "DEF123": {"Latitude": 1.987654, "Longitude": 50.654987},
            "IJK123": {"Latitude": 1.123456, "Longitude": 50.123456},
        }

        saver = ClarkeWrightSavingCalculator.__new__(ClarkeWrightSavingCalculator)
        pairs = saver.create_pairs(postcodes)
        distance = saver.calculate_distance(postcodes, pairs, CIRCUITY_FACTOR)

        expected_distance = self._haversine_formula(1.987654, 1.123456, 50.654987, 50.123456)

        self.assertEqual(len(distance), 1)
        self.assertEqual(distance[0]["postcode_1"], "DEF123")
        self.assertEqual(distance[0]["postcode_2"], "IJK123")
        self.assertAlmostEqual(distance[0]["distance"], expected_distance, places=2)



    def _haversine_formula(self, lat_1: float, lat_2: float, long_1: float, long_2: float, circuity: float = 1.2) -> float:
        from math import pi, sin, cos, acos

        haversine_distance = 3959 * (acos(sin(lat_1 * pi / 180) * sin(lat_2 * pi / 180)
                                    + cos(lat_1 * pi / 180) * cos(lat_2 * pi / 180)
                                    * cos(long_1 * pi / 180 - long_2 * pi / 180)
                                    )) * circuity
        return haversine_distance

if __name__ == "__main__":
    unittest.main()
