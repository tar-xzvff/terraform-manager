from django.db import models

from common.models.terraform_file import TerraformFile


class Environment(models.Model):
    terraform_file = models.ForeignKey(TerraformFile, unique=False, on_delete=True)
    state = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
