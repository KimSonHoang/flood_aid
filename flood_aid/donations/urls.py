from django.urls import path

from . import views

urlpatterns = [
    path("disaster-areas", views.disaster_areas, name="disaster_areas"),
    path("campaigns", views.campaigns, name="campaigns"),
    path("campaigns/<int:campaign_id>", views.campaign_detail, name="campaign_detail"),
    path("manage-campaigns", views.manage_campaigns, name="manage_campaigns"),
    path("create-campaign", views.create_campaign, name="create_campaign"),
    path("edit-campaign/<int:campaign_id>", views.edit_campaign, name="edit_campaign"),
    path(
        "delete-campaign/<int:campaign_id>",
        views.delete_campaign,
        name="delete_campaign",
    ),
    path("history/", views.donation_history, name="donation_history"),
]
