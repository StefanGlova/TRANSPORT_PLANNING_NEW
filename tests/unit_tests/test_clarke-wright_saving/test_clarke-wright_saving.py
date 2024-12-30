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

        self.assertEqual(len(distance), 1)
        self.assertEqual(distance[0]["postcode_1"], "DEF123")
        self.assertEqual(distance[0]["postcode_2"], "IJK123")
        self.assertAlmostEqual(distance[0]["distance"], 84.1169, places=2)

    def test_calculate_distance_between_two_postcodes_with_same_coordinates(self):
        """
        Test whether distance between two postcodes with the same coordinates is equal 0.
        """

        postcodes = {
            "DEF123": {"Latitude": 1.987654, "Longitude": 50.654987},
            "DEF121": {"Latitude": 1.987654, "Longitude": 50.654987},
        }

        saver = ClarkeWrightSavingCalculator.__new__(ClarkeWrightSavingCalculator)
        pairs = saver.create_pairs(postcodes)
        distance = saver.calculate_distance(postcodes, pairs, CIRCUITY_FACTOR)

        self.assertEqual(len(distance), 1)
        self.assertEqual(distance[0]["postcode_1"], "DEF123")
        self.assertEqual(distance[0]["postcode_2"], "DEF121")
        self.assertAlmostEqual(distance[0]["distance"], 0, places=2)

    def test_calculate_distance_between_postcodes_complex(self):
        """
        Test calculate distance with 5 postcodes which makes 10 pairs
        """

        postcodes = {
            "DEF123": {"Latitude": 1.987654, "Longitude": 50.654987},
            "IJK123": {"Latitude": 2.123456, "Longitude": 51.123456},
            "LMN123": {"Latitude": 3.987654, "Longitude": 52.654987},
            "OPQ123": {"Latitude": 4.123456, "Longitude": 53.123456},
            "RST123": {"Latitude": 5.987654, "Longitude": 54.654987},
        }

        saver = ClarkeWrightSavingCalculator.__new__(ClarkeWrightSavingCalculator)
        pairs = saver.create_pairs(postcodes)
        distance = saver.calculate_distance(postcodes, pairs, CIRCUITY_FACTOR)

        self.assertEqual(len(distance), 10)
        self.assertEqual(distance[0]["postcode_1"], "DEF123")
        self.assertEqual(distance[0]["postcode_2"], "IJK123")
        self.assertAlmostEqual(
            distance[0]["distance"],
            self._haversine_formula(1.987654, 2.123456, 50.654987, 51.123456),
            places=2,
        )
        self.assertEqual(distance[1]["postcode_1"], "DEF123")
        self.assertEqual(distance[1]["postcode_2"], "LMN123")
        self.assertAlmostEqual(
            distance[1]["distance"],
            self._haversine_formula(1.987654, 3.987654, 50.654987, 52.654987),
            places=2,
        )
        self.assertEqual(distance[2]["postcode_1"], "DEF123")
        self.assertEqual(distance[2]["postcode_2"], "OPQ123")
        self.assertAlmostEqual(
            distance[2]["distance"],
            self._haversine_formula(1.987654, 4.123456, 50.654987, 53.123456),
            places=2,
        )
        self.assertEqual(distance[3]["postcode_1"], "DEF123")
        self.assertEqual(distance[3]["postcode_2"], "RST123")
        self.assertAlmostEqual(
            distance[3]["distance"],
            self._haversine_formula(1.987654, 5.987654, 50.654987, 54.654987),
            places=2,
        )
        self.assertEqual(distance[4]["postcode_1"], "IJK123")
        self.assertEqual(distance[4]["postcode_2"], "LMN123")
        self.assertAlmostEqual(
            distance[4]["distance"],
            self._haversine_formula(2.123456, 3.987654, 51.123456, 52.654987),
            places=2,
        )
        self.assertEqual(distance[5]["postcode_1"], "IJK123")
        self.assertEqual(distance[5]["postcode_2"], "OPQ123")
        self.assertAlmostEqual(
            distance[5]["distance"],
            self._haversine_formula(2.123456, 4.123456, 51.123456, 53.123456),
            places=2,
        )
        self.assertEqual(distance[6]["postcode_1"], "IJK123")
        self.assertEqual(distance[6]["postcode_2"], "RST123")
        self.assertAlmostEqual(
            distance[6]["distance"],
            self._haversine_formula(2.123456, 5.987654, 51.123456, 54.654987),
            places=2,
        )
        self.assertEqual(distance[7]["postcode_1"], "LMN123")
        self.assertEqual(distance[7]["postcode_2"], "OPQ123")
        self.assertAlmostEqual(
            distance[7]["distance"],
            self._haversine_formula(3.987654, 4.123456, 52.654987, 53.123456),
            places=2,
        )
        self.assertEqual(distance[8]["postcode_1"], "LMN123")
        self.assertEqual(distance[8]["postcode_2"], "RST123")
        self.assertAlmostEqual(
            distance[8]["distance"],
            self._haversine_formula(3.987654, 5.987654, 52.654987, 54.654987),
            places=2,
        )
        self.assertEqual(distance[9]["postcode_1"], "OPQ123")
        self.assertEqual(distance[9]["postcode_2"], "RST123")
        self.assertAlmostEqual(
            distance[9]["distance"],
            self._haversine_formula(4.123456, 5.987654, 53.123456, 54.654987),
            places=2,
        )

    def test_calculate_distance_between_each_postcode_and_origin_simple(self):
        """
        Test for method calculate_distance_from_origin, simple version with just one postcode.
        """
        postcodes = {
            "DEF123": {"Latitude": 1.987654, "Longitude": 50.654987},
        }

        saver = ClarkeWrightSavingCalculator.__new__(ClarkeWrightSavingCalculator)
        distance_from_origin = saver.calculate_distance_from_origin(
            postcodes, ORIGIN_LAT, ORIGIN_LONG, CIRCUITY_FACTOR
        )

        self.assertEqual(len(distance_from_origin), 1)
        self.assertAlmostEqual(
            distance_from_origin["DEF123"],
            self._haversine_formula(ORIGIN_LAT, 1.987654, ORIGIN_LONG, 50.654987),
            places=2,
        )

    def test_calculate_distance_between_each_postcode_and_origin_complex(self):
        """
        Test for method calculate_distance_from_origin, more complex version with 5 postcodes.
        """
        postcodes = {
            "DEF123": {"Latitude": 1.987654, "Longitude": 50.654987},
            "IJK123": {"Latitude": 2.123456, "Longitude": 51.123456},
            "LMN123": {"Latitude": 3.987654, "Longitude": 52.654987},
            "OPQ123": {"Latitude": 4.123456, "Longitude": 53.123456},
            "RST123": {"Latitude": 5.987654, "Longitude": 54.654987},
        }

        saver = ClarkeWrightSavingCalculator.__new__(ClarkeWrightSavingCalculator)
        distance_from_origin = saver.calculate_distance_from_origin(
            postcodes, ORIGIN_LAT, ORIGIN_LONG, CIRCUITY_FACTOR
        )

        self.assertEqual(len(distance_from_origin), 5)
        self.assertAlmostEqual(
            distance_from_origin["DEF123"],
            self._haversine_formula(ORIGIN_LAT, 1.987654, ORIGIN_LONG, 50.654987),
            places=2,
        )
        self.assertAlmostEqual(
            distance_from_origin["IJK123"],
            self._haversine_formula(ORIGIN_LAT, 2.123456, ORIGIN_LONG, 51.123456),
            places=2,
        )
        self.assertAlmostEqual(
            distance_from_origin["LMN123"],
            self._haversine_formula(ORIGIN_LAT, 3.987654, ORIGIN_LONG, 52.654987),
            places=2,
        )
        self.assertAlmostEqual(
            distance_from_origin["OPQ123"],
            self._haversine_formula(ORIGIN_LAT, 4.123456, ORIGIN_LONG, 53.123456),
            places=2,
        )
        self.assertAlmostEqual(
            distance_from_origin["RST123"],
            self._haversine_formula(ORIGIN_LAT, 5.987654, ORIGIN_LONG, 54.654987),
            places=2,
        )

    def test_calculate_saving_simple(self):
        """
        Test to calculate saving if two postcodes are delivered together. Simple test, just with 2 postcodes.
        Result is returned in format of list of touples, sorted by saving value from largest:
        savings = [(postcode_1, postcode_2, saving), ...]
        """

        postcodes = {
            "DEF123": {"Latitude": 1.987654, "Longitude": 50.654987},
            "IJK123": {"Latitude": 1.123456, "Longitude": 50.123456},
        }

        saver = ClarkeWrightSavingCalculator.__new__(ClarkeWrightSavingCalculator)
        pairs = saver.create_pairs(postcodes)
        distance = saver.calculate_distance(postcodes, pairs, CIRCUITY_FACTOR)
        distance_from_origin = saver.calculate_distance_from_origin(
            postcodes, ORIGIN_LAT, ORIGIN_LONG, CIRCUITY_FACTOR
        )
        savings = saver.calculate_saving(distance, distance_from_origin)

        self.assertEqual(len(savings), 1)
        self.assertEqual(
            savings[0],
            (
                "DEF123",
                "IJK123",
                distance_from_origin["DEF123"]
                + distance_from_origin["IJK123"]
                - distance[0]["distance"],
            ),
        )

    def _haversine_formula(
        self,
        lat_1: float,
        lat_2: float,
        long_1: float,
        long_2: float,
        circuity: float = 1.2,
    ) -> float:
        from math import pi, sin, cos, acos

        haversine_distance = (
            3959
            * (
                acos(
                    sin(lat_1 * pi / 180) * sin(lat_2 * pi / 180)
                    + cos(lat_1 * pi / 180)
                    * cos(lat_2 * pi / 180)
                    * cos(long_1 * pi / 180 - long_2 * pi / 180)
                )
            )
            * circuity
        )
        return haversine_distance


if __name__ == "__main__":
    unittest.main()
