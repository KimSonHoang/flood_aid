from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CampaignForm, DonationForm, CommentForm
from .models import Campaign, DisasterArea, Donation, Comment


def disaster_areas(request):
    areas = DisasterArea.objects.all()
    context = {
        "areas": areas,
    }
    return render(request, "donations/disaster_areas.html", context)


def campaigns(request):
    campaigns = Campaign.objects.select_related("charity_org").all()
    return render(request, "donations/campaigns.html", {"campaigns": campaigns})


def campaign_detail(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    areas = campaign.disaster_areas.all()
    donation_form = DonationForm()
    comment_form = CommentForm()
    comments = campaign.comments.all()  # Get all comments for this campaign
    is_campaign_owner = request.user.is_authenticated and campaign.charity_org.owner.id == request.user.id

    if request.method == "POST":
        if "donation_submit" in request.POST and request.user.is_authenticated:
            donation_form = DonationForm(request.POST)
            if donation_form.is_valid():
                donation = donation_form.save(commit=False)
                donation.donor = request.user
                donation.campaign = campaign
                donation.save()

                campaign.current_amount += donation.amount
                campaign.save()

                messages.success(request, "Cảm ơn bạn vì sự đóng góp!")
                return redirect("campaign_detail", campaign_id=campaign.id)
                
        elif "comment_submit" in request.POST and request.user.is_authenticated:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.user = request.user
                comment.campaign = campaign
                comment.save()
                messages.success(request, "Bình luận của bạn đã được đăng!")
                return redirect("campaign_detail", campaign_id=campaign.id)

    context = {
        "campaign": campaign,
        "areas": areas,
        "donation_form": donation_form,
        "comment_form": comment_form,
        "comments": comments,
        "is_campaign_owner": is_campaign_owner,
    }
    return render(request, "donations/disaster_areas.html", context)


def is_charity(user):
    return user.is_authenticated and user.user_type == "charity"


@login_required
@user_passes_test(is_charity)
def manage_campaigns(request):
    campaigns = Campaign.objects.filter(charity_org=request.user.charity_organization)
    return render(request, "donations/manage_campaigns.html", {"campaigns": campaigns})


@login_required
@user_passes_test(is_charity)
def create_campaign(request):
    if request.method == "POST":
        form = CampaignForm(request.POST, request.FILES)
        if form.is_valid():
            campaign = form.save(commit=False)
            campaign.charity_org = request.user.charity_organization
            campaign.save()
            form.save_m2m()
            messages.success(request, "Chiến dịch đã được tạo thành công.")
            return redirect("manage_campaigns")
    else:
        form = CampaignForm()
    return render(
        request, "donations/campaign_form.html", {"form": form, "action": "Create"}
    )


@login_required
@user_passes_test(is_charity)
def edit_campaign(request, campaign_id):
    campaign = get_object_or_404(
        Campaign, id=campaign_id, charity_org=request.user.charity_organization
    )
    if request.method == "POST":
        form = CampaignForm(request.POST, request.FILES, instance=campaign)
        if form.is_valid():
            form.save()
            messages.success(request, "Chiến dịch đã được cập nhật thành công.")
            return redirect("manage_campaigns")
    else:
        form = CampaignForm(instance=campaign)
    return render(
        request, "donations/campaign_form.html", {"form": form, "action": "Edit"}
    )


@login_required
@user_passes_test(is_charity)
def delete_campaign(request, campaign_id):
    campaign = get_object_or_404(
        Campaign, id=campaign_id, charity_org=request.user.charity_organization
    )
    if request.method == "POST":
        campaign.delete()
        messages.success(request, "Chiến dịch đã được xóa thành công.")
        return redirect("manage_campaigns")
    return render(request, "donations/delete_campaign.html", {"campaign": campaign})


def donation_history(request):
    show_all = request.GET.get("show_all", "true").lower() == "true"

    if show_all:
        donations = Donation.objects.all().order_by("-created_at")
    else:
        donations = Donation.objects.filter(donor=request.user).order_by("-created_at")

    context = {
        "donations": donations,
        "show_all": show_all,
    }
    return render(request, "donations/donation_history.html", context)
