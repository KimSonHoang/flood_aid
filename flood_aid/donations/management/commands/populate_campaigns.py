import random
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import CharityOrganization, User
from donations.models import Campaign, DisasterArea


class Command(BaseCommand):
    def handle(self, *args, **options):
        owner_user, _ = User.objects.get_or_create(
            email="demo@hcmus.edu.com",
            is_verified=True,
            user_type="charity",
            password="Password123!",
        )
        charity_org, _ = CharityOrganization.objects.get_or_create(
            name="Hội chữ thập đỏ Việt Nam", owner_id=owner_user.id, is_approve=True
        )

        storm_data = [
            {
                "title": "Cứu trợ khẩn cấp sau bão Linda",
                "description": (
                    "Một trong những cơn bão mạnh nhất đổ bộ vào Nam Bộ, gây thiệt hại"
                    " nặng nề tại các tỉnh miền Tây Nam Bộ, đặc biệt là Cà Mau, Bạc"
                    " Liêu, làm 778 người thiệt mạng."
                ),
                "date": datetime(1997, 11, 2, tzinfo=timezone.utc),
            },
            {
                "title": "Hỗ trợ khắc phục hậu quả bão Xangsane",
                "description": (
                    "Gây thiệt hại nghiêm trọng tại Đà Nẵng và các tỉnh miền Trung, với"
                    " sức gió giật cấp 13, làm 76 người thiệt mạng và thiệt hại khoảng"
                    " 10 nghìn tỷ đồng."
                ),
                "date": datetime(2006, 10, 1, tzinfo=timezone.utc),
            },
            {
                "title": "Cứu trợ nạn nhân bão Ketsana",
                "description": (
                    "Gây lũ lụt nghiêm trọng tại miền Trung, đặc biệt tại Quảng Nam,"
                    " Quảng Ngãi, làm 163 người thiệt mạng và mất tích."
                ),
                "date": datetime(2009, 9, 29, tzinfo=timezone.utc),
            },
            {
                "title": "Hỗ trợ khắc phục sau bão Mirinae",
                "description": (
                    "Gây mưa lớn và lũ lụt tại các tỉnh Nam Trung Bộ, làm 122 người"
                    " thiệt mạng và mất tích."
                ),
                "date": datetime(2009, 11, 2, tzinfo=timezone.utc),
            },
            {
                "title": "Cứu trợ khẩn cấp sau bão Nari",
                "description": (
                    "Đổ bộ vào khu vực Đà Nẵng - Quảng Nam với sức gió mạnh cấp 12, gây"
                    " thiệt hại nặng về người và tài sản."
                ),
                "date": datetime(2013, 10, 15, tzinfo=timezone.utc),
            },
            {
                "title": "Hỗ trợ nạn nhân siêu bão Haiyan",
                "description": (
                    "Siêu bão mạnh nhất năm 2013, suy yếu khi vào Việt Nam nhưng vẫn"
                    " gây thiệt hại đáng kể tại các tỉnh miền Trung."
                ),
                "date": datetime(2013, 11, 11, tzinfo=timezone.utc),
            },
            {
                "title": "Cứu trợ sau bão Rammasun",
                "description": (
                    "Gây thiệt hại nặng tại các tỉnh phía Bắc, đặc biệt là Quảng Ninh,"
                    " với gió giật trên cấp 12."
                ),
                "date": datetime(2014, 7, 19, tzinfo=timezone.utc),
            },
            {
                "title": "Hỗ trợ khắc phục hậu quả bão Kalmaegi",
                "description": (
                    "Gây mưa lớn tại các tỉnh phía Bắc, làm 13 người thiệt mạng và"
                    " thiệt hại về tài sản."
                ),
                "date": datetime(2014, 9, 16, tzinfo=timezone.utc),
            },
            {
                "title": "Cứu trợ nạn nhân bão Doksuri",
                "description": (
                    "Đổ bộ vào Hà Tĩnh-Quảng Bình với sức gió mạnh cấp 12, gây thiệt"
                    " hại nặng về người và tài sản."
                ),
                "date": datetime(2017, 9, 15, tzinfo=timezone.utc),
            },
            {
                "title": "Hỗ trợ khẩn cấp sau bão Damrey",
                "description": (
                    "Gây thiệt hại nghiêm trọng tại các tỉnh Nam Trung Bộ, làm 106"
                    " người thiệt mạng và mất tích."
                ),
                "date": datetime(2017, 11, 4, tzinfo=timezone.utc),
            },
            {
                "title": "Cứu trợ nạn nhân bão Son-Tinh",
                "description": (
                    "Gây mưa lớn và lũ quét tại các tỉnh miền Bắc, làm 32 người thiệt"
                    " mạng."
                ),
                "date": datetime(2018, 7, 18, tzinfo=timezone.utc),
            },
            {
                "title": "Hỗ trợ khắc phục sau bão Usagi",
                "description": (
                    "Gây ngập lụt nghiêm trọng tại TP.HCM và các tỉnh Nam Bộ."
                ),
                "date": datetime(2018, 11, 25, tzinfo=timezone.utc),
            },
            {
                "title": "Cứu trợ khẩn cấp sau bão Wipha",
                "description": (
                    "Gây mưa lớn tại các tỉnh phía Bắc, đặc biệt là Quảng Ninh và Lạng"
                    " Sơn."
                ),
                "date": datetime(2019, 8, 2, tzinfo=timezone.utc),
            },
            {
                "title": "Hỗ trợ nạn nhân bão Molave",
                "description": (
                    "Một trong những cơn bão mạnh nhất năm 2020, gây thiệt hại nặng tại"
                    " miền Trung."
                ),
                "date": datetime(2020, 10, 28, tzinfo=timezone.utc),
            },
            {
                "title": "Cứu trợ sau bão Vamco",
                "description": (
                    "Gây thiệt hại lớn tại các tỉnh miền Trung, đặc biệt là Thừa"
                    " Thiên-Huế và Quảng Trị."
                ),
                "date": datetime(2020, 11, 15, tzinfo=timezone.utc),
            },
            {
                "title": "Hỗ trợ khắc phục hậu quả bão Conson",
                "description": (
                    "Gây mưa lớn tại các tỉnh miền Trung, ảnh hưởng đến đời sống người"
                    " dân."
                ),
                "date": datetime(2021, 9, 12, tzinfo=timezone.utc),
            },
            {
                "title": "Cứu trợ nạn nhân bão Kompasu",
                "description": (
                    "Gây mưa lớn và lũ lụt tại các tỉnh phía Bắc và Bắc Trung Bộ."
                ),
                "date": datetime(2021, 10, 14, tzinfo=timezone.utc),
            },
            {
                "title": "Hỗ trợ khẩn cấp sau bão Noru",
                "description": (
                    "Đổ bộ vào khu vực Đà Nẵng - Quảng Nam với sức gió mạnh, gây thiệt"
                    " hại đáng kể."
                ),
                "date": datetime(2022, 9, 28, tzinfo=timezone.utc),
            },
            {
                "title": "Cứu trợ sau bão Sonca",
                "description": (
                    "Gây mưa lớn tại các tỉnh miền Trung, đặc biệt là Thừa Thiên-Huế và"
                    " Đà Nẵng."
                ),
                "date": datetime(2023, 10, 14, tzinfo=timezone.utc),
            },
            {
                "title": "Hỗ trợ khắc phục sau bão Ma-on",
                "description": (
                    "Đổ bộ vào khu vực Quảng Ninh - Hải Phòng, gây mưa lớn và gió mạnh"
                    " tại các tỉnh phía Bắc."
                ),
                "date": datetime(2022, 8, 24, tzinfo=timezone.utc),
            },
        ]

        for storm in storm_data:
            target_amount = random.randint(100000, 1000000)
            current_amount = random.randint(0, target_amount)
            start_date = storm["date"].date()
            end_date = start_date + timedelta(days=random.randint(30, 180))
            status = "ongoing" if end_date > timezone.now().date() else "completed"

            campaign, created = Campaign.objects.get_or_create(
                title=storm["title"],
                defaults={
                    "charity_org": charity_org,
                    "description": storm["description"],
                    "start_date": start_date,
                    "end_date": end_date,
                    "target_amount": target_amount,
                    "current_amount": current_amount,
                    "status": status,
                },
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created campaign: {campaign.title}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Campaign already exists: {campaign.title}")
                )

        self.stdout.write(self.style.SUCCESS("Successfully populated campaigns"))

        all_disaster_areas = DisasterArea.objects.all()
        campaign = Campaign.objects.first()
        campaign.disaster_areas.add(*all_disaster_areas)
