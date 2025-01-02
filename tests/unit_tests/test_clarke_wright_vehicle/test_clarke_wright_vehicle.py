import unittest


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


if __name__ == "__main__":
    unittest.main()
