import csv
import io

class CSVParser:
    def parse(self, file_path: str) -> dict:
        with open(file_path, "r", encoding="utf-8") as file:
            file_stream = io.StringIO(file.read())
            return {"type": "csv", "content": csv.DictReader(file_stream)}