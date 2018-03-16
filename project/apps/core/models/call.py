from django.db import models


class Call(models.Model):
    start_timestamp = models.DateTimeField()
    end_timestamp = models.DateTimeField()
    source = models.CharField(max_length=11)
    destination = models.CharField(max_length=11)
