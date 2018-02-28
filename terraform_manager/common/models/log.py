from django.db import models

from common.models.environment import Environment


class Log(models.Model):
    environment = models.ForeignKey(Environment, on_delete=True)
    return_code = models.IntegerField(blank=True)
    stdout = models.TextField(blank=True)
    stderr = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)