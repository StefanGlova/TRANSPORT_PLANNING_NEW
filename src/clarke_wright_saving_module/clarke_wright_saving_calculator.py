class ClarkeWrightSavingCalculator:
    def __init__(self, all_postcodes: dict, orderbook: dict):
        self.all_postcodes = all_postcodes
        self.orderbook = orderbook        

    def select_used_postcodes(self) -> dict:
        
        postcodes = dict()

        for vehicle in self.orderbook:
            for order in self.orderbook[vehicle]:
                postcode = order["Customer Postcode"]
                if postcode not in postcodes:
                    postcodes[postcode] = {
                        "Latitude": self.all_postcodes[postcode]["Latitude"],
                        "Longitude": self.all_postcodes[postcode]["Longitude"],
                    }
        
        return postcodes
            
