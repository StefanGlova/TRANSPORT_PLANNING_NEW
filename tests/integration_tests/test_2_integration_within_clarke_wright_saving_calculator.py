import unittest
from src.clarke_wright_saving_module.clarke_wright_saving_calculator import (
    ClarkeWrightSavingCalculator,
)


class TestClarkeWrightSavingCalculatorIntegration(unittest.TestCase):

    def test_clarke_wright_saving_calculator_simple(self):

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
            {
                "Customer Name": "EFG",
                "Customer Postcode": "EFG456",
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
        pairs = saver.create_pairs(postcodes)

        self.assertEqual(len(pairs), 1)
        self.assertIn(("ABC123", "EFG456"), pairs)
        self.assertNotIn(("ABC123", "ABC123"), pairs)
        self.assertNotIn(("EFG456", "EFG456"), pairs)
        self.assertIsInstance(pairs[0], tuple)

    def test_clarke_wright_saving_calculator_large_dataset(self):
        """
        Test integration between select_used_postcodes and create_pairs in large dataset
        """

        all_postcodes = {
            f"PC{i:03}": {"Latitude": i, "Longitude": -i} for i in range(1, 1001)
        }
        orderbook = [
            {
                "Customer Name": f"Customer {i}",
                "Customer Postcode": f"PC{i:03}",
                "Total Volume": 5,
            }
            for i in range(1, 500)
        ]
        saver = ClarkeWrightSavingCalculator(all_postcodes, orderbook)
        postcodes = saver.select_used_postcodes()
        pairs = saver.create_pairs(postcodes)
        self.assertEqual(len(pairs), 124251)


if __name__ == "__main__":
    unittest.main()
