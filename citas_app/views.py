import re
from django.http import request
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import User, Appointment
import bcrypt

# Página de inicio
def index(request):
    return render(request, 'index.html')

# user/create_user
def create_user(request):
    if request.method == "POST":
        # Validation check before save in DB
        errors = User.objects.registration_validator(request.POST)
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request, value)
            return redirect('/')

        hash_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        print(hash_pw)
        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hash_pw
        )
        request.session['logged_user'] = new_user.id

        return redirect('/user/appointments')
    return redirect('/')

def login(request):
    if request.method == 'POST':
        user = User.objects.filter(email = request.POST['email'])

        if user:
            log_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), log_user.password.encode()):
                request.session['logged_user'] = log_user.id
                return redirect('/user/appointments')
        messages.error(request,'Email/password are incorrect. Please retry!')
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

def appointments(request):
    if 'logged_user' not in request.session:
        messages.error(request, 'Please register or please log in first')
        return redirect('/')
    
    context = {
        'logged_user': User.objects.get(id=request.session['logged_user']),
        'all_appointments': Appointment.objects.filter(user_task_id=request.session['logged_user'])

    }
    print (context)
    return render(request,'appointments.html', context)

def add_task(request):
    if 'logged_user' not in request.session:
        messages.error(request, 'Please register or please log in first')
        return redirect('/')
    return render(request, 'add_appointments.html')

def add_appointment(request):
    if 'logged_user' not in request.session:
        messages.error(request, 'Please register or please log in first')
        return redirect('/')
    
    
    user_task = User.objects.get(id=request.session['logged_user'])
    task = request.POST.get("task")
    date = request.POST.get("date")
    status = request.POST.get("status")

    if len(task) <3:
        messages.error(request, 'Task must be at least 3 characters')
        return redirect('/user/add_task')
    if not date:
        messages.error(request, 'Invalid Date, please select a date')
        return redirect('/user/add_task')
    if status == '-1':
        messages.error(request, 'Please, select Status Option')
        return redirect('/user/add_task')

    appointment = Appointment.objects.create(task=task, date=date, status=status, user_task=user_task)

    return redirect('/user/appointments')

def delete_appointment(request, task_id):
    if 'logged_user' not in request.session:
        messages.error(request, "Please register or please log in first")
        return redirect('/')
    
    task = Appointment.objects.get(id=task_id)
    task.delete()
    return redirect('/user/appointments')
    