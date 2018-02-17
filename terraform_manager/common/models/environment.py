from django.db import models

from models.terraform_file import TerraformFile


class Environment(models.Model):
    terraform_file = models.OneToOneField(TerraformFile)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
