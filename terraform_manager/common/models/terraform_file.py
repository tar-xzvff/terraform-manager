import uuid

from django.db import models


class TerraformFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    body = models.TextField()
    file_name = models.CharField(max_length=200)
    variables = models.ManyToManyField('Variable', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
