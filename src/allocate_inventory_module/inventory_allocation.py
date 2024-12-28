from src.errors import EmptyDatasetError, WrongKeysAllocatorError


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
                    allocated_volume, unallocated_volume = self._recalculate_volume(
                        order, allocated_qty, unallocated_qty
                    )
                    # If allocated_qty is more then 0, add key to order dict and append the order to orderbook_allocated
                    if allocated_qty > 0:
                        order["Allocated Qty"] = allocated_qty
                        order["Allocated Volume"] = allocated_volume
                        orderbook_allocated[vehicle].append(order)
                    # If unallocated_qty is more then 0, update Qty on the order and append order to orderbook_not_allocated
                    if unallocated_qty > 0:
                        order["Qty"] = unallocated_qty
                        order["Transport Volume (m3)"] = unallocated_volume
                        orderbook_not_allocated[vehicle].append(order)
                except KeyError:
                    self.inventory[order["SKU"]] = 0
                    orderbook_not_allocated[vehicle].append(order)

        return orderbook_allocated, self.inventory, orderbook_not_allocated

    def group_by_customer(self, orderbook_allocated: dict) -> dict:
        orderbook_grouped = dict()
        customers_check_trailer = []
        customers_check_rigid = []

        for vehicle, orders in orderbook_allocated.items():
            orderbook_grouped[vehicle] = []
            for order in orders:
                customer = order["Customer Name"]
                sku = order["SKU"]
                qty = order["Allocated Qty"]
                volume = order["Allocated Volume"]
                due_date = order["Due Date"]
                order_details = {
                    "SKU": sku,
                    "Qty": qty,
                    "Due Date": due_date,
                    "Allocated Volume": volume,
                }
                if customer in customers_check_trailer:
                    i = customers_check_trailer.index(customer)
                    orderbook_grouped[vehicle][i]["Total Volume"] += volume
                elif customer in customers_check_rigid:
                    i = customers_check_rigid.index(customer)
                    orderbook_grouped[vehicle][i]["Total Volume"] += volume
                else:
                    if vehicle == "trailer":
                        customers_check_trailer.append(customer)
                        i = customers_check_trailer.index(customer)
                    elif vehicle == "rigid":
                        customers_check_rigid.append(customer)
                        i = customers_check_rigid.index(customer)
                    postcode = order["Customer Postcode"]
                    customer_details = {
                        "Customer Name": customer,
                        "Customer Postcode": postcode,
                        "Total Volume": volume,
                        "Line Details": [],
                    }
                    orderbook_grouped[vehicle].append(customer_details)
                orderbook_grouped[vehicle][i]["Line Details"].append(order_details)

        return orderbook_grouped

    def split_by_volume(
        self,
        orderbook_allocated: dict,
        trailer_max: float,
        trailer_min: float,
        rigid_max: float,
        rigid_min: float,
        parcel_limit: float,
    ) -> dict:
        """
        This method is called after inventory allocation and group by customer to split orderbook to 3 orderbooks:
        1. full loads
        2. parcels
        3. multidrop loads
        """
        full_loads_trailers = list()
        full_loads_rigids = list()
        parcels = list()
        multidrop_loads_trailers = list()
        multidrop_loads_rigids = list()

        for vehicle, customers in orderbook_allocated.items():
            for customer in customers:
                volume = customer["Total Volume"]
                if volume <= parcel_limit:
                    parcels.append(customer)
                elif vehicle == "trailer":
                    if volume >= trailer_min:
                        trailers, reminder = self._split_too_large_customer(customer, trailer_max, trailer_min)
                        full_loads_trailers.extend(trailers)
                        if reminder:
                            multidrop_loads_trailers.extend(reminder)
                    else:
                        multidrop_loads_trailers.append(customer)
                elif vehicle == "rigid":
                    if volume >= rigid_min:
                        rigids, remidner = self._split_too_large_customer(customer, rigid_max, rigid_min)
                        full_loads_rigids.extend(rigids)
                        if reminder:
                            multidrop_loads_rigids.extend(reminder)
                    else:
                        multidrop_loads_rigids.append(customer)
        return (
            full_loads_trailers,
            full_loads_rigids,
            parcels,
            multidrop_loads_trailers,
            multidrop_loads_rigids,
        )

    def _split_too_large_customer(self, customer: dict, volume_max: float, volume_min: float):
        """
        Private method to split orders which are larger then volume of given vehicle. For example, if volume limit of vehicle is 50 and customer volume is 100.
        """

        loads, reminder = list(), dict()
        name = customer["Customer Name"]
        postcode = customer["Customer Postcode"]
        line_details = customer["Line Details"]
        total_volume = 0
        lines = []      

        for line in line_details:
            order_volume = line["Allocated Volume"]
            if total_volume + order_volume <= volume_max:
                total_volume += order_volume
                lines.append(line)
            else:
                load = {"Customer Name": name, "Customer Postcode": postcode, "Total Volume": total_volume, "Line Details": lines}
                loads.append(load)
                lines = [line]
                total_volume = order_volume
                
        if total_volume >= volume_min:
            loads.append({
                "Customer Name": name,
                "Customer Postcode": postcode,
                "Total Volume": total_volume,
                "Line Details": lines,
            })
        else:
            reminder = {
                "Customer Name": name,
                "Customer Postcode": postcode,
                "Total Volume": total_volume,
                "Line Details": lines,
            }

        return loads, reminder

    def _recalculate_volume(
        self, order: dict, allocated_qty: int, unallocated_qty: int
    ) -> float:
        """
        Private method to recalculate allocated and unallocated volume for given order.

        Returns allocated_volume and unallocated volume.
        """
        qty = order["Qty"]
        volume = order["Transport Volume (m3)"]
        allocated_volume = volume / qty * allocated_qty
        unallocated_volume = volume / qty * unallocated_qty

        return allocated_volume, unallocated_volume

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
            "Transport Volume (m3)",
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
