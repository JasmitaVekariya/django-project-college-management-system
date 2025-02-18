from django.contrib import admin
from .models import Student, Result

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'department', 'semester']

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'marks_obtained', 'total_marks', 'date_added']
