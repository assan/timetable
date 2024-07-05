# templates/models.py

from django.db import models
class Subject(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name
class Teacher(models.Model):
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, default=1)
    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=50)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE)
    free_time = models.CharField(max_length=100)

    DAY_OF_WEEK_CHOICES = (
        (0, 'Понедельник'),
        (1, 'Вторник'),
        (2, 'Среда'),
        (3, 'Четверг'),
        (4, 'Пятница'),
        (5, 'Суббота'),
        (6, 'Воскресенье'),
    )

    day_of_week = models.IntegerField(choices=DAY_OF_WEEK_CHOICES,default = 0)

    def get_day_of_week_display(self):
        return dict(self.DAY_OF_WEEK_CHOICES)[self.day_of_week]
    def __str__(self):
        return self.name

class TimeSlot(models.Model):
    start_time = models.CharField(max_length=20)
    end_time = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"

class Availability(models.Model):
    DAYS_OF_WEEK = (
        (0, 'Понедельник'),
        (1, 'Вторник'),
        (2, 'Среда'),
        (3, 'Четверг'),
        (4, 'Пятница'),
        (5, 'Суббота'),
        (6, 'Воскресенье'),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE,default=1)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    subject= models.ForeignKey(Subject, on_delete=models.CASCADE, default=1)
    available = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student} - {self.get_day_of_week_display()} - {self.time_slot} - {'Available' if self.available else 'Not Available'}"

class Lesson(models.Model):
    DAYS_OF_WEEK = (
        (0, 'Понедельник'),
        (1, 'Вторник'),
        (2, 'Среда'),
        (3, 'Четверг'),
        (4, 'Пятница'),
        (5, 'Суббота'),
        (6, 'Воскресенье'),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.teacher} - {self.get_day_of_week_display()} - {self.time_slot}"
