from django.core.management.base import BaseCommand
from django.db import IntegrityError
from money_api.csv_importer import CSVImporter


class Command(BaseCommand):
    help = "Save users models to database"

    def add_arguments(self, parser):
        parser.add_argument("file", type=str, help="Location of file with users")

    def handle(self, *args, **kwargs):
        csv_file = kwargs["file"]
        try:
            with open(csv_file) as file:
                importer = CSVImporter(file)
                importer.read_and_save_data()
        except (FileNotFoundError, IntegrityError, ValueError, TypeError) as exc:
            self.stderr.write(f"Exception occured while handling the file - {exc}")
