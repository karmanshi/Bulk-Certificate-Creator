from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import GenerationJob, Recipient
from .serializers import GenerationJobSerializer, GenerationJobDetailSerializer
from .services import create_generation_job, process_generation_job
from .services.background_processor import start_job_in_background
from django.http import FileResponse

class GenerationJobCreateView(APIView):
    def post(self, request):
        serializer = GenerationJobSerializer(data= request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status= status.HTTP_400_BAD_REQUEST
            )
        job = create_generation_job(
            serializer.validated_data 
        )

        ## this is if we want to run the job in request not in background
        # process_generation_job(job)
        # job.refresh_from_db()


        start_job_in_background(job.id)

        return Response(
            {
                "job_id": job.id,
                "status": job.status,
                "total_recipients": job.total_recipients,
                "successful_count": job.successful_count,
                "failed_count": job.failed_count,
            },
            status= status.HTTP_201_CREATED
        )

class GenerationJobDetailView(APIView):

    def get(self, request, job_id):
        try:
            job = GenerationJob.objects.prefetch_related(
                "recipients"
            ).get(id=job_id)

        except GenerationJob.DoesNotExist:
            return Response(
                {
                    "detail": "Job not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = GenerationJobDetailSerializer(
            job,
            context={"request": request}
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class CertificateDownloadView(APIView):

    def get(self, request, recipient_id):
        try:
            recipient = Recipient.objects.get(
                id=recipient_id
            )

        except Recipient.DoesNotExist:
            return Response(
                {
                    "detail": "Recipient not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if not recipient.certificate:
            return Response(
                {
                    "detail": "Certificate is not available."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            certificate_file = recipient.certificate.open("rb")

            return FileResponse(
                certificate_file,
                as_attachment=True,
                filename=f"certificate_{recipient.id}.pdf",
                content_type="application/pdf"
            )

        except FileNotFoundError:
            return Response(
                {
                    "detail": "Certificate file not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )    