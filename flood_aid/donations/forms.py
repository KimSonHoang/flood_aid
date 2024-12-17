from django import forms

from .models import Campaign, Donation, Comment


class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = [
            "title",
            "description",
            "start_date",
            "end_date",
            "target_amount",
            "status",
            "disaster_areas",
            "thumbnail",
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ["amount", "payment_method"]
        widgets = {
            "amount": forms.NumberInput(attrs={"class": "form-control"}),
            "payment_method": forms.Select(attrs={"class": "form-control"}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '3',
                'placeholder': 'Viết bình luận của bạn...'
            })
        }
