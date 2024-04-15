from modules.errors import EmptyDatasetError, WrongKeysAllocatorError


class InventoryAllocation:
    def __init__(self, orderbook: dict, inventory: dict):
        self.orderbook = orderbook
        self.inventory = inventory

    def allocate_inventory(self) -> dict:
        """
        Allocate inventory method creates 3 dictionaries which are used during method run and returned at the end:
            - orderbook_allocated - new orderbook variable used for further processing which only include orders with available and allocated inventory
            - orderbook_not_allocated - secondary orderbook, just for reference and further use which shows list of all orders which did not get inventory allocated, as available qty in orderbook was 0
            - inventory - same variable as input, but with updated values
        """
        # Initialize dict datastructures for the method output
        orderbook_allocated = dict()
        orderbook_not_allocated = {"trailer": [], "rigid": [], "error": []}

        # Check orderbook and inventory - both should not be empty, orderbook should have certain keys on both levels of dictionary
        self._check_orderbook()
        self._check_inventory()

        # Iterate though orderbook
        for vehicle, orders in self.orderbook.items():
            # Create vehicle list inside orderbook_allocated dict for each vehicle in orderbook
            orderbook_allocated[vehicle] = []
            # Iterate though orders
            for order in orders:
                # Try / except block check for case that SKU does not exist in inventory, but does exist in orderbook. In this case, it works with presumption that qty of that SKU is 0
                try:
                    # Call _allocate_qty private method which returns allocated_qty and unallocated_qty
                    allocated_qty, unallocated_qty = self._allocate_qty(order)
                    # If allocated_qty is more then 0, add key to order dict and append the order to orderbook_allocated
                    if allocated_qty > 0:
                        order["Allocated Qty"] = allocated_qty
                        orderbook_allocated[vehicle].append(order)
                    # If unallocated_qty is more then 0, update Qty on the order and append order to orderbook_not_allocated
                    if unallocated_qty > 0:
                        order["Qty"] = unallocated_qty
                        orderbook_not_allocated[vehicle].append(order)
                except KeyError:
                    self.inventory[order["SKU"]] = 0
                    orderbook_not_allocated[vehicle].append(order)

        return orderbook_allocated, self.inventory, orderbook_not_allocated

    def _allocate_qty(self, order: dict) -> int:
        """
        Private method to calculate allocated and unallocated qty for given order.

        Returns allocated_qty and unallocated_qty.
        """
        sku = order["SKU"]
        qty = order["Qty"]
        allocated_qty, unallocated_qty = 0, 0

        if self.inventory[sku] >= qty:
            allocated_qty = qty
            self.inventory[sku] -= qty
        elif self.inventory[sku] > 0:
            allocated_qty = self.inventory[sku]
            self.inventory[sku] = 0
            unallocated_qty = qty - allocated_qty
        else:
            allocated_qty = 0
            unallocated_qty = qty - allocated_qty

        return allocated_qty, unallocated_qty

    def _check_orderbook(self) -> None:
        """
        Private method to check if orderbook is not empty and if its not, whether keys in orderbook are correct.

        Raises appropriate error if not.
        """

        if self.orderbook == {}:
            raise EmptyDatasetError()

        high_level_keys = ["trailer", "rigid", "ERROR"]
        low_level_keys = [
            "Customer Name",
            "Customer Postcode",
            "SKU",
            "Qty",
            "Due Date",
        ]

        for vehicle in self.orderbook:
            if vehicle not in high_level_keys:
                raise WrongKeysAllocatorError()
            for order in self.orderbook[vehicle]:
                for order_detail in order:
                    if order_detail not in low_level_keys:
                        raise WrongKeysAllocatorError()

    def _check_inventory(self):
        """
        Private method to check if inventory is not empty.

        Raises appropriate error if not.
        """
        if self.inventory == {}:
            raise EmptyDatasetError()
