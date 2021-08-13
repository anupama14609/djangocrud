from django.db import models
from datetime import timezone

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=70)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    publish = models.BooleanField(default=True)
    timeStamp = models.DateTimeField(auto_now_add=True)
   

    def __str__(self):
        return str(self.name)