from django.shortcuts import render

# Create your views here.
# templates/views.py

from django.shortcuts import render, redirect
from .models import *
from .forms import *
from .optimization import calculate_schedule
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.http import JsonResponse
def get_teachers(request):
    subject_id = request.GET.get('subject_id')
    teachers = Teacher.objects.filter(subject_id=subject_id).values('id', 'name')
    return JsonResponse(list(teachers), safe=False)
def calculate_schedule_view(request):
    if request.method == 'POST':
        status = calculate_schedule()
        if status:
            return redirect('schedule')
        else:
            return render(request, 'error.html', {'message': 'Unable to calculate schedule.'})
    return render(request, 'calculate_schedule.html')

def schedule_view(request):
    lessons = Lesson.objects.all()
    return render(request, 'schedule.html', {'lessons': lessons})

def update_availability_view(request):
    if request.method == 'POST':
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('schedule')
    else:
        form = AvailabilityForm()
    return render(request, 'update_availability.html', {'form': form})
#Добавление, изменение и удаление студентов
def students_view(request):
    if request.method=='POST':
        form=StudentForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            name=data.get('name')
            day_of_week= data.get('day_of_week')
            free_time=data.get('free_time')
            teacher= data.get('teacher')
            subject = data.get('subject')
            Student.objects.create(name=name, free_time=free_time, day_of_week=day_of_week, teacher=teacher, subject=subject)
        students=Student.objects.all()
        return render(request,'enter_students.html',{'form':form,'students':students})

    form=StudentForm()
    students = Student.objects.all()
    return render(request, 'enter_students.html', {'form': form, 'students': students})


# изменение данных в бд
def edit_student(request, id):
    try:
        student = Student.objects.get(id=id)

        if request.method == "POST":
            form=StudentForm(request.POST)
            if form.is_valid():
                data=form.cleaned_data
                student.name = data.get("name")
                student.save()
            return redirect("/students")
        else:
            form = StudentForm()
            students = Student.objects.all()
            return render(request, "enter_students.html",{'form':form,'students':students})
    except Student.DoesNotExist:
        return HttpResponseNotFound("<h2>Курсант не найден</h2>")

# удаление данных из бд
def delete_student(request, id):
    try:
        student = Student.objects.get(id=id)
        student.delete()
        return redirect("/students")
    except Student.DoesNotExist:
        return HttpResponseNotFound("<h2>Курсант не найден</h2>")
#==================================================================================
#Добавление, изменение и удаление предметов
def subject_view(request):
    if request.method=='POST':
        form=SubjectForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            name=data.get('name')
            Subject.objects.create(name=name)
            subjects=Subject.objects.all()
        return render(request,'enter_subjects.html',{'form':form,'subjects':subjects})
    form=SubjectForm()
    subjects = Subject.objects.all()
    return render(request, 'enter_subjects.html', {'form': form, 'subjects': subjects})


# изменение данных в бд
def edit_subject(request, id):
    try:
        subject = Subject.objects.get(id=id)

        if request.method == "POST":
            form=SubjectForm(request.POST)
            if form.is_valid():
                data=form.cleaned_data
                subject.name = data.get("name")
                subject.save()
            return redirect("/students")
        else:
            form = StudentForm()
            subjects = Subject.objects.all()
            return render(request, "enter_subjects.html",{'form':form,'subjects':subjects})
    except Subject.DoesNotExist:
        return HttpResponseNotFound("<h2>Трансмиссия не найдена</h2>")

# удаление данных из бд
def delete_subject(request, id):
    try:
        subject = Subject.objects.get(id=id)
        subject.delete()
        return redirect("/subjects")
    except Subject.DoesNotExist:
        return HttpResponseNotFound("<h2>Трансмиссия не найдена</h2>")
#==================================================================================
#Добавление, изменение и удаление инструкторов
def teacher_view(request):
    if request.method=='POST':
        form=TeacherForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            name=data.get('name')
            subject=data.get('subject')
            Teacher.objects.create(name=name,subject=subject)
            teachers=Teacher.objects.all()
        return render(request,'enter_teachers.html',{'form':form,'teachers':teachers})
    form=TeacherForm()
    teachers = Teacher.objects.all()
    return render(request, 'enter_teachers.html', {'form': form, 'teachers': teachers})


# изменение данных в бд
def edit_teacher(request, id):
    try:
        teacher = Teacher.objects.get(id=id)

        if request.method == "POST":
            form=TeacherForm(request.POST)
            if form.is_valid():
                data=form.cleaned_data
                teacher.name = data.get("name")
                teacher.subject=data.get('subject')
                teacher.save()
            return redirect("/students")
        else:
            form = TeacherForm()
            teachers = Teacher.objects.all()
            return render(request, "enter_teachers.html",{'form':form,'teachers':teachers})
    except Teacher.DoesNotExist:
        return HttpResponseNotFound("<h2>Инструктор не найден</h2>")

# удаление данных из бд
def delete_teacher(request, id):
    try:
       teacher = Teacher.objects.get(id=id)
       teacher.delete()
       return redirect("/teachers")
    except Teacher.DoesNotExist:
        return HttpResponseNotFound("<h2>Инструктор не найден</h2>")
#добавление временных отрезков (по умолчаению генерируются автоматически в optimization.py) Здесь только посмотреть на них
def time_slots_view(request):
    if request.method == 'POST':
        form = TimeSlotForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            time = data.get('time')
            TimeSlot.objects.create(time=time)
            time_slots = TimeSlot.objects.all()
        return render(request, 'enter_time_slots.html', {'form': form, 'time_slots': time_slots})
    form = TimeSlotForm()
    time_slots = TimeSlot.objects.all()
    return render(request, 'enter_time_slots.html', {'form': form, 'time_slots': time_slots})
def edit_time_slot(request, id):
    try:
        time_slot = TimeSlot.objects.get(id=id)
        if request.method == "POST":
            form=TimeSlotForm(request.POST)
            if form.is_valid():
                data=form.cleaned_data
                time_slot.time = data.get("time")
                time_slot.save()
            return redirect("/time_slots")
        else:
            form = TimeSlotForm()
            time_slots = TimeSlot.objects.all()
            return render(request, "enter_time_slots.html",{'form':form,'time_slots':time_slots})
    except TimeSlot.DoesNotExist:
        return HttpResponseNotFound("<h2>Временной отрезок не найден</h2>")

# удаление данных из бд
def delete_time_slot(request, id):
    try:
        time_slot = TimeSlot.objects.get(id=id)
        time_slot.delete()
        return redirect("/time_slots")
    except Student.DoesNotExist:
        return HttpResponseNotFound("<h2>Временной отрезок не найден</h2>")