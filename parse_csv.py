import csv


class ParseCSV:
    def __init__(self, file_path):
        self.file_path = file_path

    def parse(self):
        parsed_data = []
        with open(self.file_path, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                parsed_data.append(row)
        return parsed_data
