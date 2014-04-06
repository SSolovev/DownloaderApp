from django.db import models

# Create your models here.

class DownloadRequest(models.Model):
    downloaded_url=models.CharField(max_length=500)
    requester_ip = models.CharField(max_length=20)
    request_date = models.DateTimeField('requested date')