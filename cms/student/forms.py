from django import forms
from .models import Student
from .models import Result
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class StudentForm(forms.ModelForm):
    class Meta:   #it is complisory
        model = Student
        fields = ['name','birthdate','photo','department','semester','about']
        
class UserRegistertionForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User 
        fields = ('username','email','password1','password2')


class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['student', 'semester', 'department', 'subject', 'marks_obtained', 'total_marks']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'student' in self.data:
            student_id = self.data.get('student')
            student = Student.objects.get(id=student_id)
            department = student.department
            semester = int(self.data.get('semester', 0))

            # Update subject choices based on student department and semester
            if department in Result.DEPARTMENT_SUBJECTS:
                if semester in Result.DEPARTMENT_SUBJECTS[department]:
                    subjects = Result.DEPARTMENT_SUBJECTS[department][semester]
                    self.fields['subject'].choices = [(subject, subject) for subject in subjects]
                else:
                    self.fields['subject'].choices = []
            else:
                self.fields['subject'].choices = []

        else:
            self.fields['subject'].choices = []
