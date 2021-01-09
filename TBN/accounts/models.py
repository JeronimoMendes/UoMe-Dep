from django.db import models

# Create your models here.
class User(models.Model):

    name = models.CharField(max_length = 50, default = None)
    email = models.EmailField(default = None)
    username = models.CharField(max_length = 150, default = None)
    debt = 0
    owed = 0
    #id = id_counter
    network = []
    User.id_counter += 1 
    User.usernames.append(username)