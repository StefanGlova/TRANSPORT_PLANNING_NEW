from modules.errors import WrongKeysError, WrongValueTypeError, WrongNumericRange


class ProcessPostcodes:
    # Initialize global variable for ProcessPostcodes class
    CORRECT_KEYS = ["Postcode", "Latitude", "Longitude"]

    FIELDS = {
        "Postcode": "string",
        "Latitude": "Decimal place number",
        "Longitude": "Decimal place number",
    }

    RANGE = {
        "Latitude": "must be in range from -90 to +90",
        "Longitude": "must be in range from -180 to +180",
    }

    def __init__(self, parsed_data: list) -> None:
        """
        Initialize ProcessPostcodes object.
        """
        self.parsed_data = parsed_data

    def parse_postcodes(self) -> dict:
        """
        Parse data from parsed_data list into dictionary using postcode as key and nasted dictionary as value. Nasted dictionary has two keys - Latitude and Longitude and their value is of type float.

        Input:
        parsed_data: list
        Input list must not be empty - check before further process with parse_orderbook method and raises error if it is empty.
        The list must have these fields - validation of numeric and date fields is checked by private methods
        Expected fields:
        "Postcode": "string",
        "Latitude": "Decimal place number", "must be in range from -90 to +90"
        "Longitude": "Decimal place number", "must be in range from -180 to +180"

        Returns:
            dictionary: An postcode dictionary with postcode as key and value of nasted dictionary with Latitude and Longitude as key and value of float type.
        """
        # Check if input is not empty list
        self._check_empty_list()
        # Initialize empty postocdes dict
        postcodes = dict()

        # Iterate over each item of the parsed_data list
        for row in self.parsed_data:
            # Check if row only contains correct keys
            self._check_correct_keys(row)

            # Check if Latitude and Longitude has correct value
            lat = self._validate_number_value(row["Latitude"], "Latitude")
            long = self._validate_number_value(row["Longitude"], "Longitude")

            # Initialize nasted dict inside postcodes dict
            postcodes[row["Postcode"]] = dict()
            # Assign Latitude and Longitude to each postcode
            postcodes[row["Postcode"]]["Latitude"] = lat
            postcodes[row["Postcode"]]["Longitude"] = long

        return postcodes

    def _check_empty_list(self) -> None:
        """
        Private method checking if input list is not empty. If it is, it raises error. For error details, please refer to errors.py file.
        """
        if self.parsed_data == []:
            raise WrongKeysError(
                method_called="parse_postcodes", correct_keys=self.CORRECT_KEYS
            )

    def _check_correct_keys(self, row: dict) -> None:
        """
        Private method checking if every row(dictionary) in the input list has correct keys. If not, it raises error. For error details, please refer to errors.py file.
        """
        if sorted(list(set(key for key in row.keys()))) != sorted(self.CORRECT_KEYS):
            raise WrongKeysError(
                method_called="parse_postcodes", correct_keys=self.CORRECT_KEYS
            )

    def _validate_number_value(self, value: str, field: str) -> float:
        """
        Private method checking if input value can be converted to floating point number and whether the number is in expected range. If any of these fails, it raises appropriate error. For error details, please refer to errors.py file.
        """
        try:
            value = float(value)
            if field == "Latitude":
                if value > 90 or value < -90:
                    raise WrongNumericRange(field, self.RANGE)
                else:
                    return value
            elif field == "Longitude":
                if value > 180 or value < -180:
                    raise WrongNumericRange(field, self.RANGE)
                else:
                    return value
        except ValueError:
            raise WrongValueTypeError(field, self.FIELDS)
