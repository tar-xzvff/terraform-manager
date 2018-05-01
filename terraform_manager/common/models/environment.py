import uuid

from django.db import models

from common.models.terraform_file import TerraformFile


class Environment(models.Model):
    STATE_CHOICES = (
        ('IN_WAITING_FOR_START', 'IN_WAITING_FOR_START'),
        ('IN_FILE_COPYING', 'IN_FILE_COPYING'),
        ('IN_INITIALIZE', 'IN_INITIALIZE'),
        ('INITIALIZED', 'INITIALIZED'),
        ('IN_PLANNING', 'IN_PLANNING'),
        ('PLANNED', 'PLANNED'),
        ('IN_APPLYING', 'IN_APPLYING'),
        ('APPLIED', 'APPLIED'),
        ('IN_DESTROYING', 'IN_DESTROYING'),
        ('DESTROYED', 'DESTROYED'),
        ('FAILED', 'FAILED'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    terraform_file = models.ForeignKey(TerraformFile, unique=False, on_delete=True)
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='IN_WAITING_FOR_START')
    locked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
