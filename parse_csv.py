import csv


class EmptyFileError(Exception):
    """
    Custom exception raised when the file is empty.
    """

    def __init__(self, filename):
        super().__init__(f"The file '{filename}' is empty.")
        self.filename = filename


class ParseCSV:
    def __init__(self, file_path: str) -> None:
        """
        Construction method for the ParseCSV class.

        Parameters:
            file_path (str): The path to CSV file which will be parsed.
        """
        self.file_path = file_path

    def parse(self) -> list:
        """
        Parses CSV file specified in file_path and return list of dictionaries which represent parsed data.

        Returns:
            list: A list of dictionaries, where each dictionary represents row in parsed file
        """
        # list which stores the parsed data
        parsed_data = []
        with open(self.file_path, "r") as file:
            # Create a CSV reader object using DictReader from csv module
            reader = csv.DictReader(file)
            # Check if file is empty
            if not any(reader):
                raise EmptyFileError(self.file_path)
            else:
                # Reset the file pointer to beginning of the file
                file.seek(0)
                # Skip header row
                next(reader, None)
                # Iterate over each row in the CSV reader object
                for row in reader:
                    # Append row to parsed_data list
                    parsed_data.append(row)

        return parsed_data
