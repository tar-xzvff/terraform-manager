from django.db import models


class Job(models.Model):
    state = models.CharField()
