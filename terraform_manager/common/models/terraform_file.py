import uuid

from django.db import models


class TerraformFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    body = models.TextField()
    file_name = models.CharField(max_length=200)
    variables = models.ManyToManyField('Variable', blank=True)
    provider = models.ForeignKey('Provider', on_delete=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def has_shell_script(self):
        return 0 < self.shell_script.count()

    def has_variable(self):
        return 0 < self.variables.count()
