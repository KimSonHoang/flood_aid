from django.db import models


class CharityOrganization(models.Model):
    owner = models.ForeignKey("User", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    is_approve = models.BooleanField(default=False)
    operating_license = models.TextField(blank=True)

    def __str__(self):
        return self.name
