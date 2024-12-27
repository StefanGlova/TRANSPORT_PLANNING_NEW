import unittest
from src.clarke_wright_saving_module.clarke_wright_saving_calculator import ClarkeWrightSavingCalculator

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



if __name__ == "__main__":
    unittest.main()
