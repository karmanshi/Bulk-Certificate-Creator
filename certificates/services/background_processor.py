import threading

from .job_processor import process_generation_job


def start_job_in_background(job_id):
    thread = threading.Thread(
        target=_process_job,
        args=(job_id,)
    )

    thread.daemon = True
    thread.start()


def _process_job(job_id):
    from ..models import GenerationJob

    try:
        job = GenerationJob.objects.get(
            id=job_id
        )

        process_generation_job(job)

    except GenerationJob.DoesNotExist:
        pass