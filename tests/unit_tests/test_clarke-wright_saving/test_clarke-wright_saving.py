import unittest
from src.clarke_wright_saving_module.clarke_wright_saving_calculator import ClarkeWrightSavingCalculator
from src.errors import MissingPostcodeError

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


        saver_trailers = ClarkeWrightSavingCalculator(all_postcodes, multidrop_loads_trailers)
        saver_rigids = ClarkeWrightSavingCalculator(all_postcodes, multidrop_loads_rigids)
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
 
        with self.assertRaises(MissingPostcodeError):
            saver.select_used_postcodes()


if __name__ == "__main__":
    unittest.main()
