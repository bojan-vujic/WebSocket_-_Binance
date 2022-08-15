from django.contrib.auth.models import User
from django.db import models


class Symbol(models.Model):
  user    = models.OneToOneField(User, on_delete=models.CASCADE)
  symbols = models.TextField()
  
  def __str__(self):
    return self.user.username
