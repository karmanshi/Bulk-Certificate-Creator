from django.db import models

# Create your models here.
class GenerationJob(models.Model):
    STATUS_CHOICES =[
        ("PENDING","Pending"),
        ("PROCESSING","Processing"),
        ("COMPLETED","Completed"),
        ("COMPLETED_WITH_ERRORS","Completed with Errors"),
        ("FAILED","Failed"),
    ]
    status = models.CharField(
        max_length=30,
        choices = STATUS_CHOICES,
        default="PENDING"
    )
    total_recipients = models.PositiveIntegerField(default=0)
    successful_count = models.PositiveIntegerField(default=0)
    failed_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add = True)
    completed_at = models.DateTimeField(null = True, blank=True)

    def __str__(self):
        return f"job {self.id} - {self.status}"

class Recipient(models.Model):
    STATUS_CHOICES = [
        ("PENDING","Pending"),
        ("PROCESSING","Processing"),
        ("COMPLETED","Completed"),
        ("COMPLETED_WITH_ERRORS","Completed with Errors"),
        ("FAILED","Failed"),
    ]

    job = models.ForeignKey(
        GenerationJob,
        on_delete = models.CASCADE,
        related_name = "recipients"
    )

    name = models.CharField(max_length=255)
    email = models.EmailField()

    status = models.CharField(
        max_length=30,
        choices = STATUS_CHOICES,
        default = "PENDING"
    )
    certificate = models.FileField(
        upload_to='certificates/',
        null = True,
        blank = True
    )
    error_message = models.TextField(
        null = True, 
        blank = True 
    )

    created_At = models.DateTimeField(auto_now_add =True)
    def __str__(self):
        return self.name

























