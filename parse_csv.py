import csv
import pandas as pd


class EmptyFileError(Exception):
    """
    Custom exception raised when the file is empty.
    """

    def __init__(self, filename):
        super().__init__(f"The file '{filename}' is empty.")
        self.filename = filename


class ParseCSV:
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
            rows, parsed_data = list(), list()
            with open(self.file_path, "r") as file:
                # get header
                header = file.readline()
                # get rows
                for line in file:
                    rows.append(line)
            header = header.strip().split(self.delimiter)

            for row in rows:
                row = row.strip().split(self.delimiter)
                entry = dict()
                for i in range(len(header)):
                    if i == len(header) - 1:
                        entry[header[i]] = self.delimiter.join(row[i:])
                    else:
                        entry[header[i]] = row[i]

                parsed_data.append(entry)

        return parsed_data
