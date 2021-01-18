# users/forms.py
from django.forms import ModelForm, CharField, DateField
from django.contrib.auth.forms import UserCreationForm
from users.models import Profile

class CustomUserCreationForm(UserCreationForm):
    error_messages = {
        'password_mismatch': "Passwords don't match.",
    }
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)
