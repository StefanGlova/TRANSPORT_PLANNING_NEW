import unittest
from src.clarke_wright_saving_module.clarke_wright_saving_calculator import ClarkeWrightSavingCalculator
from src.errors import MissingPostcodeError

class TestClarkeWrightSavingCalculator(unittest.TestCase):

    def test_used_postcodes_simple(self):

        all_postcodes = {
            "ABC123": {"Latitude": 1.123456, "Longitude": 50.123456},
            "EFG456": {"Latitude": 1.987654, "Longitude": 50.654987},
        }

        orderbook = {
            "trailer": [
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
        }

        saver = ClarkeWrightSavingCalculator(all_postcodes, orderbook)
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

        orderbook = {
            "trailer": [
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
            ],
            "rigid": [
                {
                    "Customer Name": "ABC",
                    "Customer Postcode": "IJK123",
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
                    "Customer Postcode": "ABC123",
                    "Total Volume": 5,
                    "Line Details": {
                        "SKU": "SKU1",
                        "Qty": 60,
                        "Due Date": 2023 - 11 - 10,
                        "Allocated Volume": 5,
                    },
                },
            ],            
        }

        saver = ClarkeWrightSavingCalculator(all_postcodes, orderbook)
        postcodes = saver.select_used_postcodes()

        self.assertIn("ABC123", postcodes)
        self.assertIn("DEF123", postcodes)
        self.assertIn("IJK123", postcodes)
        self.assertNotIn("LMN123", postcodes)
        self.assertNotIn("OPQ123", postcodes)
        self.assertNotIn("RST123", postcodes)
        self.assertEqual(postcodes["ABC123"]["Latitude"], 1.123456)
        self.assertEqual(postcodes["ABC123"]["Longitude"], 50.123456)
        counter = 0
        for _ in postcodes:
            counter += 1
        self.assertEqual(counter, 3)

    def test_used_postcodes_missing_postcode(self):

        all_postcodes = {
            "DEF123": {"Latitude": 1.987654, "Longitude": 50.654987},
            "IJK123": {"Latitude": 1.123456, "Longitude": 50.123456},
            "LMN123": {"Latitude": 1.987654, "Longitude": 50.654987},
            "OPQ123": {"Latitude": 1.123456, "Longitude": 50.123456},
            "RST123": {"Latitude": 1.987654, "Longitude": 50.654987},            
        }

        orderbook = {
            "trailer": [
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
            ],
            "rigid": [
                {
                    "Customer Name": "ABC",
                    "Customer Postcode": "IJK123",
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
                    "Customer Postcode": "ABC123",
                    "Total Volume": 5,
                    "Line Details": {
                        "SKU": "SKU1",
                        "Qty": 60,
                        "Due Date": 2023 - 11 - 10,
                        "Allocated Volume": 5,
                    },
                },
            ],            
        }

        saver = ClarkeWrightSavingCalculator(all_postcodes, orderbook)
 
        with self.assertRaises(MissingPostcodeError):
            saver.select_used_postcodes()


if __name__ == "__main__":
    unittest.main()
