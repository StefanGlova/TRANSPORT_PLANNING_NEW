class PostcodeParser:
    def __init__(self, parsed_data: list):
        """
        Constructor method for PostcodeParser class.

        Paramethers:
            parsed_data (list): A list of dictionaries, where each dictionary represents row in parsed postcode file
        """
        self.parsed_data = parsed_data

    def parse_postcodes(self) -> dict:
        """
        Parse data from parsed_data list into dictionary using postcode as key and nasted dictionary as value. Nasted dictionary has two keys - Latitude and Longitude and their value is of type float.

        Returns:
            dictionary: An postcode dictionary with postcode as key and value of nasted dictionary with Latitude and Longitude as key and value of float type.
        """
        # Initialize dict datastructure which stores postcodes
        postcodes = dict()
        # Iterate over each item of the parsed_data list
        for row in self.parsed_data:
            # Initialize nasted dict inside postcodes dict
            postcodes[row["Postcode"]] = dict()
            # Assign Latitude and Longitude to each postcode
            postcodes[row["Postcode"]]["Latitude"] = float(row["Latitude"])
            postcodes[row["Postcode"]]["Longitude"] = float(row["Longitude"])

        return postcodes
