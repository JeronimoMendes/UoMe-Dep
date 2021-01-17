from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CommonBalance(models.Model):

    user1 = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user1")
    user2 = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user2")
    balance = models.BigIntegerField(default=0)

    def __str__(self): return "CB{}_{}".format(self.user1, self.user2)


    def increase_debt(self, user, value):
        if user == self.user1:
           self.balance += value

        else: self.balance -= value


    def descrease_debt(self, user, value):
        if user == self.user1:
           self.balance -= value

        else: self.balance += value


    def how_much_debt(self, user):
        if user == self.user1:
            if self.balance > 0: return 0
            return abs(self.balance)

        else: 
            if self.balance < 0: return 0
            return self.balance

    
    def other_user(self, user):
        if user == self.user1: return self.user2
        else: return self.user1

