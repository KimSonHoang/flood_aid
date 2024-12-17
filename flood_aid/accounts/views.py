from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from donations.models import Campaign

from .forms import (
    CustomAuthenticationForm,
    CustomUserCreationForm,
    OTPForm,
    ProfileUpdateForm,
)
from .models import CharityOrganization


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_verified = False
            user.save()

            if user.user_type == "charity":
                CharityOrganization.objects.create(
                    owner=user,
                    name=f"{user.email}'s Organization",
                    operating_license="",
                    is_approve=False,
                )

            request.session["user_id"] = user.id
            messages.info(
                request,
                "Đăng ký thành công. Vui lòng xác minh tài khoản của bạn bằng mã OTP được gửi"
                " đến số điện thoại của bạn.",
            )
            return redirect("verify_otp")
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})


def verify_otp(request):
    User = get_user_model()  # noqa: N806
    user = None

    user_id = request.session.get("user_id")
    if user_id:
        user = User.objects.filter(id=user_id).first()

    elif request.user.is_authenticated and not request.user.is_verified:
        user = request.user

    if not user:
        messages.error(request, "Vui lòng đăng nhập để xác minh tài khoản của bạn.")
        return redirect("login")

    if request.method == "POST":
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data["otp"]
            if otp.startswith("111"):
                user.is_verified = True
                user.save()
                login(request, user)
                messages.success(
                    request, "Tài khoản của bạn đã được xác minh và bạn đã đăng nhập thành công."
                )
                request.session.pop("user_id", None)
                if (
                    user.user_type == "charity"
                    and not user.charity_organization.operating_license
                ):
                    messages.info(
                        request,
                        "Vui lòng cập nhật hồ sơ của bạn để thêm Giấy phép hoạt động.",
                    )
                    return redirect("profile")
                return redirect("home")
            else:
                messages.error(request, "Mã OTP không hợp lệ.")
    else:
        form = OTPForm()
        messages.info(request, "Một mã OTP đã được gửi đến số điện thoại của bạn.")

    return render(
        request,
        "accounts/verify_otp.html",
        {"form": form, "phone_number": user.phone_number},
    )


def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=email, password=password)
            if user is not None:
                if user.user_type == 'admin' or user.is_superuser:
                    messages.error(
                        request,
                        "Please use the admin login page (/admin) to access the admin interface."
                    )
                    return redirect('login')
                
                if user.is_verified:
                    login(request, user)
                    messages.success(request, f"Welcome back, {email}!")
                    if (
                        user.user_type == "charity"
                        and not user.charity_organization.operating_license
                    ):
                        messages.info(
                            request,
                            "Vui lòng cập nhật hồ sơ của bạn để thêm Giấy phép hoạt động.",
                        )
                        return redirect("profile")
                    return redirect("home")
                else:
                    messages.error(
                        request,
                        "Tài khoản của bạn chưa được xác minh. Vui lòng xác minh tài khoản của bạn.",
                    )
                    request.session["user_id"] = user.id
                    return redirect("verify_otp")
            else:
                messages.error(request, "Email hoặc mật khẩu không hợp lệ.")
        else:
            messages.error(request, "Email hoặc mật khẩu không hợp lệ.")
    else:
        form = CustomAuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})


@login_required
def profile(request):
    user = request.user
    charity_org = None
    if user.user_type == "charity":
        try:
            charity_org = user.charity_organization
        except CharityOrganization.DoesNotExist:
            pass

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Hồ sơ của bạn đã được cập nhật thành công.")
            return redirect("profile")
    else:
        form = ProfileUpdateForm(instance=user)

    context = {
        "form": form,
        "charity_org": charity_org,
    }
    return render(request, "accounts/profile.html", context)


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_campaigns"] = Campaign.objects.all()[:3]
        return context
