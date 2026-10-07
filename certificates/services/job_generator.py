from certificates.models import GenerationJob, Recipient

def create_generation_job(validate_data):
    recipients_data = validate_data["reccipients"]
    job = GenerationJob.objects.create(
        total_recipients = len(recipients_data)
    )

    recipients = [
        Recipient(
            job=job,
            name=recipient["name"],
            email=recipient["email"],
        )
        for recipient in recipients_data
    ]

    Recipient.objects.bulk_create(recipients)
    return job









