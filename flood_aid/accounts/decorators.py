from django.contrib import messages
from django.shortcuts import redirect


def verified_user_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Vui lòng đăng nhập để truy cập trang này.")
            return redirect("login")
        elif not request.user.is_verified:
            messages.error(request, "Vui lòng xác minh tài khoản của bạn để truy cập trang này.")
            request.session["user_id"] = request.user.id
            return redirect("verify_otp")
        else:
            return view_func(request, *args, **kwargs)

    return wrapper
