from rest_framework import serializers
from .models import GenerationJob, Recipient

class RecipientInputSerializers(serializers.Serializer):
    name = serializers.CharField(
        max_length = 255,
        allow_blank = False 
    )

    email = serializers.EmailField()

class GenerationJobSerializer(serializers.Serializer):
    recipients = RecipientInputSerializers(
        many = True 
    )

    def validate_recipients(self,recipients):
        if not recipients:
            raise serializers.ValidationError(
                "At least one recipient is required."
            )
        return recipients

class RecipientResultSerializer(serializers.ModelSerializer):
    recipient_id = serializers.IntegerField(source="id")
    certificate_url = serializers.SerializerMethodField()

    class Meta:
        model = Recipient
        fields = [
            "recipient_id",
            "name",
            "email",
            "status",
            "certificate_url",
            "error_message",
        ]

    def get_certificate_url(self, obj):
        if not obj.certificate:
            return None

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(
                obj.certificate.url
            )

        return obj.certificate.url    

class GenerationJobDetailSerializer(serializers.ModelSerializer):
    job_id = serializers.IntegerField(source="id")
    recipients = RecipientResultSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = GenerationJob
        fields = [
            "job_id",
            "status",
            "total_recipients",
            "successful_count",
            "failed_count",
            "created_at",
            "completed_at",
            "recipients",
        ]


















