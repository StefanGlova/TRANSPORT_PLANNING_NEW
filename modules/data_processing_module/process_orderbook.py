from modules.data_processing_module.general_file_parser import GeneralFileParser


class ProcessOrderbook(GeneralFileParser):
    # Initialize global variable for ProcessOrderbook class
    CORRECT_KEYS = [
        "Customer Name",
        "Customer Postcode",
        "SKU",
        "Qty",
        "Vehicle Type",
        "Due Date",
        "Transport Volume (m3)",
    ]

    FIELDS = {
        "Customer Name": "string",
        "Customer Postcode": "string",
        "SKU": "string",
        "Qty": "number",
        "Vehicle Type": "string",
        "Due Date": "date",
        "Transport Volume (m3)": "number",
    }

    RANGE = {
        "Qty": "cannot be negative",
        "Transport Volume (m3)": "cannot be negative",
    }

    def __init__(self, file_path: str, delimiter: str = ",") -> None:
        """
        Initialize ProcessOrderbook object.
        """
        super().__init__(file_path=file_path, delimiter=delimiter)

    def parse_orderbook(self) -> dict:
        """
        Parse data from parsed_data list into dictionary of lists.

        Input:
            parsed_data: list
            Input list must not be empty - check before further process with parse_orderbook method and raises error if it is empty.
            The list must have these fields - validation of numeric and date fields is checked by private methods
            Expected fields:
                "Customer Name": "string",
                "Customer Postcode": "string",
                "SKU": "string",
                "Qty": "number", "cannot be negative"
                "Vehicle Type": "string",
                "Due Date": "date",
                "Transport Volume (m3)": "number", "cannot be negative"

        Returns:
            dictionary: A orderbook dictionary of three lists: trailer, rigid and ERROR. Each list is list of dictionarie containing information about orders.
        """
        # Check if input is not empty list. Raise appropriate error if it is
        self._check_empty_list(method_called="parse_orderbook")

        # Initialise empty orderbook
        orderbook = {"trailer": list(), "rigid": list(), "ERROR": list()}

        # Iterate over each item of the parsed_data list
        for row in self.parsed_data:
            # Check if each row has correct keys
            self._check_correct_keys(row=row, method_called="parse_orderbook")
            # Check if qty and voluem are correct numeric value and date is correct date
            qty = self._validate_number_value(row["Qty"], "Qty")
            volume = self._validate_number_value(
                row["Transport Volume (m3)"], "Transport Volume (m3)"
            )
            date = self._validate_date(row["Due Date"])

            # Create customer variable (dict) which store data from each row
            customer = {
                "Customer Name": row["Customer Name"],
                "Customer Postcode": row["Customer Postcode"],
                "SKU": row["SKU"],
                "Qty": qty,
                "Due Date": date,
                "Transport Volume (m3)": volume,
            }
            # Create vehicle variable (str) which stores vehicle type
            vehicle = row["Vehicle Type"]

            # Append customer dict to correct list of orderbook dict
            if vehicle == "trailer":
                orderbook["trailer"].append(customer)
            elif vehicle == "rigid":
                orderbook["rigid"].append(customer)
            else:
                orderbook["ERROR"].append(customer)

        return orderbook
