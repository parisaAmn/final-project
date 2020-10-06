from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
# Create your models here.

class CanvasProfile(User):
    # username = models.CharField(max_length = 150)
    # password = models.CharField(max_length = 150)
    # email = models.EmailField()
    canvasfingerprint = models.CharField(max_length=64)
    uniqueness = models.BooleanField(default = True)

    def __str__(self):
        return self.username + ' / ' + str(self.email) +' / '+ self.canvasfingerprint+' / '+str(self.uniqueness)
