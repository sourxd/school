from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms

from users.models import User, Cgroup


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class ChClassForm(forms.Form):
    clas = forms.ModelChoiceField(queryset=Cgroup.objects.all(), label='Выберите класс')

    class Meta:
        model = Cgroup
        fields = ('clas',)