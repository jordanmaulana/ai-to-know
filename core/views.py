from django.contrib.auth.views import LoginView, redirect_to_login
from django.core.exceptions import PermissionDenied


class SuperuserRequiredMixin:
    """Superuser-only pages.

    Anonymous -> /login/?next=..., signed-in non-superuser -> 403. The 403 matters: sending an
    already-authenticated user back to the login form just loops them through it again.
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path(), "/login/")
        if not request.user.is_superuser:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class AdminLoginView(LoginView):
    template_name = "registration/login.html"
