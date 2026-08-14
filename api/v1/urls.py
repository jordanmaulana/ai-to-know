from django.urls import path

from api.v1 import auth_api, editorial_api, payments_api, syllabus_api

urlpatterns = [
    path("auth/google/", auth_api.google, name="api-v1-auth-google"),
    path("auth/register/", auth_api.register, name="api-v1-auth-register"),
    path("auth/login/", auth_api.login, name="api-v1-auth-login"),
    path("auth/logout/", auth_api.logout, name="api-v1-logout"),
    path("auth/me/", auth_api.me, name="api-v1-me"),
    path("payments/mayar/webhook/", payments_api.webhook, name="api-v1-mayar-webhook"),
    path(
        "syllabus/subjects/",
        syllabus_api.SubjectAPI.as_view(),
        name="api-v1-subjects",
    ),
    path(
        "syllabus/subjects/<slug:slug>/",
        syllabus_api.SubjectAPI.as_view(),
        name="api-v1-subject",
    ),
    path(
        "syllabus/editorial/",
        editorial_api.EditorialAPI.as_view(),
        name="api-v1-editorial",
    ),
]
