from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(User):
    # username = models.CharField(max_length = 150)
    # password = models.CharField(max_length = 150)
    # email = models.EmailField()
    browserfingerprint = models.CharField(max_length=64)
    bf_uniquenes = models.BooleanField(default = True)

    def __str__(self):
        return self.username + ' / ' + str(self.email) +' / '+ self.browserfingerprint+' / '+str(self.bf_uniquenes)
