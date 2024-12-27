class ClarkeWrightSavingCalculator:
    def __init__(self, all_postcodes: dict, orderbook: dict):
        self.all_postcodes = all_postcodes
        self.orderbook = orderbook        

    def select_used_postcodes(self) -> dict:
        pass