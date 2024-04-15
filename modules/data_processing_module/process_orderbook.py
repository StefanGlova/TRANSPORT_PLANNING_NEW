from modules.errors import WrongKeysError, WrongValueTypeError, WrongNumericRange
from datetime import datetime
import re


class ProcessOrderbook:
    def __init__(self, parsed_data: list):
        self.parsed_data = parsed_data

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

    def parse_orderbook(self) -> dict:
        """
        Parse data from parsed_data list into dictionary of lists.

        Input:
            parsed_data: list
            Input list must not be empty - check before further process with parse_orderbook method and raises error if it is empty.
            The list must have these fields - validation of numeric and date fields is checked by private methods
                "Customer Name": "string",
                "Customer Postcode": "string",
                "SKU": "string",
                "Qty": "number",
                "Vehicle Type": "string",
                "Due Date": "date",
                "Transport Volume (m3)": "number",

        Returns:
            dictionary: A orderbook dictionary of three lists: trailer, rigid and ERROR. Each list is list of dictionarie containing information about orders.
        """
        # Check if input is not empty list. Raise appropriate error if it is
        self._check_empty_list()

        # Initialise empty orderbook
        orderbook = {"trailer": list(), "rigid": list(), "ERROR": list()}

        # Iterate over each item of the parsed_data list
        for row in self.parsed_data:
            # Check if each row has correct keys
            self._check_correct_keys(row)
            # Check if qty and voluem are correct numeric value and date is correct date
            qty = self._validate_number_values(row["Qty"], "Qty")
            volume = self._validate_number_values(
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

    def _check_empty_list(self) -> None:
        """
        Private method checking if input list is not empty. If it is, it raises error. For error details, please refer to errors.py file.
        """
        if self.parsed_data == []:
            raise WrongKeysError(
                method_called="parse_orderbook", correct_keys=self.CORRECT_KEYS
            )

    def _check_correct_keys(self, row: dict) -> None:
        """
        Private method checking if every row(dictionary) in the input list has correct keys. If not, it raises error. For error details, please refer to errors.py file.
        """
        if sorted(list(set(key for key in row.keys()))) != sorted(self.CORRECT_KEYS):
            raise WrongKeysError(
                method_called="parse_orderbook", correct_keys=self.CORRECT_KEYS
            )

    def _validate_number_values(self, value: str, field_name: str) -> float:
        """
        Private method checking if input value can be converted to floating point number and whether the number is not negative. If any of these fails, it raises appropriate error. For error details, please refer to errors.py file.
        """
        try:
            value = float(value)
            if value < 0:
                raise WrongNumericRange(field_name, self.RANGE)
            else:
                return value
        except ValueError:
            raise WrongValueTypeError(field_name, self.FIELDS)

    def _validate_date(self, value: str) -> datetime:
        """
        Private method checking if input value can be converted to datetime object. If not, it raises an error. For error details, please refer to errors.py file.
        """
        try:
            date_string = value
            match = re.search(r"\d{4}-\d{2}-\d{2}", date_string)
            date = datetime.strptime(match.group(), "%Y-%m-%d").date()
            return date
        except AttributeError:
            raise WrongValueTypeError("Due Date", self.FIELDS)
