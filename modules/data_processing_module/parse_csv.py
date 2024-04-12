import pandas as pd
from modules.errors import EmptyFileError, WrongKeysError


class GeneralFileParser:
    def __init__(self, file_path: str, delimiter: str = ",") -> None:
        """
        Construction method for the ParseCSV class.

        Parameters:
            file_path (str): The path to CSV file which will be parsed.
            delimiter (str): The delimiter used in the CSV file with ',' as default.
        """
        self.file_path = file_path
        self.delimiter = delimiter

    def parse(self) -> list:
        """
        Parses CSV file specified in file_path and return list of dictionaries which represent parsed data.

        The method works on 2 different scenarios:
            1. delimiter is ',' - then it uses Pandas to parse the file and loop through the rows to ensure each value is of type str
            2. delimiter is something else - then it reads the file separate 1st line as header from all the other lines. It is based on scenario that last column is date separated year, month and day with same delimiter as columns in the file.

        Returns:
            list: A list of dictionaries, where each dictionary represents row in parsed file
        """
        if self.delimiter == ",":
            try:
                df = pd.read_csv(self.file_path, delimiter=self.delimiter)
                parsed_data = df.to_dict(orient="records")
                for row in parsed_data:
                    for key, value in row.items():
                        row[key] = str(value)
            except pd.errors.EmptyDataError:
                raise EmptyFileError(self.file_path)
        else:
            # Initialize parsed_data list variable which will be returned from parse method
            parsed_data = list()

            # Read the file
            with open(self.file_path, "r") as file:
                # get header
                header = file.readline()
                # get rows
                rows = list()
                for line in file:
                    rows.append(line)

            # Split header to list of column names, removing any white space or 'end of line' symbol
            header = header.strip().split(self.delimiter)

            # Iterate through rows
            for row in rows:
                # Split row to list of columns, removing any white space or 'end of line' symbol
                row = row.strip().split(self.delimiter)
                # Initialize / re-initialize empty dict
                entry = dict()
                # Iterate through all lines and enter keys and values to entry dict - if line has more columns than header, it join reminding coluns to one value - based on scenario that last column in that case is date separated with same delimiter than columns in the origina file
                for i in range(len(header)):
                    if i == len(header) - 1:
                        entry[header[i]] = self.delimiter.join(row[i:])
                    else:
                        entry[header[i]] = row[i]

                # Append created dict to parsed_data list
                parsed_data.append(entry)

        return parsed_data

    def parse_inventory(self) -> dict:
        """
        Parse data from parsed_data list into dictionary and group them by SKU.

        Returns:
            dictionary: An inventory dictionary of SKU and it qty, grouped by SKU.
        """
        # Initialize dict datastructure which stores inventry key value pairs and also variable correct_keys
        inventory, correct_keys = dict(), ["SKU", "Qty"]

        # Check if parsed_data is not empty list
        if self.parsed_data == []:
            raise WrongKeysError(
                method_called="parse_inventory", correct_keys=correct_keys
            )

        # Iterate over each item of the parsed_data list
        for row in self.parsed_data:
            # Check if row only contains correct keys
            if sorted(list(set(key for key in row.keys()))) != sorted(correct_keys):
                raise WrongKeysError(
                    method_called="parse_inventory", correct_keys=correct_keys
                )

            # If SKU already exist in inventory dict, then it increment its value by Qty, if does not exist, it adds it with its initial Qty
            inventory[row["SKU"]] = inventory.get(row["SKU"], 0) + int(row["Qty"])

        return inventory

    def parse_orderbook(self) -> dict:
        """
        Parse data from parsed_data list into dictionary of lists.

        Returns:
            dictionary: A orderbook dictionary of three lists: trailer, rigid and ERROR. Each list is list of dictionarie containing information about orders.
        """
        # Initialize dict datastructure which stores inventry key value pairs and also variable correct_keys
        orderbook = {"trailer": list(), "rigid": list(), "ERROR": list()}
        correct_keys = [
            "Customer Name",
            "Customer Postcode",
            "SKU",
            "Qty",
            "Vehicle Type",
            "Due Date",
        ]

        # Check if parsed_data is not empty list
        if self.parsed_data == []:
            raise WrongKeysError(
                method_called="parse_orderbook", correct_keys=correct_keys
            )

        # Iterate over each item of the parsed_data list
        for row in self.parsed_data:
            # Check if row only contains correct keys
            if sorted(list(set(key for key in row.keys()))) != sorted(correct_keys):
                raise WrongKeysError(
                    method_called="parse_orderbook", correct_keys=correct_keys
                )

            # Create customer variable (dict) which store data from each row
            customer = {
                "Customer Name": row["Customer Name"],
                "Customer Postcode": row["Customer Postcode"],
                "SKU": row["SKU"],
                "Qty": row["Qty"],
                "Due Date": row["Due Date"],
            }
            # Create vehicle variable (str) which stores vehicle type
            vehicle = row["Vehicle Type"]

            # Check vehicle type and append customer dict  to correct list of orderbook dict
            if vehicle == "trailer":
                orderbook["trailer"].append(customer)
            elif vehicle == "rigid":
                orderbook["rigid"].append(customer)
            else:
                orderbook["ERROR"].append(customer)

        return orderbook

    def parse_postcodes(self) -> dict:
        """
        Parse data from parsed_data list into dictionary using postcode as key and nasted dictionary as value. Nasted dictionary has two keys - Latitude and Longitude and their value is of type float.

        Returns:
            dictionary: An postcode dictionary with postcode as key and value of nasted dictionary with Latitude and Longitude as key and value of float type.
        """
        # Initialize dict datastructure which stores inventry key value pairs and also variable correct_keys
        postcodes, correct_keys = dict(), ["Postcode", "Latitude", "Longitude"]

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

            # Initialize nasted dict inside postcodes dict
            postcodes[row["Postcode"]] = dict()
            # Assign Latitude and Longitude to each postcode
            postcodes[row["Postcode"]]["Latitude"] = float(row["Latitude"])
            postcodes[row["Postcode"]]["Longitude"] = float(row["Longitude"])

        return postcodes
