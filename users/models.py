from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    
    network = models.ManyToManyField("self")
    network_requests = models.ManyToManyField("self")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    debt = models.BigIntegerField(default=0)
    owed = models.BigIntegerField(default=0)

    def __str__(self):
        return self.user.username

    def add_to_network(self, user2):
        user2 = User.objects.get(username=user2)
        self.network.add(user2)
        self.network_requests.remove(user2)

    def request_network(self, user2):
        """
        user2: user username
        """
        user2 = User.objects.get(username=user2)
        self.network_requests.add(user2.profile)



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):

    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

