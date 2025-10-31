from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class Department(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

 
ROLE_CHOICES =[
    ('USER','User'),
    ('ADMIN','Admin'),
]    
class Employee(models.Model):
    user= models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='employee_profile'
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='USER' )
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, blank=True, null=True, related_name='employees')
    
    def __str__(self):
        return self.user.username
    
class Task(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    due_date = models.DateField(blank=True, null=True)
    department = models.ForeignKey(
        Department, 
        on_delete=models.SET_NULL,
        blank=True, null=True, 
        related_name='tasks')
    assignee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='tasks'
    )
    
    def __str__(self):
        return f'{self.id} - {self.title}' 