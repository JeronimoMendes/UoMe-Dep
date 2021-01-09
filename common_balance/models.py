from django.db import models

# Create your models here.
class CommonBalance(models.Model):

    user1 = models.OneToOneField(User1, on_delete=models.CASCADE)
    user2 = models.OneToOneField(User2, on_delete=models.CASCADE)
