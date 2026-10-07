from pathlib import Path
from django.conf import settings
from django.core.files import File

from ..models import Recipient
from .certificate_generator import generate_certificate

def process_recipient(recipient):
    recipient.status = "PROCESSING"
    recipient.save(update_fields = ["status"])

    try:
        output_dir  = Path(settings.MEDIA_ROOT)/"certificates"
        output_dir.mkdir(parents=True,exist_ok = True)
        output_path = output_dir /f"certificate_{recipient.id}.pdf"

        generate_certificate(
            recipient.name,
            output_path 
        )
        with open(output_path , "rb") as certificate_file:
            recipient.certificate.save(
                f"certificate_{recipient.id}.pdf",
                File(certificate_file),
                save = False
            )

        recipient.status = "SUCCESS"
        recipient.error_message = None 

        recipient.save(
            update_fields = [
                "certificate",
                "status",
                "error_message",
            ]
        )    
        return recipient
    except Exception as exc:
        recipient.status = "FAILED"
        recipient.error_message = str(exc)    

        recipient.save(
            update_fields = [
                "status",
                "error_message",
            ]
        )
        return recipient








