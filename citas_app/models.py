# Importa librerías
from django.db import models
import re
from django.db.models.base import Model

# Validations
#=================== UserManager=====================
# Valida caracteres y/o formato para ingreso de correo
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}

        if len(postData['first_name']) < 2:
            errors['first_name'] = "Invalid first name. First Name must be at least 3 characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Invalid last name. Last Name must be at least 3 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        users_with_email = User.objects.filter(email = postData['email'])

        if len(users_with_email) >= 1:
            errors['duplicate'] = "Email already exists."
        if len(postData['password']) < 3:
            errors['password'] = "Password must be at least 3 characters."
        if postData['password'] != postData['confirm_password']:
            errors['pw_match'] = "Password must match!"
        
        return errors

#=============== AppointmentManager =================
class AppointmentManager(models.Model):
    def appointment_validator(self, postData):
        errors = {}
        if len(postData['task']) < 3:
            errors['task'] = "Task must be at least 3 characters."

# Models Creation
#=================== user ==========================
class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

#=================== usuarios ==========================
class Appointment(models.Model):
    task = models.CharField(max_length=250)
    date = models.DateTimeField()
    status = models.CharField(max_length=50)
    user_task = models.ForeignKey(User, related_name='user_tasks',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AppointmentManager()
#=======================================================
