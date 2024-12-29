from src.errors import MissingPostcodeError, PairsCreationError


class ClarkeWrightSavingCalculator:
    def __init__(self, all_postcodes: dict, orderbook: list) -> dict:
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

    def create_pairs(self, postcodes: dict) -> list[tuple]:
        pairs = list()
        postcodes_list = list(dict.fromkeys(postcodes))

        if len(postcodes_list) < 2:
            raise PairsCreationError

        for i in range(len(postcodes_list)):
            for j in range(i + 1, len(postcodes_list)):
                pairs.append((postcodes_list[i], postcodes_list[j]))

        return pairs

    def calculate_distance(self, postcodes: dict, pairs: list, circuity: float = 1.2) -> list:
        """
        
        """
        
        distance = list()

        for pair in pairs:
            postcode_1, postcode_2 = pair
            lat_1 = postcodes[postcode_1]["Latitude"]
            long_1 = postcodes[postcode_1]["Longitude"]
            lat_2 = postcodes[postcode_2]["Latitude"]
            long_2 = postcodes[postcode_2]["Longitude"]
            haversine_distance = self._haversine_formula(lat_1, lat_2, long_1, long_2, circuity)
            distance.append(
                {
                    "postcode_1": postcode_1,
                    "postcode_2": postcode_2,
                    "distance": haversine_distance
                }
            )
        
        return distance
    
    def calculate_distance_from_origin(self, postcodes: dict, origin_lat: float, origin_long: float, circuity: float = 1.2) -> float:
        """
        """
        distance_from_origin = dict()

        for postcode in postcodes:
            lat = postcodes[postcode]["Latitude"]
            long = postcodes[postcode]["Longitude"]
            distance = self._haversine_formula(lat, origin_lat, long, origin_long, circuity)
            distance_from_origin[postcode] = distance

        return distance_from_origin



    def _haversine_formula(self, lat_1: float, lat_2: float, long_1: float, long_2: float, circuity: float = 1.2) -> float:
        from math import pi, sin, cos, acos

        haversine_distance = 3959 * (acos(sin(lat_1 * pi / 180) * sin(lat_2 * pi / 180)
                                    + cos(lat_1 * pi / 180) * cos(lat_2 * pi / 180)
                                    * cos(long_1 * pi / 180 - long_2 * pi / 180)
                                    )) * circuity

        return haversine_distance