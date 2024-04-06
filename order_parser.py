from parse_csv import ParseCSV


class OrderParser:
    def __init__(self, file_path):
        self.file_path = file_path

    def parse_orderbook(self):

        parsed_data = ParseCSV(self.file_path).parse_csv()

        # create variable orderbook for dictionary datastructure which stores data from orderbook file
        orderbook = {"trailer": list(), "rigid": list(), "ERROR": list()}

        for row in parsed_data:
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
                pass

        return orderbook
