from django.db import models


class History(models.Model):

    name = models.CharField(max_length=256)
    date = models.DateField()
    value = models.FloatField()
