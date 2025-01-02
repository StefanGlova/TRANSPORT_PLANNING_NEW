class ClarkeWrightVehiclePlanner:
    def __init__(self):
        pass

    def count_postcodes(self, orderbook: dict) -> dict:
        """
        method which count how many orders have same postcode
        """

        postcodes_count = dict()

        for order in orderbook:
            postcode = order["Customer Postcode"]
            postcodes_count[postcode] = postcodes_count.get(postcode, 0) + 1
        
        return postcodes_count

