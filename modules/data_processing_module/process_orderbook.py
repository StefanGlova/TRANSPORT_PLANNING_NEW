from modules.errors import WrongKeysError, WrongValueTypeError
from datetime import datetime
import re


class ProcessOrderbook:
    def __init__(self, parsed_data):
        self.parsed_data = parsed_data

    def parse_orderbook(self) -> dict:
        """
        Parse data from parsed_data list into dictionary of lists.

        Returns:
            dictionary: A orderbook dictionary of three lists: trailer, rigid and ERROR. Each list is list of dictionarie containing information about orders.
        """
        # Initialize dict datastructure which stores inventry key value pairs and also variable correct_keys
        orderbook = {"trailer": list(), "rigid": list(), "ERROR": list()}
        correct_keys = [
            "Customer Name",
            "Customer Postcode",
            "SKU",
            "Qty",
            "Vehicle Type",
            "Due Date",
        ]

        fields = {
            "Customer Name": "string",
            "Customer Postcode": "string",
            "SKU": "string",
            "Qty": "number",
            "Vehicle Type": "string",
            "Due Date": "date",
        }

        # Check if parsed_data is not empty list
        if self.parsed_data == []:
            raise WrongKeysError(
                method_called="parse_orderbook", correct_keys=correct_keys
            )

        # Iterate over each item of the parsed_data list
        for row in self.parsed_data:
            # Check if row only contains correct keys
            if sorted(list(set(key for key in row.keys()))) != sorted(correct_keys):
                raise WrongKeysError(
                    method_called="parse_orderbook", correct_keys=correct_keys
                )
            # Check if Qty field has numeric value
            try:
                qty = int(row["Qty"])
            except ValueError:
                raise WrongValueTypeError("Qty", fields)

            # Check if Due Date field has date format
            try:
                date_string = row["Due Date"]
                match = re.search(r"\d{4}-\d{2}-\d{2}", date_string)
                date = datetime.strptime(match.group(), "%Y-%m-%d").date()
            except AttributeError:
                raise WrongValueTypeError("Due Date", fields)
            # Create customer variable (dict) which store data from each row
            customer = {
                "Customer Name": row["Customer Name"],
                "Customer Postcode": row["Customer Postcode"],
                "SKU": row["SKU"],
                "Qty": qty,
                "Due Date": date,
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
