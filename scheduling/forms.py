# templates/forms.py

from django import forms
from .models import *

# class AvailabilityForm(forms.ModelForm):
#     student = forms.ModelChoiceField(queryset=Student.objects.all())
#     time_slot = forms.ModelChoiceField(queryset=TimeSlot.objects.all())
#     day_of_week = forms.ChoiceField(choices=Availability.DAYS_OF_WEEK)
#     available = forms.BooleanField(required=False)
#
#     class Meta:
#         model = Availability
#         fields = ['student', 'time_slot', 'day_of_week', 'available']

class StudentForm(forms.ModelForm):
    subject = forms.ModelChoiceField(queryset=Subject.objects.all())
    teacher=forms.ModelChoiceField(queryset=Teacher.objects.all())
    day_of_week = forms.ChoiceField(choices=Student.DAY_OF_WEEK_CHOICES)
    class Meta:
        model= Student
        fields=['name','subject','teacher','day_of_week','free_time']
        labels = {'name': 'Имя',
                  'subject':'Тип коробки передач',
                  'day_of_week':'День недели',
                  'free_time':'Свобоное время',
                  'teacher':'Инструктор'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['teacher'].queryset = Teacher.objects.none()

        if 'subject' in self.data:
            try:
                subject_id = int(self.data.get('subject'))
                self.fields['teacher'].queryset = Teacher.objects.filter(subject_id=subject_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Teacher queryset
        elif self.instance.pk:
            self.fields['teacher'].queryset = self.instance.subject.teacher_set.order_by('name')
class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields=['name']
        labels={'name':'Тип трансмиссии'}
class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields=['name','subject']
        labels={'name':'Имя инструктора','subject':'Трансмиссия на учёбной машине'}
class TimeSlotForm(forms.ModelForm):
    class Meta:
        model = TimeSlot
        fields = ['start_time','end_time']
        labels={'start_time':'Время начала занятия','end_time':'Время конца занятия'}