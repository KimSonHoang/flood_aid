from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

from accounts.models import CharityOrganization, User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Xác nhận mật khẩu", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("email",)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Mật khẩu không khớp")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ("email", "password", "is_active", "is_admin")

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ("email", "is_admin", "is_verified", "user_type")
    list_filter = ("is_admin", "is_verified", "user_type")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_admin",)}),
        ("Profile", {"fields": ("is_verified", "user_type", "phone_number")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = ()


class CharityOrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "is_approve")
    list_filter = ("is_approve",)
    search_fields = ("name", "owner__username")
    readonly_fields = ("owner",)

    fieldsets = (
        (None, {"fields": ("name", "owner")}),
        ("Approval", {"fields": ("is_approve", "operating_license")}),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("owner",)
        return self.readonly_fields


admin.site.register(User, UserAdmin)
admin.site.register(CharityOrganization, CharityOrganizationAdmin)
admin.site.unregister(Group)
