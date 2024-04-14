class InventoryAllocation:
    def __init__(self, orderbook, inventory):
        self.orderbook = orderbook
        self.inventory = inventory

    def allocate_inventory(self):

        orderbook_allocated, inventory_left, orderbook_not_allocated = (
            dict(),
            dict(),
            {"trailer": [], "rigid": [], "error": []},
        )

        for vehicle in self.orderbook:
            for i in range(len(self.orderbook[vehicle])):
                sku = self.orderbook[vehicle][i]["SKU"]
                qty = self.orderbook[vehicle][i]["Qty"]
                if self.inventory[sku] >= qty:
                    allocated = qty
                    inventory_left[sku] = (
                        inventory_left.get(sku, self.inventory[sku]) - qty
                    )
                    self.orderbook[vehicle][i]["Allocated Qty"] = allocated

                    try:
                        orderbook_allocated[vehicle].append(self.orderbook[vehicle][i])
                    except KeyError:
                        orderbook_allocated[vehicle] = []
                        orderbook_allocated[vehicle].append(self.orderbook[vehicle][i])

        return orderbook_allocated, inventory_left, orderbook_not_allocated
