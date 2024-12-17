from django.db import models

from .disaster_area import DisasterArea


class Campaign(models.Model):
    STATUS_CHOICES = [
        ("ongoing", "Đang tiến hành"),
        ("completed", "Đã hoàn thành"),
    ]

    charity_org = models.ForeignKey(
        "accounts.CharityOrganization", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    disaster_areas = models.ManyToManyField(DisasterArea)
    thumbnail = models.ImageField(
        upload_to="campaign_thumbnails/", null=True, blank=True
    )

    def __str__(self):
        return self.title

    @property
    def progress_percentage(self):
        if self.target_amount > 0:
            return min(round((self.current_amount / self.target_amount) * 100), 100)
        return 0
