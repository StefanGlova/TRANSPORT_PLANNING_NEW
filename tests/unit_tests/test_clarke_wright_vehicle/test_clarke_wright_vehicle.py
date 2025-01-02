import unittest

from src.clarke_wright_vehicle_module.clarke_wright_vehicle_planner import ClarkeWrightVehiclePlanner


# Testing parameters
TRAILER_MAX = 55
TRAILER_MIN = 50
RIGID_MAX = 25
RIGID_MIN = 20
PARCEL_LIMIT = 2


class TestClarkeWrightVehiclePlanner(unittest.TestCase):
    """ """

    def test_postcodes_count_one_postcode(self):
        """
        Test method postcodes_count which loops through orderbook and count how many times each postcode is used.
        """

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

        planner = ClarkeWrightVehiclePlanner()
        postcodes_count = planner.count_postcodes(orderbook=multidrop_loads_trailers)

        self.assertEqual(len(postcodes_count), 1)
        self.assertEqual(postcodes_count["ABC123"], 1)


    def test_postcodes_count_more_postcodes_all_same(self):
        """
        Test count of more then one postcode if all are same.
        """


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
                "Customer Name": "GHI",
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
                "Customer Name": "JKL",
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

        planner = ClarkeWrightVehiclePlanner()
        postcodes_count = planner.count_postcodes(orderbook=multidrop_loads_trailers)

        self.assertEqual(len(postcodes_count), 1)
        self.assertEqual(postcodes_count["ABC123"], 4)


    def test_postcodes_count_more_postcodes_different(self):
        """
        Test count of more then one postcode if they are not all same.
        """


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
                "Customer Name": "GHI",
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
                "Customer Name": "JKL",
                "Customer Postcode": "JKL123",
                "Total Volume": 5,
                "Line Details": {
                    "SKU": "SKU1",
                    "Qty": 60,
                    "Due Date": 2023 - 11 - 10,
                    "Allocated Volume": 5,
                },
            },
        ]

        planner = ClarkeWrightVehiclePlanner()
        postcodes_count = planner.count_postcodes(orderbook=multidrop_loads_trailers)

        self.assertEqual(len(postcodes_count), 2)
        self.assertEqual(postcodes_count["ABC123"], 3)
        self.assertEqual(postcodes_count["JKL123"], 1)

if __name__ == "__main__":
    unittest.main()
