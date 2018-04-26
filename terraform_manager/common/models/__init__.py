from django.db import models

from common.models.environment import Environment
from common.models.terraform_file import TerraformFile


class Variable(models.Model):
    key = models.CharField(max_length=100)
    value = models.TextField()

    def __str__(self):
        return '{}: {}'.format(self.key, self.value)


class Log(models.Model):
    environment = models.ForeignKey(Environment, on_delete=True)
    return_code = models.IntegerField(blank=True)
    stdout = models.TextField(blank=True)
    stderr = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ShellScript(models.Model):
    name = models.CharField(max_length=100)
    file_name = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    terraform_file = models.ForeignKey(TerraformFile, unique=False, on_delete=True)
