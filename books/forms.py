import datetime

from django import forms

from books.models import Subjects, Cgroup, Students, Ranks, Daylessons


class ScheduleForm(forms.Form):
    def __init__(self, list_subj, *args, **kwargs):
        super(ScheduleForm, self).__init__(*args, **kwargs)
        self.fields['first'] = forms.ModelChoiceField(queryset=list_subj, label='1', required=False)
        self.fields['second'] = forms.ModelChoiceField(queryset=list_subj, label='2', required=False)
        self.fields['third'] = forms.ModelChoiceField(queryset=list_subj, label='3', required=False)
        self.fields['fourth'] = forms.ModelChoiceField(queryset=list_subj, label='4', required=False)
        self.fields['fifth'] = forms.ModelChoiceField(queryset=list_subj, label='5', required=False)
        self.fields['sixth'] = forms.ModelChoiceField(queryset=list_subj, label='6', required=False)

    date = forms.DateField(initial=datetime.date.today, label='Дата')
    first = forms.ModelChoiceField(queryset=Subjects.objects.all(), label='1', required=False)
    second = forms.ModelChoiceField(queryset=Subjects.objects.all(), label='2', required=False)
    third = forms.ModelChoiceField(queryset=Subjects.objects.all(), label='3', required=False)
    fourth = forms.ModelChoiceField(queryset=Subjects.objects.all(), label='4', required=False)
    fifth = forms.ModelChoiceField(queryset=Subjects.objects.all(), label='5', required=False)
    sixth = forms.ModelChoiceField(queryset=Subjects.objects.all(), label='6', required=False)

    class Meta:
        model = Daylessons
        fields = ('date', 'group', 'first', 'second', 'third', 'fourth', 'fifth', 'sixth')


class ChClassForm(forms.Form):
    id = forms.ModelChoiceField(queryset=Cgroup.objects.all().order_by('clas'), label='Выберите класс',
                                widget=forms.Select(attrs={'onchange': 'submit();'}), required=False)

    class Meta:
        model = Cgroup
        fields = ('id',)


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


class AddStudentForm(forms.Form):
    def __init__(self, class_id, *args, **kwargs):
        super(AddStudentForm, self).__init__(*args, **kwargs)
        self.fields['cgroup'] = forms.ModelChoiceField(initial=Cgroup.objects.get(id=class_id),
                                                       queryset=Cgroup.objects.all().order_by('clas'), label='Класс')

    SEX_CHOICES = (
        ('М', 'М',),
        ('Ж', 'Ж',),
    )
    first_name = forms.CharField(max_length=255, label='Имя')
    last_name = forms.CharField(max_length=255, label='Фамилия')
    sex = forms.ChoiceField(choices=SEX_CHOICES, label='Пол')
    birth_date = forms.DateField(label='Дата рождения')
    cgroup = forms.ModelChoiceField(queryset=Cgroup.objects.all().order_by('clas'), label='Класс')

    class Meta:
        model = Students
        fields = ('first_name', 'last_name', 'sex', 'birth_date', 'cgroup')
