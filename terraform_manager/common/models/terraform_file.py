from django.db import models


class TerraformFile(models.Model):
    body = models.TextField()
