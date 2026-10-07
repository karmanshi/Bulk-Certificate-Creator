from django.urls import path

from .views import (
    DashboardView,
    GenerationJobCreateView,
    GenerationJobDetailView,
    CertificateDownloadView,
    CertificateListView
)

template_patterns=[
    path(
        "",
        DashboardView.as_view(),
        name="dashboard"
    )
]


urlpatterns = [
    path(
        "jobs/",
        GenerationJobCreateView.as_view(),
        name="generation-job-create"
    ),
    path(
        "jobs/<int:job_id>/",
        GenerationJobDetailView.as_view(),
        name="generation-job-detail"
    ),
    path(
        "certificates/<int:recipient_id>/download/",
        CertificateDownloadView.as_view(),
        name="certificate-download"
    ),
    path(
        "certificates/",
        CertificateListView.as_view(),
        name="certificate-list"
    ),
]