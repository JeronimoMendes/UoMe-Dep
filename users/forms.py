# users/forms.py
from django.forms import ModelForm, CharField, DateField
from django.contrib.auth.forms import UserCreationForm
from users.models import Profile

class CustomUserCreationForm(UserCreationForm):
    error_messages = {
        'password_mismatch': "Passwords don't match.",
    }
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email", "first_name")

class AddToNetwork(ModelForm):

    bio = CharField(required=False, max_length=500, initial="bio")
    location = CharField(required=False, max_length=30, initial=" ")
    birth_date = DateField(required=False, initial=" ")

    class Meta:
        model = Profile
        fields = ["bio", "location", "birth_date"]


