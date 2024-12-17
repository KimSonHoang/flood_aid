import random

from django.core.management.base import BaseCommand

from donations.models import DisasterArea
from faker import Faker
from geopy.geocoders import Nominatim


class Command(BaseCommand):
    help = "Description of your command"

    def handle(self, *args, **options):
        def generate_disaster_area():
            lat = round(random.uniform(min_lat, max_lat), 6)
            lon = round(random.uniform(min_lon, max_lon), 6)

            location = geolocator.reverse(f"{lat}, {lon}", language="en")
            if location:
                name = location.raw.get("address", {}).get(
                    "road", ""
                ) or location.raw.get("address", {}).get("suburb", "")
                if not name:
                    name = f"Area in {random.choice(districts)}"
            else:
                name = f"Area in {random.choice(districts)}"

            return {
                "name": name,
                "latitude": lat,
                "longitude": lon,
                "severity": random.choice(DisasterArea.SEVERITY_CHOICES)[0],
            }

        Faker()
        geolocator = Nominatim(user_agent="disaster_area_populator")

        min_lat, max_lat = 10.3776, 10.8961
        min_lon, max_lon = 106.3638, 106.8777

        districts = [
            "Quan 1",
            "Quan 2",
            "Quan 3",
            "Quan 4",
            "Quan 5",
            "Quan 6",
            "Quan 7",
            "Quan 8",
            "Quan 9",
            "Quan 10",
            "Quan 11",
            "Quan 12",
            "Binh Thanh",
            "Thu Duc",
            "Go Vap",
            "Phu Nhuan",
            "Tan Binh",
            "Tan Phu",
            "Binh Tan",
        ]

        for _ in range(100): # Generate 100 records
            disaster_area_data = generate_disaster_area()
            DisasterArea.objects.create(**disaster_area_data)
            print(f"Created: {disaster_area_data['name']}")

        print("Population complete!")
