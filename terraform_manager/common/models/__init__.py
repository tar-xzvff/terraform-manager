from django.db import models


class Variable(models.Model):
    body = models.TextField()
