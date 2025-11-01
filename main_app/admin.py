from django.contrib import admin
from .models import Department, Employee, Task
# Register your models here.

admin.site.register(Department)
admin.site.register(Employee)
admin.site.register(Task)
