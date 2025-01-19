from django.contrib.auth.forms import UserCreationForm

from .models import User

class RegisterForm(UserCreationForm):
    class Meta:
        fields = ['email', 'username', 'password1', 'password2']
        model = User