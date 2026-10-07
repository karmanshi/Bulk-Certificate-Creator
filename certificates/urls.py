from django.urls import path

from .views import (
    GenerationJobCreateView,
    GenerationJobDetailView,
)


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
]