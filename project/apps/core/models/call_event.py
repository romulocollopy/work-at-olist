from django.db import models


class StoredCallEvent(models.Model):
    timestamp = models.DateTimeField()
    call_id = models.IntegerField()
    source = models.CharField(max_length=11)
    destination = models.CharField(max_length=11)
    type = models.CharField(max_length=10)
