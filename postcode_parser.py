class PostcodeParser:
    def __init__(self, parsed_data: list):
        self.parsed_data = parsed_data

    def parse_postcodes(self) -> dict:

        postcodes = dict()

        for row in self.parsed_data:
            postcodes[row["Postcode"]] = dict()
            postcodes[row["Postcode"]]["Latitude"] = float(row["Latitude"])
            postcodes[row["Postcode"]]["Longitude"] = float(row["Longitude"])

        return postcodes
