import uuid

from django.db import models

from common.models.terraform_file import TerraformFile


class Environment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    terraform_file = models.ForeignKey(TerraformFile, unique=False, on_delete=True)
    state = models.CharField(max_length=20)
    locked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
