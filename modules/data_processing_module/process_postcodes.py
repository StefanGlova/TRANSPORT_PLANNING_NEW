from modules.errors import WrongKeysError, WrongValueTypeError, WrongNumericRange


class ProcessPostcodes:
    def __init__(self, parsed_data):
        self.parsed_data = parsed_data

    def parse_postcodes(self) -> dict:
        """
        Parse data from parsed_data list into dictionary using postcode as key and nasted dictionary as value. Nasted dictionary has two keys - Latitude and Longitude and their value is of type float.

        Returns:
            dictionary: An postcode dictionary with postcode as key and value of nasted dictionary with Latitude and Longitude as key and value of float type.
        """
        # Initialize dict datastructure which stores inventry key value pairs and also variable correct_keys
        postcodes, correct_keys = dict(), ["Postcode", "Latitude", "Longitude"]
        fields = {
            "Postcode": "string",
            "Latitude": "Decimal place number",
            "Longitude": "Decimal place number",
        }
        range = {
            "Latitude": "must be in range from -90 to +90",
            "Longitude": "must be in range from -180 to +180",
        }

        # Check if parsed_data is not empty list
        if self.parsed_data == []:
            raise WrongKeysError(
                method_called="parse_postcodes", correct_keys=correct_keys
            )

        # Iterate over each item of the parsed_data list
        for row in self.parsed_data:
            # Check if row only contains correct keys
            if sorted(list(set(key for key in row.keys()))) != sorted(correct_keys):
                raise WrongKeysError(
                    method_called="parse_postcodes", correct_keys=correct_keys
                )

            # Check if Latitude and Longitude has decimal place numeric value. If has, convert to float data type, if not, raise error
            # latitude_range = [-90, 90]
            # longitude_range = [-180, 180]
            try:
                lat = float(row["Latitude"])
                if lat > 90 or lat < -90:
                    raise WrongNumericRange("Latitude", range)
            except ValueError:
                raise WrongValueTypeError("Latitude", fields)
            try:
                long = float(row["Longitude"])
                if long > 180 or long < -180:
                    raise WrongNumericRange("Longitude", range)
            except ValueError:
                raise WrongValueTypeError("Longitude", fields)

            # Initialize nasted dict inside postcodes dict
            postcodes[row["Postcode"]] = dict()
            # Assign Latitude and Longitude to each postcode
            postcodes[row["Postcode"]]["Latitude"] = lat
            postcodes[row["Postcode"]]["Longitude"] = long

        return postcodes
