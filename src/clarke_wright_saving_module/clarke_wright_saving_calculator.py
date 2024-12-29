from src.errors import MissingPostcodeError


class ClarkeWrightSavingCalculator:
    def __init__(self, all_postcodes: dict, orderbook: list):
        self.all_postcodes = all_postcodes
        self.orderbook = orderbook

    def select_used_postcodes(self) -> dict:

        postcodes = dict()

        for order in self.orderbook:
            postcode = order["Customer Postcode"]
            if postcode not in postcodes:
                try:
                    postcodes[postcode] = {
                        "Latitude": self.all_postcodes[postcode]["Latitude"],
                        "Longitude": self.all_postcodes[postcode]["Longitude"],
                    }
                except KeyError:
                    raise (MissingPostcodeError(postcode))

        return postcodes
