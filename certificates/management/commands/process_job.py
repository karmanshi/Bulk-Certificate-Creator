from django.core.management.base import BaseCommand

from certificates.models import GenerationJob
from certificates.services.job_processor import process_generation_job


class Command(BaseCommand):

    help = "Process a certificate generation job"

    def add_arguments(self, parser):
        parser.add_argument(
            "job_id",
            type=int
        )

    def handle(self, *args, **options):
        job_id = options["job_id"]

        try:
            job = GenerationJob.objects.get(
                id=job_id
            )
        except GenerationJob.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(
                    f"Job {job_id} not found."
                )
            )
            return

        process_generation_job(job)

        self.stdout.write(
            self.style.SUCCESS(
                f"Job {job_id} processed successfully."
            )
        )