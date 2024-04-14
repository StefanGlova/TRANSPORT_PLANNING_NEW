import unittest
from modules.allocate_inventory_module.inventory_allocation import InventoryAllocation


class TestInventoryAllocation(unittest.TestCase):
    """
    Test suit for Inventory Allocation
    """

    def test_inventory_allocation_simple_case(self):

        print("test Allocation simple case")

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

        inventory = {
            "SKU1": 100,
        }

        allocator = InventoryAllocation(orderbook, inventory)
        orderbook_allocated, inventory_left, orderbook_not_allocated = (
            allocator.allocate_inventory()
        )

        self.assertEqual(orderbook_allocated["trailer"][0]["Allocated Qty"], 60)
        self.assertEqual(inventory_left["SKU1"], 40)
        self.assertEqual(orderbook_not_allocated["trailer"], [])
