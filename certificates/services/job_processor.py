from django.utils import timezone

from ..models import GenerationJob
from .processor import process_recipient

def process_generation_job(job):
    job.status = "PROCESSING"
    job.save(update_field=["status"])

    recipients = job.recipients.all()
    for recipient in recipients:
        process_recipient(recipient)

    successful_count = job.recipients.filter(
        status="SUCCESS"
    ).count()

    failed_count = job.recipients.filter(
        status="FAILED"
    ).count()

    job.successful_count = successful_count
    job.failed_count = failed_count

    if failed_count == 0:
        job.status = "COMPLETED"
    elif successful_count > 0:
        job.status = "COMPLETED_WITH_ERRORS"
    else:
        job.status = "FAILED"

    job.completed_at = timezone.now()

    job.save(
        update_fields=[
            "status",
            "successful_count",
            "failed_count",
            "completed_at",
        ]
    )

    return job










