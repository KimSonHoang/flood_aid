from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import CharityOrganization, User


class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    user_type = forms.ChoiceField(
        choices=User.USER_TYPE_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        fields = ("email", "phone_number", "user_type", "password1", "password2")
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "password1": forms.PasswordInput(attrs={"class": "form-control"}),
            "password2": forms.PasswordInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class OTPForm(forms.Form):
    otp = forms.CharField(
        max_length=6,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter OTP"}
        ),
    )


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={"autofocus": True, "class": "form-control"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class ProfileUpdateForm(forms.ModelForm):
    operating_license = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 5}),
        required=False,
        label="Giấy Phép Hoạt Động",
        help_text=(
            "Vui lòng cung cấp giấy phép hoạt động của bạn tại đây. (Bắt buộc đối với các tổ chức từ thiện)"
        ),
    )
    organization_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False,
        label="Tên Tổ Chức",
    )

    class Meta:
        model = User
        fields = [
            "email",
            "phone_number",
            "user_type",
            "organization_name",
            "operating_license",
        ]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "user_type": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.user_type != "charity":
            self.fields.pop("operating_license")
            self.fields.pop("organization_name")
        else:
            try:
                charity_org = self.instance.charity_organization
                self.fields["operating_license"].initial = charity_org.operating_license
                self.fields["organization_name"].initial = charity_org.name
            except CharityOrganization.DoesNotExist:
                pass

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            if user.user_type == "charity":
                charity_org, created = CharityOrganization.objects.get_or_create(
                    owner=user
                )
                charity_org.operating_license = self.cleaned_data.get(
                    "operating_license", ""
                )
                charity_org.name = self.cleaned_data.get("organization_name", "")
                charity_org.save()
        return user
