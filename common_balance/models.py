from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CommonAccount(models.Model):

    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user1")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2")
    balance = models.BigIntegerField(default=0)

    def __str__(self): return "CB{}_{}".format(self.user1, self.user2)


    def increase_debt(self, user, value):
        user.profile.change_owed(value)
        self.other_user(user).profile.change_debt(value)

        if user == self.user1:
           self.balance += value

        else: self.balance -= value

        self.save()


    def decrease_debt(self, user, value):
        user.profile.change_owed(value)
        self.other_user(user).profile.change_debt(value)

        if user == self.user1:
           self.balance -= value

        else: self.balance += value

        self.save()


    def how_much_debt(self, user):
        if user == self.user1:
            if self.balance > 0: return 0
            return abs(self.balance)

        else: 
            if self.balance < 0: return 0
            return self.balance

    
    def how_much_owes(self, user):
        return self.how_much_debt(self.other_user(user))

    
    def other_user(self, user):
        if user == self.user1.username: return self.user2
        else: return self.user1

