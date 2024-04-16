from modules.data_processing_module.parse_csv import GeneralFileParser


class ProcessPostcodes(GeneralFileParser):
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

    def __init__(self, file_path: str, delimiter: str = ",") -> None:
        """
        Initialize ProcessPostcodes object.
        """
        super().__init__(file_path=file_path, delimiter=delimiter)

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
        self._check_empty_list(method_called="parse_postcodes")
        # Initialize empty postocdes dict
        postcodes = dict()

        # Iterate over each item of the parsed_data list
        for row in self.parsed_data:
            # Check if row only contains correct keys
            self._check_correct_keys(row=row, method_called="parse_postcodes")

            # Check if Latitude and Longitude has correct value
            lat = self._validate_number_value(row["Latitude"], "Latitude")
            long = self._validate_number_value(row["Longitude"], "Longitude")

            # Initialize nasted dict inside postcodes dict
            postcodes[row["Postcode"]] = dict()
            # Assign Latitude and Longitude to each postcode
            postcodes[row["Postcode"]]["Latitude"] = lat
            postcodes[row["Postcode"]]["Longitude"] = long

        return postcodes
