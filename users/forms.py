import datetime

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms

from users.models import User, Cgroup, Ranks, Students, Subjects


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


class GradesForm(forms.Form):
    def __init__(self, subj, stud_list, *args, **kwargs):
        super(GradesForm, self).__init__(*args, **kwargs)
        self.fields['student'] = forms.ModelChoiceField(queryset=stud_list, label='Ученик')
        self.fields['subject'] = forms.ModelChoiceField(queryset=subj, label='Предмет')

    LIST_RANK_CHOICES = [
        (5, 5), (4, 4), (3, 3), (2, 2), (1, 1), ('Б', 'Б'), ('Н', 'Н')
    ]

    date = forms.DateField(initial=datetime.date.today, label='Дата')
    student = forms.ModelChoiceField(queryset=Students.objects.all(), label='Ученик')
    subject = forms.ModelChoiceField(queryset=Subjects.objects.all(), label='Предмет')
    rank = forms.ChoiceField(choices=LIST_RANK_CHOICES, label='Оценка')

    class Meta:
        model = Ranks
        fields = ('date', 'student', 'subject', 'rank')
