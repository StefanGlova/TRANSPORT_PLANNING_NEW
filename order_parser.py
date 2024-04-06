from parse_csv import ParseCSV


class OrderParser:
    def __init__(self, parsed_data):
        self.parsed_data = parsed_data

    def parse_orderbook(self):

        # create variable orderbook for dictionary datastructure which stores data from orderbook file
        orderbook = {"trailer": list(), "rigid": list(), "ERROR": list()}

        for row in self.parsed_data:
            customer = {
                "Customer Name": row["Customer Name"],
                "Customer Postcode": row["Customer Postcode"],
                "SKU": row["SKU"],
                "Qty": row["Qty"],
                "Due Date": row["Due Date"],
            }
            vehicle = row["Vehicle Type"]

            if vehicle == "trailer":
                orderbook["trailer"].append(customer)
            elif vehicle == "rigid":
                orderbook["rigid"].append(customer)
            else:
                orderbook["ERROR"].append(customer)

        return orderbook
