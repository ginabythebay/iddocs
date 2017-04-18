from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

class EncryptedPwd(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pwd = models.CharField(max_length=255, blank=True)
