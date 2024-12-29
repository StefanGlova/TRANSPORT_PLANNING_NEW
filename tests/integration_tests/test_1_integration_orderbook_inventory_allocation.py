import unittest
from src.data_processing_module.process_inventory import ProcessInventory
from src.data_processing_module.process_orderbook import ProcessOrderbook
from src.allocate_inventory_module.inventory_allocation import InventoryAllocation
from src.errors import (
    EmptyFileError,
    WrongKeysError,
    WrongValueTypeError,
    WrongNumericRange,
    EmptyDatasetError,
    WrongKeysAllocatorError,
)

ORDERBOOK_PARSER = ProcessOrderbook(None)
INVENTORY_PARSER = ProcessInventory(None)

INVENTORY_CORRECT_KEYS = ["SKU", "Qty"]
ORDERBOOK_CORRECT_KEYS = [
    "Customer Name",
    "Customer Postcode",
    "SKU",
    "Qty",
    "Vehicle Type",
    "Due Date",
    "Transport Volume (m3)",
]


class TestIntegrationOrderbookInventoryAllocation(unittest.TestCase):

    def test_simple_integration(self):

        # Create inventory sample with just one sku
        inventory_test_data = [
            {
                "SKU": "SKU1",
                "Qty": "100",
            },
        ]

        # Create orderbook sample with just one order
        orderbook_test_data = [
            {
                "Customer Name": "ABC",
                "Customer Postcode": "ABC123",
                "SKU": "SKU1",
                "Qty": "60",
                "Vehicle Type": "trailer",
                "Due Date": "2024-04-10",
                "Transport Volume (m3)": "60",
            },
        ]

        # Initialize InventoryParser object
        INVENTORY_PARSER.parsed_data = inventory_test_data
        # Parse the inventory
        inventory = INVENTORY_PARSER.parse_inventory()
        # Initialize OrderParser object
        ORDERBOOK_PARSER.parsed_data = orderbook_test_data
        # Parse the orderbook
        orderbook = ORDERBOOK_PARSER.parse_orderbook()

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


if __name__ == "__main__":
    unittest.main()
