class InventoryAllocation:
    def __init__(self, orderbook, inventory):
        self.orderbook = orderbook
        self.inventory = inventory

    def allocate_inventory(self):
        """
        Allocate inventory method creates 3 dictionaries which are used during method run and returned at the end:
            - orderbook_allocated - new orderbook variable used for further processing which only include orders with available and allocated inventory
            - orderbook_not_allocated - secondary orderbook, just for reference and further use which shows list of all orders which did not get inventory allocated, as available qty in orderbook was 0
            - inventory - same variable as input, but with updated values
        """
        # Initialize dict datastructures for the method output
        orderbook_allocated, orderbook_not_allocated = (
            dict(),
            {"trailer": [], "rigid": [], "error": []},
        )
        # allocated_count, not_allocated_count = 0, 0

        # Iterate over each vehicle in orderbook
        for vehicle in self.orderbook:
            # Iterate over each line of the vehicle in orderbook
            for i in range(len(self.orderbook[vehicle])):
                sku = self.orderbook[vehicle][i]["SKU"]
                qty = self.orderbook[vehicle][i]["Qty"]
                # Try if needed SKU has qty in inventory dictionary, if yes, process, if not add record with 0 qty and add order to orderbook_not_allocated (see 'except KeyError')
                try:
                    # Check if available inventory is higher or equal then qty needed for order and if so, allocate it, reduce inventory and append order to appropriate vehicle in orderbook_allocated dictionary
                    if self.inventory[sku] >= qty:
                        allocated = qty
                        self.inventory[sku] -= qty
                        self.orderbook[vehicle][i]["Allocated Qty"] = allocated

                        try:
                            orderbook_allocated[vehicle].append(
                                self.orderbook[vehicle][i]
                            )
                        except KeyError:
                            orderbook_allocated[vehicle] = []
                            orderbook_allocated[vehicle].append(
                                self.orderbook[vehicle][i]
                            )
                    # If inventory is less than demand, but more then 0, allocate all inventory to order, reduce inventory to 0 and move rest of order to orderbook_not_allocated
                    elif self.inventory[sku] > 0:
                        allocated = self.inventory[sku]
                        self.inventory[sku] -= allocated
                        self.orderbook[vehicle][i]["Allocated Qty"] = allocated
                        try:
                            orderbook_allocated[vehicle].append(
                                self.orderbook[vehicle][i]
                            )
                        except KeyError:
                            orderbook_allocated[vehicle] = []
                            orderbook_allocated[vehicle].append(
                                self.orderbook[vehicle][i]
                            )

                        not_allocated_qty = qty - allocated
                        self.orderbook[vehicle][i]["Qty"] = not_allocated_qty
                        orderbook_not_allocated[vehicle].append(
                            self.orderbook[vehicle][i]
                        )

                except KeyError:
                    self.inventory[sku] = 0
                    orderbook_not_allocated[vehicle].append(self.orderbook[vehicle][i])

        return orderbook_allocated, self.inventory, orderbook_not_allocated
