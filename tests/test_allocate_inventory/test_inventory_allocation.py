import unittest
from modules.allocate_inventory_module.inventory_allocation import InventoryAllocation


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

        # Create allocater as object of InventoryAllocation class and run allocate_inventory method on the created object
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

        # Create allocater as object of InventoryAllocation class and run allocate_inventory method on the created object
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

        # Create allocater as object of InventoryAllocation class and run allocate_inventory method on the created object
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


if __name__ == "__main__":
    unittest.main()
