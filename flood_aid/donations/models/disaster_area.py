from django.db import models


class DisasterArea(models.Model):
    SEVERITY_CHOICES = [
        ("low", "Thấp"),
        ("moderate", "Vừa"),
        ("high", "Cao"),
    ]

    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)

    class Meta:
        app_label = "donations"

    def __str__(self):
        return self.name
