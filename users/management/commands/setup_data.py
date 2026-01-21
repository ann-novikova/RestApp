from django.core.management import call_command
from django.core.management.base import BaseCommand

from content.models import RestaurantInfo


class Command(BaseCommand):
    help = "Загружает начальные данные, если база пуста"

    def handle(self, *args, **options):

        if not RestaurantInfo.objects.exists():
            self.stdout.write("Base is empty, loading data...")
            call_command("loaddata", "data.json")
            self.stdout.write(self.style.SUCCESS("Successfully loaded data"))
        else:
            self.stdout.write("Data already exists, skipping...")
