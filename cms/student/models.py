from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    birthdate = models.DateField()

    DEPARTMENT_CHOICE = [
        ('CE', 'Computer'),
        ('IT', 'Information Tech.'),
        ('EC', 'Electronic'),
    ]
    
    department = models.CharField(max_length=2, choices=DEPARTMENT_CHOICE)
    semester = models.DecimalField(max_digits=8, decimal_places=0)
    year = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    about = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Automatically set year based on the semester value
        if self.semester:
            if self.semester % 2 == 0:
                self.year = self.semester / 2
            else:
                self.year = (self.semester / 2) + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} - {self.department} {self.semester}'

class Result(models.Model):
    SEMESTER_CHOICES = [
        (1, 'Semester 1'),
        (2, 'Semester 2'),
        (3, 'Semester 3'),
        (4, 'Semester 4'),
        (5, 'Semester 5'),
        (6, 'Semester 6'),
        (7, 'Semester 7'),
        (8, 'Semester 8'),
    ]

    DEPARTMENT_SUBJECTS = {
        'CE': {
            1: ['Mathematics', 'BEE', 'PPS'],
            2: ['Mathematics', 'BEE', 'PPS'],
            3: ['DSA', 'JT', 'SP'],
            4: ['DSA', 'JT', 'SP'],
            5: ['Advanced DSA', 'Software Engineering', 'Compiler Design'],
            6: ['Operating Systems', 'Database Management', 'Networks'],
            7: ['Computer Graphics', 'Machine Learning', 'AI'],
            8: ['Cloud Computing', 'Cyber Security', 'Software Testing'],
        },
        'IT': {
            1: ['Mathematics', 'BEE', 'PPS'],
            2: ['Mathematics', 'BEE', 'PPS'],
            3: ['DSA', 'JT', 'SP'],
            4: ['DSA', 'JT', 'SP'],
            5: ['Advanced DSA', 'Software Engineering', 'Compiler Design'],
            6: ['Operating Systems', 'Database Management', 'Networks'],
            7: ['Computer Graphics', 'Machine Learning', 'AI'],
            8: ['Cloud Computing', 'Cyber Security', 'Software Testing'],
        },
        'EC': {
            1: ['Mathematics', 'BEE', 'PPS'],
            2: ['Mathematics', 'BEE', 'PPS'],
            3: ['DSA', 'JT', 'SP'],
            4: ['DSA', 'JT', 'SP'],
            5: ['Advanced DSA', 'Software Engineering', 'Compiler Design'],
            6: ['Operating Systems', 'Database Management', 'Networks'],
            7: ['Communication Systems', 'Signals and Systems', 'Microelectronics'],
            8: ['Digital Signal Processing', 'Embedded Systems', 'VLSI'],
        },
    }

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    total_marks = models.DecimalField(max_digits=5, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)
    semester = models.PositiveIntegerField(choices=SEMESTER_CHOICES, blank=True, null=True)
    department = models.CharField(max_length=2, choices=Student.DEPARTMENT_CHOICE, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Automatically fill department and semester based on student data
        if not self.department:
            self.department = self.student.department
        if not self.semester:
            self.semester = self.student.semester
        
        # Ensure that the department and semester match
        if self.student.department != self.department:
            raise ValueError(f"Student's department ({self.student.department}) doesn't match the provided department ({self.department})")
        
        if self.student.semester != self.semester:
            raise ValueError(f"Student's semester ({self.student.semester}) doesn't match the provided semester ({self.semester})")

        # Check if the subject is valid for this department and semester
        valid_subjects = self.DEPARTMENT_SUBJECTS.get(self.department, {}).get(self.semester, [])
        if self.subject not in valid_subjects:
            raise ValueError(f"Invalid subject for {self.department} - Semester {self.semester}. Available subjects: {', '.join(valid_subjects)}")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.name} - {self.subject} ({self.marks_obtained}/{self.total_marks})"
