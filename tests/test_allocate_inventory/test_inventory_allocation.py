import unittest
from modules.allocate_inventory_module.inventory_allocation import InventoryAllocation

from modules.errors import EmptyDatasetError


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
        print("test Allocation simple case")

        # Create orderbook sample with just one order
        orderbook = {
            "trailer": [
                {
                    "Customer Name": "ABC",
                    "Customer Postcode": "ABC123",
                    "SKU": "SKU1",
                    "Qty": 60,
                    "Due Date": 2023 - 11 - 10,
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
        self.assertEqual(inventory_left["SKU1"], 40)
        self.assertEqual(orderbook_not_allocated["trailer"], [])

    def test_inventory_allocation_two_orders_case(self):
        """
        Similar to simple case, but 2 orders for same SKU and same vehicle type. Also 2nd different sku which is not used in any of orders.
        """
        print("test Allocation 2 orders case")

        # Create orderbook sample with just one order
        orderbook = {
            "trailer": [
                {
                    "Customer Name": "ABC",
                    "Customer Postcode": "ABC123",
                    "SKU": "SKU1",
                    "Qty": 60,
                    "Due Date": 2023 - 11 - 10,
                },
                {
                    "Customer Name": "XYZ",
                    "Customer Postcode": "XYZ123",
                    "SKU": "SKU1",
                    "Qty": 30,
                    "Due Date": 2023 - 11 - 10,
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
        self.assertEqual(inventory_left["SKU1"], 10)
        self.assertEqual(inventory_left["SKU2"], 100)
        self.assertEqual(orderbook_not_allocated["trailer"], [])

    def test_inventory_allocation_more_complex_case(self):
        """ """
        print("test Allocation more complex case")

        # Create orderbook sample with just one order
        orderbook = {
            "trailer": [
                {
                    "Customer Name": "ABC",
                    "Customer Postcode": "ABC123",
                    "SKU": "SKU1",
                    "Qty": 1000,
                    "Due Date": 2023 - 11 - 10,
                },
                {
                    "Customer Name": "XYZ",
                    "Customer Postcode": "XYZ123",
                    "SKU": "SKU2",
                    "Qty": 30,
                    "Due Date": 2023 - 11 - 10,
                },
                {
                    "Customer Name": "EFG",
                    "Customer Postcode": "XYZ123",
                    "SKU": "SKU6",
                    "Qty": 100,
                    "Due Date": 2023 - 11 - 10,
                },
                {
                    "Customer Name": "EFG",
                    "Customer Postcode": "XYZ123",
                    "SKU": "SKU4",
                    "Qty": 50,
                    "Due Date": 2023 - 11 - 10,
                },
                {
                    "Customer Name": "EFG",
                    "Customer Postcode": "XYZ123",
                    "SKU": "SKU6",
                    "Qty": 100,
                    "Due Date": 2023 - 11 - 10,
                },
                {
                    "Customer Name": "EFG",
                    "Customer Postcode": "XYZ123",
                    "SKU": "SKU5",
                    "Qty": 50,
                    "Due Date": 2023 - 11 - 10,
                },
                {
                    "Customer Name": "EFG",
                    "Customer Postcode": "XYZ123",
                    "SKU": "SKU6",
                    "Qty": 200,
                    "Due Date": 2023 - 11 - 10,
                },
            ],
            "rigid": [
                {
                    "Customer Name": "ABC",
                    "Customer Postcode": "ABC123",
                    "SKU": "SKU2",
                    "Qty": 60,
                    "Due Date": 2023 - 11 - 10,
                },
                {
                    "Customer Name": "EFG",
                    "Customer Postcode": "XYZ123",
                    "SKU": "SKU6",
                    "Qty": 100,
                    "Due Date": 2023 - 11 - 10,
                },
                {
                    "Customer Name": "XYZ",
                    "Customer Postcode": "XYZ123",
                    "SKU": "SKU3",
                    "Qty": 30,
                    "Due Date": 2023 - 11 - 10,
                },
                {
                    "Customer Name": "EFG",
                    "Customer Postcode": "XYZ123",
                    "SKU": "SKU6",
                    "Qty": 100,
                    "Due Date": 2023 - 11 - 10,
                },
                {
                    "Customer Name": "XYZ",
                    "Customer Postcode": "XYZ123",
                    "SKU": "SKU5",
                    "Qty": 100,
                    "Due Date": 2023 - 11 - 10,
                },
                {
                    "Customer Name": "EFG",
                    "Customer Postcode": "XYZ123",
                    "SKU": "SKU6",
                    "Qty": 200,
                    "Due Date": 2023 - 11 - 10,
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
        orderbook_correct_keys = [
            "Customer Name",
            "Customer Postcode",
            "SKU",
            "Qty",
            "Due Date",
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
                }
            ]
        }
        # Create orderbook sample with all correct keys to test if correct Error message is raised with wrong columns in inventory
        orderbook_sample_2 = {
            "rigid": [
                {
                    "Customer Name": "XYZ",
                    "Customer Postcode": "XYZ123",
                    "SKU": "SKU2",
                    "Qty": 30,
                    "Due Date": 2023 - 11 - 10,
                },
            ]
        }

        # Create inventory sample with all correct keys to test if correct Error message is raised with wrong columns in orderbook
        inventory_sample_1 = {"SKU1": 100, "SKU2": 100}
        # Create inventory sample with wrong key to test if correct Error message is raised with wrong columns in inventory
        inventory_sample_2 = {"ABC": 100, "SKU2": 100}

        # Create InventoryAllocation objects - allocator_1 has got wrong key in orderbook and correct keys in inventory AND allocator_2 has got wrong key in inventory and all correct keys in orderbook
        allocator_1 = InventoryAllocation(orderbook_sample_1, inventory_sample_1)
        allocator_2 = InventoryAllocation(orderbook_sample_2, inventory_sample_2)
        error_message = """
                Function allocate_inventory takes two dictionaries: orderbook and inventory. 
                Orderbook must be outcome from parse_orderbook method called on OrderbookParser object.
                Inventory must be outcome from parse_inventory method called on InventoryParser object.
                If they are not, they may not have correct keys.
                """

        for key in orderbook_sample_1:
            if key not in ["trailer", "rigid", "ERROR"]:
                with self.assertRaises(WrongKeysAllocatorError) as context:
                    allocator_1.allocate_inventory()
                self.assertEqual(str(context.exception), error_message)
            for sub_key in orderbook_sample_1[key]:
                if sub_key not in orderbook_correct_keys:
                    with self.assertRaises(WrongKeysAllocatorError) as context:
                        allocator_1.allocate_inventory()
                    self.assertEqual(str(context.exception), error_message)

        for key in inventory_sample_2:
            if key not in ["SKU", "Qty"]:
                with self.assertRaises(WrongKeysAllocatorError) as context:
                    allocator_1.allocate_inventory()
                self.assertEqual(str(context.exception), error_message)


if __name__ == "__main__":
    unittest.main()
