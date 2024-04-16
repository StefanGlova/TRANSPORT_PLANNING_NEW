import pandas as pd
from modules.errors import (
    EmptyFileError,
    WrongKeysError,
    WrongValueTypeError,
    WrongNumericRange,
)
from datetime import datetime
import re


class GeneralFileParser:

    CORRECT_KEYS = []
    FIELDS = {}
    RANGE = {}

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
                raise EmptyFileError(filename=self.file_path)
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

    def _check_empty_list(self, method_called) -> None:
        """
        Private method checking if input list is not empty. If it is, it raises error. For error details, please refer to errors.py file.
        """
        if self.parsed_data == []:
            raise WrongKeysError(
                method_called=method_called, correct_keys=self.CORRECT_KEYS
            )

    def _check_correct_keys(self, row: dict, method_called) -> None:
        """
        Private method checking if every row(dictionary) in the input list has correct keys. If not, it raises error. For error details, please refer to errors.py file.
        """
        if sorted(list(set(key for key in row.keys()))) != sorted(self.CORRECT_KEYS):
            raise WrongKeysError(
                method_called=method_called, correct_keys=self.CORRECT_KEYS
            )

    def _validate_number_value(self, value: str, field: str) -> float:
        """
        Private method checking if input value can be converted to floating point number and whether the number is in expected range. If any of these fails, it raises appropriate error. For error details, please refer to errors.py file.
        """
        try:
            value = float(value)
            if field == "Latitude":
                if value > 90 or value < -90:
                    raise WrongNumericRange(parameter=field, range=self.RANGE)
                else:
                    return value
            elif field == "Longitude":
                if value > 180 or value < -180:
                    raise WrongNumericRange(parameter=field, range=self.RANGE)
                else:
                    return value
            else:
                if value < 0:
                    raise WrongNumericRange(parameter=field, range=self.RANGE)
                else:
                    return value
        except ValueError:
            raise WrongValueTypeError(parameter=field, field=self.FIELDS)

    def _validate_date(self, value: str) -> datetime:
        """
        Private method checking if input value can be converted to datetime object. If not, it raises an error. For error details, please refer to errors.py file.
        """
        try:
            date_string = value
            match = re.search(r"\d{4}-\d{2}-\d{2}", date_string)
            date = datetime.strptime(match.group(), "%Y-%m-%d").date()
            return date
        except AttributeError:
            raise WrongValueTypeError(parameter="Due Date", field=self.FIELDS)
