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


if __name__ == "__main__":
    unittest.main()
