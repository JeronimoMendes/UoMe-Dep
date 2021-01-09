# users/forms.py
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from users.models import Profile

class CustomUserCreationForm(UserCreationForm):
    error_messages = {
        'password_mismatch': "Passwords don't match.",
    }
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email", "first_name")

class AddToNetwork(ModelForm):
    class Meta:
        model = Profile
        fields = ["network"]

