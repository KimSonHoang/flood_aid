from django.contrib import admin

from donations.models import Campaign, DisasterArea


@admin.register(DisasterArea)
class DisasterAreaAdmin(admin.ModelAdmin):
    list_display = ("name", "latitude", "longitude", "severity")
    list_filter = ("severity",)
    search_fields = ("name",)


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "charity_org",
        "start_date",
        "end_date",
        "status",
        "current_amount",
    )
    list_filter = ("status", "charity_org")
    search_fields = ("title", "charity_org__name")
