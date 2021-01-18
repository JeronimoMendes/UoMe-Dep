from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    
    network = models.ManyToManyField("self", blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    debt = models.BigIntegerField(default=0)
    owed = models.BigIntegerField(default=0)

    def __str__(self):
        return self.user.username

    def add_to_network(self, user2):
        user2 = User.objects.get(username=user2)
        FriendRequest.objects.get(to_user=self.user, from_user=user2).delete()
        self.network.add(user2.profile)

    def request_network(self, user2):
        """
        user2: user username
        """
        user2 = User.objects.get(username=user2)
        FriendRequest.objects.create(from_user=self.user, to_user=user2)

    def remove_from_network(self, user2):

        print(user2)
        self.network.remove(User.objects.get(username=user2).profile)

    def change_debt(self, value):
        self.debt += value

        self.save()

    
    def change_owed(self, value):
        self.owed += value

        self.save()


class FriendRequest(models.Model):

    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_user")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user")

    def __str__(self): return (self.from_user.username+ "_" + self.to_user.username)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):

    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

