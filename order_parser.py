class OrderParser:
    def __init__(self, file_path):
        self.file_path = file_path

    def parse_orderbook(self):
        # import csv module
        import csv

        # create variable orderbook for dictionary datastructure which stores data from orderbook file
        orderbook = {"trailer": list(), "rigid": list(), "ERROR": list()}

        # open orderbook file
        with open(self.file_path, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                customer_name = row["Customer Name"]
                postcode = row["Customer Postcode"]
                sku = row["SKU"]
                qty = row["Qty"]
                vehicle = row["Vehicle Type"]
                date = row["Due Date"]
                customer = {
                    "Customer Name": customer_name,
                    "Customer Postcode": postcode,
                    "SKU": sku,
                    "Qty": qty,
                    "Due Date": date,
                }
                if vehicle == "trailer":
                    orderbook["trailer"].append(customer)
                elif vehicle == "rigid":
                    orderbook["rigid"].append(customer)
                else:
                    pass

        return orderbook
