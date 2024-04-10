# TODO to be deleted


class OrderParser:
    def __init__(self, parsed_data: list) -> None:
        """
        Constructor method for OrderParser class.

        Paramethers:
            parsed_data (list): A list of dictionaries, where each dictionary represents row in parsed orderbook file
        """
        self.parsed_data = parsed_data

    def parse_orderbook(self) -> dict:
        """
        Parse data from parsed_data list into dictionary of lists.

        Returns:
            dictionary: A orderbook dictionary of three lists: trailer, rigid and ERROR. Each list is list of dictionarie containing information about orders.
        """
        # Initialize dict datastructure which stores data from orderbook file
        orderbook = {"trailer": list(), "rigid": list(), "ERROR": list()}
        # Iterate over each item of the parsed_data list
        for row in self.parsed_data:
            # Create customer variable (dict) which store data from each row
            customer = {
                "Customer Name": row["Customer Name"],
                "Customer Postcode": row["Customer Postcode"],
                "SKU": row["SKU"],
                "Qty": row["Qty"],
                "Due Date": row["Due Date"],
            }
            # Create vehicle variable (str) which stores vehicle type
            vehicle = row["Vehicle Type"]

            # Check vehicle type and append customer dict  to correct list of orderbook dict
            if vehicle == "trailer":
                orderbook["trailer"].append(customer)
            elif vehicle == "rigid":
                orderbook["rigid"].append(customer)
            else:
                orderbook["ERROR"].append(customer)

        return orderbook
