from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path
from django.views.generic import RedirectView

from core.views import AdminLoginView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", AdminLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    # The CMS. Its first route is "", so /dashboard/ still resolves and LOGIN_REDIRECT_URL
    # needs no change. Moving this prefix means also moving LOGIN_REDIRECT_URL, the redirect
    # below, and SuperuserRequiredMixin's login_url.
    path("dashboard/", include("syllabus.urls")),
    path("api/v1/", include("api.v1.urls")),
    path("", RedirectView.as_view(url="/dashboard/", permanent=False), name="home"),
]
