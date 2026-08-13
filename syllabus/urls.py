from django.urls import path

from syllabus import views

app_name = "cms"

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("subjects/", views.SubjectListView.as_view(), name="subjects"),
    path("subjects/new/", views.SubjectFormView.as_view(), name="subject_new"),
    path("subjects/<slug:slug>/", views.SubjectFormView.as_view(), name="subject_edit"),
    path(
        "subjects/<slug:slug>/publish/",
        views.SubjectPublishView.as_view(),
        name="subject_publish",
    ),
    path("queue/", views.QueueView.as_view(), name="queue"),
    path("editorial/", views.EditorialView.as_view(), name="editorial"),
]
