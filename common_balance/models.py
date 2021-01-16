from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CommonBalance(models.Model):

    user1 = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user1")
    user2 = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user2")
    balance = models.BigIntegerField(default=0)
    owed_user1 = models.BigIntegerField(default=0)
    owed_user2 = models.BigIntegerField(default=0)

    def increase_debt(self, user):
        if user == user1:
           pass

