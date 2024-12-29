import unittest
from src.allocate_inventory_module.inventory_allocation import InventoryAllocation

from src.errors import EmptyDatasetError, WrongKeysAllocatorError

# Testing parameters
TRAILER_MAX = 55
TRAILER_MIN = 50
RIGID_MAX = 25
RIGID_MIN = 20
PARCEL_LIMIT = 2

class TestInventoryAllocation(unittest.TestCase):
    """
    Test suit for Inventory Allocation
    """

    def test_inventory_allocation_simple_case(self):
        """
        Very basic, simple test for checking allocate_inventory method of the class InventoryAllocation.

        This test case create simple orderbook sample and inventory sample with just one order and one SKU in inventory. Available inventory is higher than qty on order.

        It checks:
        - allocate_inventory correctly crete another key in order dictionary "Allocated Qty" and check that qty assigned to it as value is correct.
        - inventory left has correct value after allocating inventory to the order
        - that orderbook_not_allocated does not have any value against vehicle type
        """
        print("test Inventory Allocation simple case")

        # Create orderbook sample with just one order
        orderbook = {
            "trailer": [
                {
                    "Customer Name": "ABC",
                    "Customer Postcode": "ABC123",
                    "SKU": "SKU1",
                    "Qty": 60,
                    "Due Date": 2023 - 11 - 10,
                    "Transport Volume (m3)": 60,
                },
            ]
        }

        # Create inventory sample with just one sku
        inventory = {
            "SKU1": 100,
        }

        # Create allocator as object of InventoryAllocation class and run allocate_inventory method on the created object
        allocator = InventoryAllocation(orderbook, inventory)
        orderbook_allocated, inventory_left, orderbook_not_allocated = (
            allocator.allocate_inventory()
        )

        # Verify the outcome of allocate_inventory method
        self.assertEqual(orderbook_allocated["trailer"][0]["Allocated Qty"], 60)
        self.assertEqual(orderbook_allocated["trailer"][0]["Allocated Volume"], 60)
        self.assertEqual(inventory_left["SKU1"], 40)
        self.assertEqual(orderbook_not_allocated["trailer"], [])

    def test_inventory_allocation_two_orders_case(self):
        """
        Similar to simple case, but 2 orders for same SKU and same vehicle type. Also 2nd different sku which is not used in any of orders.
        """
        print("test Inventory Allocation  2 orders case")

        # Create orderbook sample with just one order
        orderbook = {
            "trailer": [
                {
                    "Customer Name": "ABC",
                    "Customer Postcode": "ABC123",
                    "SKU": "SKU1",
                    "Qty": 60,
                    "Due Date": 2023 - 11 - 10,
                    "Transport Volume (m3)": 60,
                },
                {
                    "Customer Name": "XYZ",
                    "Customer Postcode": "XYZ123",
                    "SKU": "SKU1",
                    "Qty": 30,
                    "Due Date": 2023 - 11 - 10,
                    "Transport Volume (m3)": 30,
                },
            ]
        }

        # Create inventory sample with just one sku
        inventory = {
            "SKU1": 100,
            "SKU2": 100,
        }

        # Create allocator as object of InventoryAllocation class and run allocate_inventory method on the created object
        allocator = InventoryAllocation(orderbook, inventory)
        orderbook_allocated, inventory_left, orderbook_not_allocated = (
            allocator.allocate_inventory()
        )

        # Verify the outcome of allocate_inventory method
        self.assertEqual(orderbook_allocated["trailer"][0]["Allocated Qty"], 60)
        self.assertEqual(orderbook_allocated["trailer"][1]["Allocated Qty"], 30)
        self.assertEqual(orderbook_allocated["trailer"][0]["Allocated Volume"], 60)
        self.assertEqual(orderbook_allocated["trailer"][1]["Allocated Volume"], 30)
        self.assertEqual(inventory_left["SKU1"], 10)
        self.assertEqual(inventory_left["SKU2"], 100)
        self.assertEqual(orderbook_not_allocated["trailer"], [])

    def test_inventory_allocation_simple_case_no_enough_inventory_volume_recalculation(
        self,
    ):
        """
        Test case similar to simple case, but with not enough inventory to test correct recalulation of allocated volume
        """

        # Create orderbook sample with just one order
        orderbook = {
            "trailer": [
                {
                    "Customer Name": "ABC",
                    "Customer Postcode": "ABC123",
                    "SKU": "SKU1",
                    "Qty": 60,
                    "Due Date": 2023 - 11 - 10,
                    "Transport Volume (m3)": 60,
                },
            ]
        }

        # Create inventory sample with just one sku
        inventory = {
            "SKU1": 50,
        }

        # Create allocator as object of InventoryAllocation class and run allocate_inventory method on the created object
        allocator = InventoryAllocation(orderbook, inventory)
        orderbook_allocated, inventory_left, orderbook_not_allocated = (
            allocator.allocate_inventory()
        )

        # Verify the outcome of allocate_inventory method
        self.assertEqual(orderbook_allocated["trailer"][0]["Allocated Qty"], 50)
        self.assertEqual(orderbook_allocated["trailer"][0]["Allocated Volume"], 50)
        self.assertEqual(inventory_left["SKU1"], 0)
        self.assertEqual(
            orderbook_not_allocated["trailer"][0]["Transport Volume (m3)"], 10.0
        )

    def test_inventory_allocation_two_orders_case_no_enough_inventory_volume_recalculation(
        self,
    ):
        """
        Similar to test_inventory_allocation_two_orders, but testing for volume recalculation if not enough invcentory.
        """

        # Create orderbook sample with just one order
        orderbook = {
            "trailer": [
                {
                    "Customer Name": "ABC",
                    "Customer Postcode": "ABC123",
                    "SKU": "SKU1",
                    "Qty": 60,
                    "Due Date": 2023 - 11 - 10,
                    "Transport Volume (m3)": 60,
                },
                {
                    "Customer Name": "XYZ",
                    "Customer Postcode": "XYZ123",
                    "SKU": "SKU1",
                    "Qty": 30,
                    "Due Date": 2023 - 11 - 10,
                    "Transport Volume (m3)": 30,
                },
            ]
        }

        # Create inventory sample with just one sku
        inventory = {
            "SKU1": 50,
            "SKU2": 100,
        }

        # Create allocator as object of InventoryAllocation class and run allocate_inventory method on the created object
        allocator = InventoryAllocation(orderbook, inventory)
        orderbook_allocated, inventory_left, orderbook_not_allocated = (
            allocator.allocate_inventory()
        )

        # Verify the outcome of allocate_inventory method
        self.assertEqual(orderbook_allocated["trailer"][0]["Customer Name"], "ABC")
        self.assertEqual(orderbook_not_allocated["trailer"][0]["Customer Name"], "ABC")
        self.assertEqual(orderbook_not_allocated["trailer"][1]["Customer Name"], "XYZ")
        self.assertEqual(orderbook_allocated["trailer"][0]["Allocated Qty"], 50)
        self.assertEqual(orderbook_allocated["trailer"][0]["Allocated Volume"], 50)
        self.assertEqual(orderbook_not_allocated["trailer"][0]["Qty"], 10)
        self.assertEqual(
            orderbook_not_allocated["trailer"][0]["Transport Volume (m3)"], 10
        )
        self.assertEqual(orderbook_not_allocated["trailer"][1]["Qty"], 30)
        self.assertEqual(
            orderbook_not_allocated["trailer"][1]["Transport Volume (m3)"], 30
        )
        self.assertEqual(inventory_left["SKU1"], 0)
        self.assertEqual(inventory_left["SKU2"], 100)

    def test_inventory_allocation_complex_case(self):
        """ """
        print("test Inventory Allocation complex case")

        # Create orderbook sample with just one order
        orderbook = {
            "trailer": [
                {
                    "Customer Name": "ABC",
                    "Customer Postcode": "ABC123",
                    "SKU": "SKU1",
                    "Qty": 1000,
                    "Due Date": 2023 - 11 - 10,
                    "Transport Volume (m3)": 1000,
                },
                {
                    "Customer Name": "XYZ",
                    "Customer Postcode": "XYZ123",
                    "SKU": "SKU2",
                    "Qty": 30,
                    "Due Date": 2023 - 11 - 10,
                    "Transport Volume (m3)": 30,
                },
                {
                    "Customer Name": "EFG",
                    "Customer Postcode": "XYZ123",
                    "SKU": "SKU6",
                    "Qty": 100,
                    "Due Date": 2023 - 11 - 10,
                    "Transport Volume (m3)": 100,
                },
                {
                    "Customer Name": "EFG",
                    "Customer Postcode": "XYZ123",
                    "SKU": "SKU4",
                    "Qty": 50,
                    "Due Date": 2023 - 11 - 10,
                    "Transport Volume (m3)": 50,
                },
                {
                    "Customer Name": "EFG",
                    "Customer Postcode": "XYZ123",
                    "SKU": "SKU6",
                    "Qty": 100,
                    "Due Date": 2023 - 11 - 10,
                    "Transport Volume (m3)": 100,
                },
                {
                    "Customer Name": "EFG",
                    "Customer Postcode": "XYZ123",
                    "SKU": "SKU5",
                    "Qty": 50,
                    "Due Date": 2023 - 11 - 10,
                    "Transport Volume (m3)": 50,
                },
                {
                    "Customer Name": "EFG",
                    "Customer Postcode": "XYZ123",
                    "SKU": "SKU6",
                    "Qty": 200,
                    "Due Date": 2023 - 11 - 10,
                    "Transport Volume (m3)": 200,
                },
            ],
            "rigid": [
                {
                    "Customer Name": "ABC",
                    "Customer Postcode": "ABC123",
                    "SKU": "SKU2",
                    "Qty": 60,
                    "Due Date": 2023 - 11 - 10,
                    "Transport Volume (m3)": 60,
                },
                {
                    "Customer Name": "EFG",
                    "Customer Postcode": "XYZ123",
                    "SKU": "SKU6",
                    "Qty": 100,
                    "Due Date": 2023 - 11 - 10,
                    "Transport Volume (m3)": 100,
                },
                {
                    "Customer Name": "XYZ",
                    "Customer Postcode": "XYZ123",
                    "SKU": "SKU3",
                    "Qty": 30,
                    "Due Date": 2023 - 11 - 10,
                    "Transport Volume (m3)": 30,
                },
                {
                    "Customer Name": "EFG",
                    "Customer Postcode": "XYZ123",
                    "SKU": "SKU6",
                    "Qty": 100,
                    "Due Date": 2023 - 11 - 10,
                    "Transport Volume (m3)": 100,
                },
                {
                    "Customer Name": "XYZ",
                    "Customer Postcode": "XYZ123",
                    "SKU": "SKU5",
                    "Qty": 100,
                    "Due Date": 2023 - 11 - 10,
                    "Transport Volume (m3)": 100,
                },
                {
                    "Customer Name": "EFG",
                    "Customer Postcode": "XYZ123",
                    "SKU": "SKU6",
                    "Qty": 200,
                    "Due Date": 2023 - 11 - 10,
                    "Transport Volume (m3)": 100,
                },
            ],
        }

        # Create inventory sample with just one sku
        inventory = {"SKU1": 100, "SKU2": 100, "SKU4": 0, "SKU5": 100, "SKU6": 2000}

        # Create allocator as object of InventoryAllocation class and run allocate_inventory method on the created object
        allocator = InventoryAllocation(orderbook, inventory)
        orderbook_allocated, inventory_left, orderbook_not_allocated = (
            allocator.allocate_inventory()
        )

        # Verify the outcome of allocate_inventory method
        # length of orderbook_allocated and orderbook_not_allocated to match expected values
        self.assertEqual(len(orderbook_allocated["trailer"]), 6)
        self.assertEqual(len(orderbook_allocated["rigid"]), 5)
        self.assertEqual(len(orderbook_not_allocated["trailer"]), 2)
        self.assertEqual(len(orderbook_not_allocated["rigid"]), 2)
        # Trailers - Allocated qty match expected values
        self.assertEqual(orderbook_allocated["trailer"][0]["SKU"], "SKU1")
        self.assertEqual(orderbook_allocated["trailer"][0]["Allocated Qty"], 100)
        self.assertEqual(orderbook_allocated["trailer"][1]["SKU"], "SKU2")
        self.assertEqual(orderbook_allocated["trailer"][1]["Allocated Qty"], 30)
        self.assertEqual(orderbook_allocated["trailer"][2]["SKU"], "SKU6")
        self.assertEqual(orderbook_allocated["trailer"][2]["Allocated Qty"], 100)
        self.assertEqual(orderbook_allocated["trailer"][3]["SKU"], "SKU6")
        self.assertEqual(orderbook_allocated["trailer"][3]["Allocated Qty"], 100)
        self.assertEqual(orderbook_allocated["trailer"][4]["SKU"], "SKU5")
        self.assertEqual(orderbook_allocated["trailer"][4]["Allocated Qty"], 50)
        self.assertEqual(orderbook_allocated["trailer"][5]["SKU"], "SKU6")
        self.assertEqual(orderbook_allocated["trailer"][5]["Allocated Qty"], 200)
        # Rigids - Allocated qty match expected values
        self.assertEqual(orderbook_allocated["rigid"][0]["SKU"], "SKU2")
        self.assertEqual(orderbook_allocated["rigid"][0]["Allocated Qty"], 60)
        self.assertEqual(orderbook_allocated["rigid"][1]["SKU"], "SKU6")
        self.assertEqual(orderbook_allocated["rigid"][1]["Allocated Qty"], 100)
        self.assertEqual(orderbook_allocated["rigid"][2]["SKU"], "SKU6")
        self.assertEqual(orderbook_allocated["rigid"][2]["Allocated Qty"], 100)
        self.assertEqual(orderbook_allocated["rigid"][3]["SKU"], "SKU5")
        self.assertEqual(orderbook_allocated["rigid"][3]["Allocated Qty"], 50)
        self.assertEqual(orderbook_allocated["rigid"][4]["SKU"], "SKU6")
        self.assertEqual(orderbook_allocated["rigid"][4]["Allocated Qty"], 200)
        # Inventory left after allocation match expected qty
        self.assertEqual(inventory_left["SKU1"], 0)
        self.assertEqual(inventory_left["SKU2"], 10)
        self.assertEqual(inventory_left["SKU3"], 0)
        self.assertEqual(inventory_left["SKU4"], 0)
        self.assertEqual(inventory_left["SKU5"], 0)
        self.assertEqual(inventory_left["SKU6"], 1200)
        # Orderbook not allocated contain correct order(s)
        self.assertEqual(orderbook_not_allocated["trailer"][0]["SKU"], "SKU1")
        self.assertEqual(orderbook_not_allocated["trailer"][0]["Qty"], 900)
        self.assertEqual(orderbook_not_allocated["trailer"][1]["SKU"], "SKU4")
        self.assertEqual(orderbook_not_allocated["trailer"][1]["Qty"], 50)
        self.assertEqual(orderbook_not_allocated["rigid"][0]["SKU"], "SKU3")
        self.assertEqual(orderbook_not_allocated["rigid"][0]["Qty"], 30)
        self.assertEqual(orderbook_not_allocated["rigid"][1]["SKU"], "SKU5")
        self.assertEqual(orderbook_not_allocated["rigid"][1]["Qty"], 50)

    def test_inventory_allocation_empty_dataset(self):
        """
        Test for empty dataset.
        """
        print("test Inventory Allocation empty dataset")

        # Both, orderbook and inventory are empty
        orderbook, inventory = dict(), dict()
        allocator = InventoryAllocation(orderbook, inventory)
        if orderbook == {} or inventory == {}:
            with self.assertRaises(EmptyDatasetError) as context:
                allocator.allocate_inventory()
            self.assertEqual(
                str(context.exception), "Orderbook and inventory must not be empty"
            )

        # Orderbook is empty, but inventory has some data
        orderbook, inventory = dict(), {"SKU1": 100}
        allocator = InventoryAllocation(orderbook, inventory)

        if orderbook == {} or inventory == {}:
            with self.assertRaises(EmptyDatasetError) as context:
                allocator.allocate_inventory()
            self.assertEqual(
                str(context.exception), "Orderbook and inventory must not be empty"
            )

        # Inventory is empty, but orderbook has some data
        inventory = {}
        orderbook = {
            "trailer": [
                {
                    "Customer Name": "ABC",
                    "Customer Postcode": "ABC123",
                    "SKU": "SKU1",
                    "Qty": 1000,
                    "Due Date": 2023 - 11 - 10,
                },
            ]
        }
        allocator = InventoryAllocation(orderbook, inventory)
        if orderbook == {} or inventory == {}:
            with self.assertRaises(EmptyDatasetError) as context:
                allocator.allocate_inventory()
            self.assertEqual(
                str(context.exception), "Orderbook and inventory must not be empty"
            )

    def test_inventory_allocation_correct_keys(self):
        """
        Test for correct keys in orderbook dictionary.
        Raises appropriate error if not.
        """

        print("test Inventory Allocation correct keys")

        # Define correct keys
        orderbook_correct_keys = [
            "Customer Name",
            "Customer Postcode",
            "SKU",
            "Qty",
            "Due Date",
            "Transport Volume (m3)",
        ]

        inventory_correct_keys = ["SKU", "Qty"]

        # Create orderbook sample with wrong key to test if correct Error message is raised with wrong columns in orderbook
        orderbook_sample_1 = {
            "trailer": [
                {
                    "Customer Name": "ABC",
                    "Customer Postcode": "ABC123",
                    "ABC": "SKU1",
                    "Qty": 1000,
                    "Due Date": 2023 - 11 - 10,
                    "Transport Volume (m3)": 1000,
                }
            ]
        }
        # Create orderbook sample with all correct keys
        orderbook_sample_2 = {
            "rigid": [
                {
                    "Customer Name": "XYZ",
                    "Customer Postcode": "XYZ123",
                    "SKU": "SKU2",
                    "Qty": 30,
                    "Due Date": 2023 - 11 - 10,
                    "Transport Volume (m3)": 30,
                },
            ]
        }
        # Create orderbook sample with wrong top level key
        orderbook_sample_3 = {
            "trailer": [
                {
                    "Customer Name": "ABC",
                    "Customer Postcode": "ABC123",
                    "ABC": "SKU1",
                    "Qty": 1000,
                    "Due Date": 2023 - 11 - 10,
                    "Transport Volume (m3)": 1000,
                }
            ],
            "delivery_van": [
                {
                    "Customer Name": "ABC",
                    "Customer Postcode": "ABC123",
                    "ABC": "SKU1",
                    "Qty": 1000,
                    "Due Date": 2023 - 11 - 10,
                    "Transport Volume (m3)": 1000,
                }
            ],
        }

        # Create inventory samples with all correct keys
        inventory_sample_1 = {"SKU1": 100, "SKU2": 100}
        inventory_sample_2 = {"ABC": 100, "SKU2": 100}
        inventory_sample_3 = {"SKU1": 100, "SKU2": 100}

        # Create InventoryAllocation objects - allocator_1 has got wrong key in orderbook and correct keys in inventory AND allocator_2 has got wrong key in inventory and all correct keys in orderbook
        allocator_1 = InventoryAllocation(orderbook_sample_1, inventory_sample_1)
        allocator_2 = InventoryAllocation(orderbook_sample_2, inventory_sample_2)
        allocator_3 = InventoryAllocation(orderbook_sample_3, inventory_sample_3)

        # Error message used in WrongKeysAllocatorError
        error_message = "Function allocate_inventory takes two dictionaries: orderbook and inventory.\nOrderbook must be outcome from parse_orderbook method called on OrderbookParser object.\nInventory must be outcome from parse_inventory method called on InventoryParser object.\nIf they are not, they may not have correct keys.\n"

        # Test case for orderbook_sampel_1 should raise the error
        for vehicle in orderbook_sample_1:
            if vehicle not in ["trailer", "rigid", "ERROR"]:
                with self.assertRaises(WrongKeysAllocatorError) as context:
                    allocator_1.allocate_inventory()
                self.assertEqual(str(context.exception), error_message)
            for entry in orderbook_sample_1[vehicle]:
                for sub_key in entry:
                    if sub_key not in orderbook_correct_keys:
                        with self.assertRaises(WrongKeysAllocatorError) as context:
                            allocator_1.allocate_inventory()
                        self.assertEqual(str(context.exception), error_message)

        # Test case for orderbook_sample_2 should process correctly and all outcomes should pass
        orderbook_allocated, inventory_left, orderbook_not_allocated = (
            allocator_2.allocate_inventory()
        )

        self.assertEqual(orderbook_allocated["rigid"][0]["SKU"], "SKU2")
        self.assertEqual(orderbook_allocated["rigid"][0]["Qty"], 30)
        self.assertEqual(inventory_left["SKU2"], 70)
        self.assertEqual(inventory_left["ABC"], 100)
        self.assertDictEqual(
            orderbook_not_allocated, {"trailer": [], "rigid": [], "error": []}
        )

        # Test case for orderbook_sample_3 should raise error due to top level wrong key
        for vehicle in orderbook_sample_3:
            if vehicle not in ["trailer", "rigid", "ERROR"]:
                with self.assertRaises(WrongKeysAllocatorError) as context:
                    allocator_3.allocate_inventory()
                self.assertEqual(str(context.exception), error_message)
            for entry in orderbook_sample_3[vehicle]:
                for sub_key in entry:
                    if sub_key not in orderbook_correct_keys:
                        with self.assertRaises(WrongKeysAllocatorError) as context:
                            allocator_3.allocate_inventory()
                        self.assertEqual(str(context.exception), error_message)

    def test_inventory_allocation_simple_group(self):
        """
        Simple test to check if method simple_group in the class InvcentoryAllocation
        group orders by customer with common name, postcode, vehicle type, adding total
        transport volume and list of line details, such as sku, qty, transport volume
        of the line and due date.
        Expected outcome is dict datatype with this structure:
        {
        'Vehicle Type':
            [
                {
                'Customer Name',
                'Customer Postcode',
                'Total Volume',
                'Line Details':
                    [
                        {
                        'SKU',
                        'Qty',
                        'Transport Volume',
                        'Due Date'
                        },
                        {
                        ...
                        }
                    ],
                },
            ]
        }
        """

        # Create orderbook sample with same customer but two orders
        orderbook = {
            "trailer": [
                {
                    "Customer Name": "ABC",
                    "Customer Postcode": "ABC123",
                    "SKU": "SKU1",
                    "Qty": 60,
                    "Due Date": 2023 - 11 - 10,
                    "Transport Volume (m3)": 1,
                },
                {
                    "Customer Name": "ABC",
                    "Customer Postcode": "ABC123",
                    "SKU": "SKU2",
                    "Qty": 10,
                    "Due Date": 2023 - 11 - 11,
                    "Transport Volume (m3)": 2,
                },
            ]
        }

        # Create inventory sample with just two skus
        inventory = {
            "SKU1": 100,
            "SKU2": 100,
        }

        # Create allocator as object of InventoryAllocation class and run allocate_inventory method on the created object
        allocator = InventoryAllocation(orderbook, inventory)
        orderbook_allocated, inventory_left, orderbook_not_allocated = (
            allocator.allocate_inventory()
        )
        # Create a new dict with orderbook grouped by customer
        grouped_orderbook_allocated = allocator.group_by_customer(orderbook_allocated)

        # Verify the outcome of allocate_inventory method
        self.assertEqual(orderbook_allocated["trailer"][0]["Allocated Qty"], 60)
        self.assertEqual(inventory_left["SKU1"], 40)
        self.assertEqual(orderbook_not_allocated["trailer"], [])

        # # Verify the outcome of group_by_customer method
        self.assertEqual(
            len(grouped_orderbook_allocated["trailer"][0]["Line Details"]), 2
        )
        self.assertEqual(len(grouped_orderbook_allocated["trailer"]), 1)
        self.assertEqual(
            grouped_orderbook_allocated["trailer"][0]["Customer Name"], "ABC"
        )
        self.assertEqual(
            grouped_orderbook_allocated["trailer"][0]["Customer Postcode"], "ABC123"
        )
        self.assertEqual(grouped_orderbook_allocated["trailer"][0]["Total Volume"], 3)
        self.assertEqual(
            grouped_orderbook_allocated["trailer"][0]["Line Details"][0],
            {
                "SKU": "SKU1",
                "Qty": 60,
                "Due Date": 2023 - 11 - 10,
                "Allocated Volume": 1,
            },
        )
        self.assertEqual(
            grouped_orderbook_allocated["trailer"][0]["Line Details"][1],
            {
                "SKU": "SKU2",
                "Qty": 10,
                "Due Date": 2023 - 11 - 11,
                "Allocated Volume": 2,
            },
        )

    def test_inventory_allocation_group_two_customers_same_vehicle_enough_inventory(
        self,
    ):
        """
        Testing for inventory allocation and grouping by customer with two different customers with same vehicle type and enough inventory to cover all orders

        """

        # Create orderbook sample with same customer but two orders
        orderbook = {
            "trailer": [
                {
                    "Customer Name": "ABC",
                    "Customer Postcode": "ABC123",
                    "SKU": "SKU1",
                    "Qty": 60,
                    "Due Date": 2023 - 11 - 10,
                    "Transport Volume (m3)": 1,
                },
                {
                    "Customer Name": "ABC",
                    "Customer Postcode": "ABC123",
                    "SKU": "SKU2",
                    "Qty": 10,
                    "Due Date": 2023 - 11 - 11,
                    "Transport Volume (m3)": 2,
                },
                {
                    "Customer Name": "XYZ",
                    "Customer Postcode": "XYZ123",
                    "SKU": "SKU1",
                    "Qty": 60,
                    "Due Date": 2023 - 11 - 10,
                    "Transport Volume (m3)": 1,
                },
                {
                    "Customer Name": "XYZ",
                    "Customer Postcode": "XYZ123",
                    "SKU": "SKU2",
                    "Qty": 10,
                    "Due Date": 2023 - 11 - 11,
                    "Transport Volume (m3)": 2,
                },
            ]
        }

        # Create inventory sample with just two skus
        inventory = {
            "SKU1": 200,
            "SKU2": 200,
        }

        # Create allocator as object of InventoryAllocation class and run allocate_inventory method on the created object
        allocator = InventoryAllocation(orderbook, inventory)
        orderbook_allocated, inventory_left, orderbook_not_allocated = (
            allocator.allocate_inventory()
        )
        # Create a new dict with orderbook grouped by customer
        grouped_orderbook_allocated = allocator.group_by_customer(orderbook_allocated)

        # Verify the outcome of allocate_inventory method
        self.assertEqual(orderbook_allocated["trailer"][0]["Allocated Qty"], 60)
        self.assertEqual(inventory_left["SKU1"], 80)
        self.assertEqual(orderbook_not_allocated["trailer"], [])

        # # Verify the outcome of group_by_customer method
        self.assertEqual(
            len(grouped_orderbook_allocated["trailer"][0]["Line Details"]), 2
        )
        self.assertEqual(len(grouped_orderbook_allocated["trailer"]), 2)
        self.assertEqual(
            grouped_orderbook_allocated["trailer"][0]["Customer Name"], "ABC"
        )
        self.assertEqual(
            grouped_orderbook_allocated["trailer"][0]["Customer Postcode"], "ABC123"
        )
        self.assertEqual(grouped_orderbook_allocated["trailer"][0]["Total Volume"], 3)
        self.assertEqual(
            grouped_orderbook_allocated["trailer"][1]["Customer Name"], "XYZ"
        )
        self.assertEqual(
            grouped_orderbook_allocated["trailer"][1]["Customer Postcode"], "XYZ123"
        )
        self.assertEqual(grouped_orderbook_allocated["trailer"][1]["Total Volume"], 3)
        self.assertEqual(
            grouped_orderbook_allocated["trailer"][0]["Line Details"][0],
            {
                "SKU": "SKU1",
                "Qty": 60,
                "Due Date": 2023 - 11 - 10,
                "Allocated Volume": 1,
            },
        )
        self.assertEqual(
            grouped_orderbook_allocated["trailer"][0]["Line Details"][1],
            {
                "SKU": "SKU2",
                "Qty": 10,
                "Due Date": 2023 - 11 - 11,
                "Allocated Volume": 2,
            },
        )
        self.assertEqual(
            grouped_orderbook_allocated["trailer"][1]["Line Details"][0],
            {
                "SKU": "SKU1",
                "Qty": 60,
                "Due Date": 2023 - 11 - 10,
                "Allocated Volume": 1,
            },
        )
        self.assertEqual(
            grouped_orderbook_allocated["trailer"][1]["Line Details"][1],
            {
                "SKU": "SKU2",
                "Qty": 10,
                "Due Date": 2023 - 11 - 11,
                "Allocated Volume": 2,
            },
        )

    def test_inventory_allocation_group_three_customers_different_vehicle_not_enough_inventory(
        self,
    ):
        """
        Testing for inventory allocation and grouping by customer with three different customers with different vehicle type and not enough inventory to cover all orders

        """

        # Create orderbook sample with same customer but two orders
        orderbook = {
            "trailer": [
                {
                    "Customer Name": "ABC",
                    "Customer Postcode": "ABC123",
                    "SKU": "SKU1",
                    "Qty": 60,
                    "Due Date": 2023 - 11 - 10,
                    "Transport Volume (m3)": 1,
                },
                {
                    "Customer Name": "ABC",
                    "Customer Postcode": "ABC123",
                    "SKU": "SKU2",
                    "Qty": 10,
                    "Due Date": 2023 - 11 - 11,
                    "Transport Volume (m3)": 2,
                },
                {
                    "Customer Name": "XYZ",
                    "Customer Postcode": "XYZ123",
                    "SKU": "SKU1",
                    "Qty": 60,
                    "Due Date": 2023 - 11 - 10,
                    "Transport Volume (m3)": 1,
                },
                {
                    "Customer Name": "XYZ",
                    "Customer Postcode": "XYZ123",
                    "SKU": "SKU2",
                    "Qty": 10,
                    "Due Date": 2023 - 11 - 11,
                    "Transport Volume (m3)": 2,
                },
            ],
            "rigid": [
                {
                    "Customer Name": "IJK",
                    "Customer Postcode": "IJK123",
                    "SKU": "SKU1",
                    "Qty": 100,
                    "Due Date": 2023 - 11 - 10,
                    "Transport Volume (m3)": 50,
                },
                {
                    "Customer Name": "IJK",
                    "Customer Postcode": "IJK123",
                    "SKU": "SKU2",
                    "Qty": 10,
                    "Due Date": 2023 - 11 - 11,
                    "Transport Volume (m3)": 2,
                },
            ],
        }

        # Create inventory sample with just two skus
        inventory = {
            "SKU1": 200,
            "SKU2": 200,
        }

        # Create allocator as object of InventoryAllocation class and run allocate_inventory method on the created object
        allocator = InventoryAllocation(orderbook, inventory)
        orderbook_allocated, inventory_left, orderbook_not_allocated = (
            allocator.allocate_inventory()
        )
        # Create a new dict with orderbook grouped by customer
        grouped_orderbook_allocated = allocator.group_by_customer(orderbook_allocated)

        # Verify the outcome of allocate_inventory method
        self.assertEqual(orderbook_allocated["trailer"][0]["Allocated Qty"], 60)
        self.assertEqual(orderbook_allocated["trailer"][0]["Allocated Volume"], 1)
        self.assertEqual(orderbook_allocated["trailer"][1]["Allocated Qty"], 10)
        self.assertEqual(orderbook_allocated["trailer"][1]["Allocated Volume"], 2)
        self.assertEqual(orderbook_allocated["rigid"][0]["Allocated Qty"], 80)
        self.assertEqual(orderbook_allocated["rigid"][0]["Allocated Volume"], 40)
        self.assertEqual(inventory_left["SKU1"], 0)
        self.assertEqual(orderbook_not_allocated["trailer"], [])

        # # Verify the outcome of group_by_customer method
        self.assertEqual(
            len(grouped_orderbook_allocated["trailer"][0]["Line Details"]), 2
        )
        self.assertEqual(
            len(grouped_orderbook_allocated["trailer"][1]["Line Details"]), 2
        )
        self.assertEqual(
            len(grouped_orderbook_allocated["rigid"][0]["Line Details"]), 2
        )
        self.assertEqual(len(grouped_orderbook_allocated["trailer"]), 2)
        self.assertEqual(len(grouped_orderbook_allocated["rigid"]), 1)
        self.assertEqual(
            grouped_orderbook_allocated["trailer"][0]["Customer Name"], "ABC"
        )
        self.assertEqual(
            grouped_orderbook_allocated["trailer"][0]["Customer Postcode"], "ABC123"
        )
        self.assertEqual(grouped_orderbook_allocated["trailer"][0]["Total Volume"], 3)
        self.assertEqual(
            grouped_orderbook_allocated["trailer"][1]["Customer Name"], "XYZ"
        )
        self.assertEqual(
            grouped_orderbook_allocated["trailer"][1]["Customer Postcode"], "XYZ123"
        )
        self.assertEqual(grouped_orderbook_allocated["trailer"][1]["Total Volume"], 3)
        self.assertEqual(
            grouped_orderbook_allocated["rigid"][0]["Customer Name"], "IJK"
        )
        self.assertEqual(
            grouped_orderbook_allocated["rigid"][0]["Customer Postcode"], "IJK123"
        )
        self.assertEqual(grouped_orderbook_allocated["rigid"][0]["Total Volume"], 42)
        self.assertEqual(
            grouped_orderbook_allocated["trailer"][0]["Line Details"][0],
            {
                "SKU": "SKU1",
                "Qty": 60,
                "Due Date": 2023 - 11 - 10,
                "Allocated Volume": 1,
            },
        )
        self.assertEqual(
            grouped_orderbook_allocated["trailer"][0]["Line Details"][1],
            {
                "SKU": "SKU2",
                "Qty": 10,
                "Due Date": 2023 - 11 - 11,
                "Allocated Volume": 2,
            },
        )
        self.assertEqual(
            grouped_orderbook_allocated["trailer"][0]["Line Details"],
            [
                {
                    "SKU": "SKU1",
                    "Qty": 60,
                    "Due Date": 2023 - 11 - 10,
                    "Allocated Volume": 1,
                },
                {
                    "SKU": "SKU2",
                    "Qty": 10,
                    "Due Date": 2023 - 11 - 11,
                    "Allocated Volume": 2,
                },
            ],
        )
        self.assertEqual(
            grouped_orderbook_allocated["trailer"][1]["Line Details"][0],
            {
                "SKU": "SKU1",
                "Qty": 60,
                "Due Date": 2023 - 11 - 10,
                "Allocated Volume": 1,
            },
        )
        self.assertEqual(
            grouped_orderbook_allocated["trailer"][1]["Line Details"][1],
            {
                "SKU": "SKU2",
                "Qty": 10,
                "Due Date": 2023 - 11 - 11,
                "Allocated Volume": 2,
            },
        )
        self.assertEqual(
            grouped_orderbook_allocated["trailer"][0]["Line Details"],
            [
                {
                    "SKU": "SKU1",
                    "Qty": 60,
                    "Due Date": 2023 - 11 - 10,
                    "Allocated Volume": 1,
                },
                {
                    "SKU": "SKU2",
                    "Qty": 10,
                    "Due Date": 2023 - 11 - 11,
                    "Allocated Volume": 2,
                },
            ],
        )
        self.assertEqual(
            grouped_orderbook_allocated["rigid"][0]["Line Details"][0],
            {
                "SKU": "SKU1",
                "Qty": 80,
                "Due Date": 2023 - 11 - 10,
                "Allocated Volume": 40,
            },
        )
        self.assertEqual(
            grouped_orderbook_allocated["rigid"][0]["Line Details"][1],
            {
                "SKU": "SKU2",
                "Qty": 10,
                "Due Date": 2023 - 11 - 11,
                "Allocated Volume": 2,
            },
        )
        self.assertEqual(
            grouped_orderbook_allocated["rigid"][0]["Line Details"],
            [
                {
                    "SKU": "SKU1",
                    "Qty": 80,
                    "Due Date": 2023 - 11 - 10,
                    "Allocated Volume": 40,
                },
                {
                    "SKU": "SKU2",
                    "Qty": 10,
                    "Due Date": 2023 - 11 - 11,
                    "Allocated Volume": 2,
                },
            ],
        )

    def test_split_orderbook_by_volume_simple(self):
        """
        This tests methoc split_orderbook_by_volume which splits orderbook to 5 orderbooks:
        1. full_loads_trailers and full_loads_rigids- orders which are just about a full vehicle
        2. parcels - orders which too small
        3. multidrop_orders_trailers and multidrop_orders_rigids - orders which are between the first two
        """

        orderbook = {
            "trailer": [
                {
                    # Customer for full_load
                    "Customer Name": "ABC",
                    "Customer Postcode": "ABC123",
                    "Total Volume": 52,
                    "Line Details": [
                        {
                            "SKU": "SKU1",
                            "Qty": 50,
                            "Due Date": 2023 - 11 - 10,
                            "Allocated Volume": 50,
                        },
                        {
                            "SKU": "SKU1",
                            "Qty": 2,
                            "Due Date": 2023 - 11 - 10,
                            "Allocated Volume": 2,
                        },
                    ],
                },
                {
                    # Customer for parcel
                    "Customer Name": "XYZ",
                    "Customer Postcode": "XYZ123",
                    "Total Volume": 1,
                    "Line Details": [
                        {
                            "SKU": "SKU1",
                            "Qty": 1,
                            "Due Date": 2023 - 11 - 10,
                            "Allocated Volume": 0.5,
                        },
                        {
                            "SKU": "SKU1",
                            "Qty": 1,
                            "Due Date": 2023 - 11 - 10,
                            "Allocated Volume": 0.5,
                        },
                    ],
                },
                {
                    # Customer for multidrop
                    "Customer Name": "DEF",
                    "Customer Postcode": "DEF123",
                    "Total Volume": 30,
                    "Line Details": [
                        {
                            "SKU": "SKU1",
                            "Qty": 15,
                            "Due Date": 2023 - 11 - 10,
                            "Allocated Volume": 15,
                        },
                        {
                            "SKU": "SKU1",
                            "Qty": 15,
                            "Due Date": 2023 - 11 - 10,
                            "Allocated Volume": 15,
                        },
                    ],
                },
            ]
        }

        allocator = InventoryAllocation.__new__(InventoryAllocation)
        (
            full_loads_trailers,
            full_loads_rigids,
            parcels,
            multidrop_loads_trailers,
            multidrop_loads_rigids,
        ) = allocator.split_by_volume(
            orderbook, TRAILER_MAX, TRAILER_MIN, RIGID_MAX, RIGID_MIN, PARCEL_LIMIT
        )

        self.assertEqual(len(full_loads_trailers), 1)
        self.assertEqual(len(full_loads_rigids), 0)
        self.assertEqual(len(parcels), 1)
        self.assertEqual(len(multidrop_loads_trailers), 1)
        self.assertEqual(len(multidrop_loads_rigids), 0)
        self.assertEqual(full_loads_trailers[0]["Customer Name"], "ABC")
        self.assertEqual(parcels[0]["Customer Name"], "XYZ")
        self.assertEqual(multidrop_loads_trailers[0]["Customer Name"], "DEF")
        self.assertEqual(len(full_loads_trailers[0]["Line Details"]), 2)
        self.assertEqual(len(parcels[0]["Line Details"]), 2)
        self.assertEqual(len(multidrop_loads_trailers[0]["Line Details"]), 2)


    def test_split_orderbook_by_volume_too_large_order(self):
        """
        This tests methoc split_orderbook_by_volume for the case if order it bigger than full load - scenario 1 - order is for 1, 2, 3 full loads, but orders does not need breaking down.
        """

        orderbook = {
            "trailer": [
                {
                    # Customer for full_load
                    "Customer Name": "ABC",
                    "Customer Postcode": "ABC123",
                    "Total Volume": 52,
                    "Line Details": [
                        {
                            "SKU": "SKU1",
                            "Qty": 50,
                            "Due Date": 2023 - 11 - 10,
                            "Allocated Volume": 50,
                        },
                        {
                            "SKU": "SKU1",
                            "Qty": 2,
                            "Due Date": 2023 - 11 - 10,
                            "Allocated Volume": 2,
                        },
                    ],
                },
                {
                    # Customer for 2 full loads
                    "Customer Name": "XYZ",
                    "Customer Postcode": "XYZ123",
                    "Total Volume": 104,
                    "Line Details": [
                        {
                            "SKU": "SKU1",
                            "Qty": 10,
                            "Due Date": 2023 - 11 - 10,
                            "Allocated Volume": 52,
                        },
                        {
                            "SKU": "SKU1",
                            "Qty": 10,
                            "Due Date": 2023 - 11 - 10,
                            "Allocated Volume": 52,
                        },
                    ],
                },
                {
                    # Customer for 3 full loads
                    "Customer Name": "DEF",
                    "Customer Postcode": "DEF123",
                    "Total Volume": 156,
                    "Line Details": [
                        {
                            "SKU": "SKU1",
                            "Qty": 10,
                            "Due Date": 2023 - 11 - 10,
                            "Allocated Volume": 52,
                        },
                        {
                            "SKU": "SKU1",
                            "Qty": 10,
                            "Due Date": 2023 - 11 - 10,
                            "Allocated Volume": 52,
                        },
                        {
                            "SKU": "SKU1",
                            "Qty": 10,
                            "Due Date": 2023 - 11 - 10,
                            "Allocated Volume": 52,
                        },                        
                    ],
                },
            ]
        }

        allocator = InventoryAllocation.__new__(InventoryAllocation)
        (
            full_loads_trailers,
            full_loads_rigids,
            parcels,
            multidrop_loads_trailers,
            multidrop_loads_rigids,
        ) = allocator.split_by_volume(
            orderbook, TRAILER_MAX, TRAILER_MIN, RIGID_MAX, RIGID_MIN, PARCEL_LIMIT
        )

        self.assertEqual(len(full_loads_trailers), 6)
        self.assertEqual(len(full_loads_rigids), 0)
        self.assertEqual(len(parcels), 0)
        self.assertEqual(len(multidrop_loads_trailers), 0)
        self.assertEqual(len(multidrop_loads_rigids), 0)

        self.assertEqual(full_loads_trailers[0]["Customer Name"], "ABC")
        self.assertEqual(full_loads_trailers[0]["Customer Postcode"], "ABC123")
        self.assertEqual(full_loads_trailers[0]["Total Volume"], 52)
        self.assertEqual(len(full_loads_trailers[0]["Line Details"]), 2)
        self.assertEqual(full_loads_trailers[0]["Line Details"], [
            {"SKU": "SKU1", "Qty": 50, "Due Date": 2023 - 11 - 10, "Allocated Volume": 50},
            {"SKU": "SKU1", "Qty": 2, "Due Date": 2023 - 11 - 10, "Allocated Volume": 2}
            ])

        self.assertEqual(full_loads_trailers[1]["Customer Name"], "XYZ")
        self.assertEqual(full_loads_trailers[1]["Customer Postcode"], "XYZ123")
        self.assertEqual(full_loads_trailers[1]["Total Volume"], 52)
        self.assertEqual(len(full_loads_trailers[1]["Line Details"]), 1)
        self.assertEqual(full_loads_trailers[1]["Line Details"], [
            {"SKU": "SKU1", "Qty": 10, "Due Date": 2023 - 11 - 10, "Allocated Volume": 52}
            ])

        self.assertEqual(full_loads_trailers[2]["Customer Name"], "XYZ")
        self.assertEqual(full_loads_trailers[2]["Customer Postcode"], "XYZ123")
        self.assertEqual(full_loads_trailers[2]["Total Volume"], 52)
        self.assertEqual(len(full_loads_trailers[2]["Line Details"]), 1)
        self.assertEqual(full_loads_trailers[2]["Line Details"], [
            {"SKU": "SKU1", "Qty": 10, "Due Date": 2023 - 11 - 10, "Allocated Volume": 52}
            ])

        self.assertEqual(full_loads_trailers[3]["Customer Name"], "DEF")
        self.assertEqual(full_loads_trailers[3]["Customer Postcode"], "DEF123")
        self.assertEqual(full_loads_trailers[3]["Total Volume"], 52)
        self.assertEqual(len(full_loads_trailers[3]["Line Details"]), 1)
        self.assertEqual(full_loads_trailers[3]["Line Details"], [
            {"SKU": "SKU1", "Qty": 10, "Due Date": 2023 - 11 - 10, "Allocated Volume": 52}
            ])
        
        self.assertEqual(full_loads_trailers[4]["Customer Name"], "DEF")
        self.assertEqual(full_loads_trailers[4]["Customer Postcode"], "DEF123")
        self.assertEqual(full_loads_trailers[4]["Total Volume"], 52)
        self.assertEqual(len(full_loads_trailers[4]["Line Details"]), 1)
        self.assertEqual(full_loads_trailers[4]["Line Details"], [
            {"SKU": "SKU1", "Qty": 10, "Due Date": 2023 - 11 - 10, "Allocated Volume": 52}
            ])    

        self.assertEqual(full_loads_trailers[5]["Customer Name"], "DEF")
        self.assertEqual(full_loads_trailers[5]["Customer Postcode"], "DEF123")
        self.assertEqual(full_loads_trailers[5]["Total Volume"], 52)
        self.assertEqual(len(full_loads_trailers[5]["Line Details"]), 1)
        self.assertEqual(full_loads_trailers[5]["Line Details"], [
            {"SKU": "SKU1", "Qty": 10, "Due Date": 2023 - 11 - 10, "Allocated Volume": 52}
            ])

    def test_split_orderbook_by_volume_too_large_order_breaking_down_order(self):
        """
        This tests methoc split_orderbook_by_volume for the case if order it bigger than full load - scenario 2 - order is for more then 1 full load, 
        but order does need breaking down and splitting same product for more loads.
        """
        
        orderbook = {
            "trailer": [
                {
                    # 1st product needs split, partially to 1 load and partially, together with 2nd product to 2nd load
                    "Customer Name": "ABC",
                    "Customer Postcode": "ABC123",
                    "Total Volume": 105,
                    "Line Details": [
                        {
                            "SKU": "SKU1",
                            "Qty": 80,
                            "Due Date": 2023 - 11 - 10,
                            "Allocated Volume": 80,
                        },
                        {
                            "SKU": "SKU2",
                            "Qty": 25,
                            "Due Date": 2023 - 11 - 10,
                            "Allocated Volume": 25,
                        },
                    ],
                },
             ]
        }

        allocator = InventoryAllocation.__new__(InventoryAllocation)
        (
            full_loads_trailers,
            full_loads_rigids,
            parcels,
            multidrop_loads_trailers,
            multidrop_loads_rigids,
        ) = allocator.split_by_volume(
            orderbook, TRAILER_MAX, TRAILER_MIN, RIGID_MAX, RIGID_MIN, PARCEL_LIMIT
        )

        self.assertEqual(len(full_loads_trailers), 2)
        self.assertEqual(len(full_loads_rigids), 0)
        self.assertEqual(len(parcels), 0)
        self.assertEqual(len(multidrop_loads_trailers), 0)
        self.assertEqual(len(multidrop_loads_rigids), 0)

        self.assertEqual(full_loads_trailers[0]["Customer Name"], "ABC")
        self.assertEqual(full_loads_trailers[0]["Customer Postcode"], "ABC123")
        self.assertEqual(full_loads_trailers[0]["Total Volume"], 55)
        self.assertEqual(len(full_loads_trailers[0]["Line Details"]), 1)
        self.assertEqual(full_loads_trailers[0]["Line Details"], [
            {"SKU": "SKU1", "Qty": 55, "Due Date": 2023 - 11 - 10, "Allocated Volume": 55},
            ])

        self.assertEqual(full_loads_trailers[1]["Customer Name"], "ABC")
        self.assertEqual(full_loads_trailers[1]["Customer Postcode"], "ABC123")
        self.assertEqual(full_loads_trailers[1]["Total Volume"], 50)
        self.assertEqual(len(full_loads_trailers[1]["Line Details"]), 2)
        self.assertEqual(full_loads_trailers[1]["Line Details"], [
            {"SKU": "SKU1", "Qty": 25, "Due Date": 2023 - 11 - 10, "Allocated Volume": 25},
            {"SKU": "SKU2", "Qty": 25, "Due Date": 2023 - 11 - 10, "Allocated Volume": 25}
            ])

    def test_split_orderbook_by_volume_simple_check_for_too_large_order_with_reminder(self):
        """
        This tests methoc split_orderbook_by_volume for the case if order it bigger than full load - scenario 3 - order is for more then 1 full load, 
        but order does need breaking down and splitting same product for more loads with reminder which needs adding to multidrop list.
        """
        
        orderbook = {
            "trailer": [
                {
                    # 1st product needs split, partially to 1 load and partially, together with 2nd product to 2nd load
                    "Customer Name": "ABC",
                    "Customer Postcode": "ABC123",
                    "Total Volume": 130,
                    "Line Details": [
                        {
                            "SKU": "SKU1",
                            "Qty": 80,
                            "Due Date": 2023 - 11 - 10,
                            "Allocated Volume": 80,
                        },
                        {
                            "SKU": "SKU2",
                            "Qty": 50,
                            "Due Date": 2023 - 11 - 10,
                            "Allocated Volume": 50,
                        },
                    ],
                },
             ]
        }

        allocator = InventoryAllocation.__new__(InventoryAllocation)
        (
            full_loads_trailers,
            full_loads_rigids,
            parcels,
            multidrop_loads_trailers,
            multidrop_loads_rigids,
        ) = allocator.split_by_volume(
            orderbook, TRAILER_MAX, TRAILER_MIN, RIGID_MAX, RIGID_MIN, PARCEL_LIMIT
        )

        self.assertEqual(len(full_loads_trailers), 2)
        self.assertEqual(len(full_loads_rigids), 0)
        self.assertEqual(len(parcels), 0)
        self.assertEqual(len(multidrop_loads_trailers), 1)
        self.assertEqual(len(multidrop_loads_rigids), 0)

        self.assertEqual(full_loads_trailers[0]["Customer Name"], "ABC")
        self.assertEqual(full_loads_trailers[0]["Customer Postcode"], "ABC123")
        self.assertEqual(full_loads_trailers[0]["Total Volume"], 55)
        self.assertEqual(len(full_loads_trailers[0]["Line Details"]), 1)
        self.assertEqual(full_loads_trailers[0]["Line Details"], [
            {"SKU": "SKU1", "Qty": 55, "Due Date": 2023 - 11 - 10, "Allocated Volume": 55},
            ])

        self.assertEqual(full_loads_trailers[1]["Customer Name"], "ABC")
        self.assertEqual(full_loads_trailers[1]["Customer Postcode"], "ABC123")
        self.assertEqual(full_loads_trailers[1]["Total Volume"], 55)
        self.assertEqual(len(full_loads_trailers[1]["Line Details"]), 2)
        self.assertEqual(full_loads_trailers[1]["Line Details"], [
            {"SKU": "SKU1", "Qty": 25, "Due Date": 2023 - 11 - 10, "Allocated Volume": 25},
            {"SKU": "SKU2", "Qty": 30, "Due Date": 2023 - 11 - 10, "Allocated Volume": 30}
            ])
        
        self.assertEqual(multidrop_loads_trailers[0]["Customer Name"], "ABC")
        self.assertEqual(multidrop_loads_trailers[0]["Customer Postcode"], "ABC123")
        self.assertEqual(multidrop_loads_trailers[0]["Total Volume"], 20)
        self.assertEqual(len(multidrop_loads_trailers[0]["Line Details"]), 1)
        self.assertEqual(multidrop_loads_trailers[0]["Line Details"], [
            {"SKU": "SKU2", "Qty": 20, "Due Date": 2023 - 11 - 10, "Allocated Volume": 20}
            ])

    def test_split_orderbook_by_volume_simple_check_for_too_large_order_with_reminder_for_parcel(self):
        """
        This tests methoc split_orderbook_by_volume for the case if order it bigger than full load - scenario 4 - order is for more then 1 full load, 
        but order does need breaking down and splitting same product for more loads with reminder which needs adding to parcels.
        """

        orderbook = {
            "trailer": [
                {
                    "Customer Name": "ABC",
                    "Customer Postcode": "ABC123",
                    "Total Volume": 130,
                    "Line Details": [
                        {
                            "SKU": "SKU1",
                            "Qty": 80,
                            "Due Date": 2023 - 11 - 10,
                            "Allocated Volume": 80,
                        },
                        {
                            "SKU": "SKU2",
                            "Qty": 31,
                            "Due Date": 2023 - 11 - 10,
                            "Allocated Volume": 31,
                        },
                    ],
                },
             ]
        }

        allocator = InventoryAllocation.__new__(InventoryAllocation)
        (
            full_loads_trailers,
            full_loads_rigids,
            parcels,
            multidrop_loads_trailers,
            multidrop_loads_rigids,
        ) = allocator.split_by_volume(
            orderbook, TRAILER_MAX, TRAILER_MIN, RIGID_MAX, RIGID_MIN, PARCEL_LIMIT
        )

        self.assertEqual(len(full_loads_trailers), 2)
        self.assertEqual(len(full_loads_rigids), 0)
        self.assertEqual(len(parcels), 1)
        self.assertEqual(len(multidrop_loads_trailers), 0)
        self.assertEqual(len(multidrop_loads_rigids), 0)

        self.assertEqual(full_loads_trailers[0]["Customer Name"], "ABC")
        self.assertEqual(full_loads_trailers[0]["Customer Postcode"], "ABC123")
        self.assertEqual(full_loads_trailers[0]["Total Volume"], 55)
        self.assertEqual(len(full_loads_trailers[0]["Line Details"]), 1)
        self.assertEqual(full_loads_trailers[0]["Line Details"], [
            {"SKU": "SKU1", "Qty": 55, "Due Date": 2023 - 11 - 10, "Allocated Volume": 55},
            ])

        self.assertEqual(full_loads_trailers[1]["Customer Name"], "ABC")
        self.assertEqual(full_loads_trailers[1]["Customer Postcode"], "ABC123")
        self.assertEqual(full_loads_trailers[1]["Total Volume"], 55)
        self.assertEqual(len(full_loads_trailers[1]["Line Details"]), 2)
        self.assertEqual(full_loads_trailers[1]["Line Details"], [
            {"SKU": "SKU1", "Qty": 25, "Due Date": 2023 - 11 - 10, "Allocated Volume": 25},
            {"SKU": "SKU2", "Qty": 30, "Due Date": 2023 - 11 - 10, "Allocated Volume": 30}
            ])
        
        self.assertEqual(parcels[0]["Customer Name"], "ABC")
        self.assertEqual(parcels[0]["Customer Postcode"], "ABC123")
        self.assertEqual(parcels[0]["Total Volume"], 1)
        self.assertEqual(len(parcels[0]["Line Details"]), 1)
        self.assertEqual(parcels[0]["Line Details"], [
            {"SKU": "SKU2", "Qty": 1, "Due Date": 2023 - 11 - 10, "Allocated Volume": 1}
            ])


    def test_split_orderbook_by_volume_complex(self):
        """
        This tests methoc split_orderbook_by_volume complex orderbook.
        """
        from tests.unit_tests.test_allocate_inventory.test_data.test_data_complex_split_orderbook import orderbook
        from tests.unit_tests.test_allocate_inventory.test_data.test_data_complex_split_result import full_loads_trailers_result, full_loads_rigids_result, parcels_result, multidrop_loads_trailers_result, multidrop_loads_rigids_result

        self.maxDiff = None

        allocator = InventoryAllocation.__new__(InventoryAllocation)
        (
            full_loads_trailers,
            full_loads_rigids,
            parcels,
            multidrop_loads_trailers,
            multidrop_loads_rigids,
        ) = allocator.split_by_volume(
            orderbook, TRAILER_MAX, TRAILER_MIN, RIGID_MAX, RIGID_MIN, PARCEL_LIMIT
        )

        for i, result in enumerate(full_loads_trailers_result):
            self.assertEqual(full_loads_trailers[i], result)

        for i, result in enumerate(full_loads_rigids_result):
            self.assertEqual(full_loads_rigids[i], result)

        for i, result in enumerate(parcels_result):
            self.assertEqual(parcels[i], result)
        
        for i, result in enumerate(multidrop_loads_trailers_result):
            self.assertEqual(multidrop_loads_trailers[i], result)
        
        for i, result in enumerate(multidrop_loads_rigids_result):
            self.assertEqual(multidrop_loads_rigids[i], result)





if __name__ == "__main__":
    unittest.main()
