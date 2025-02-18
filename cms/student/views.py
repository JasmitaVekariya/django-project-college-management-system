from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Result, Student
from .forms import ResultForm, StudentForm
from .forms import UserRegistertionForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required ,user_passes_test
from django.contrib.auth import login
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from collections import UserDict

# Create your views here.


def student_list(request):
    if request.user.is_superuser:
        students = Student.objects.all()  # Superuser sees all students
    else:
        students = Student.objects.filter(user=request.user)  # Regular user sees only their profile

    return render(request, 'student_list.html', {'students': students})

@login_required
def student_create(request):
    # Check if the user is a superuser
    if request.user.is_superuser:
        # Superuser can create any number of student profiles
        if request.method == "POST":
            form = StudentForm(request.POST, request.FILES)
            if form.is_valid():
                student = form.save(commit=False)
                student.user = request.user  # Assign the superuser as the creator
                student.save()
                return redirect('student_profile')
        else:
            form = StudentForm()

    else:
        # Normal user flow: Check if a student profile already exists with the same name
        student_name = request.POST.get('name', None)  # Get the student name from the form
        if student_name:
            existing_student = Student.objects.filter(name=student_name).first()

            if existing_student:
                # If the profile exists, show the profile or redirect to the profile page
                return redirect('student_profile')  # Redirect to the user's profile page

        if request.method == "POST":
            form = StudentForm(request.POST, request.FILES)
            if form.is_valid():
                # Create the student profile and assign the user
                student = form.save(commit=False)
                student.user = request.user  # Assign the logged-in user as the student
                student.save()
                return redirect('student_list')
        else:
            form = StudentForm()

    return render(request, 'student_form.html', {'form': form})

@login_required
def student_edit(request, student_id):
    student = get_object_or_404(Student, pk=student_id)

    # Only allow the student themselves or a superuser to edit
    if student.user != request.user and not request.user.is_superuser:
        return redirect('student_list')  # Redirect if unauthorized

    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            student = form.save(commit=False)
            student.user = request.user
            student.save()
            return redirect('student_profile', student_id=student.id)
    else:
        form = StudentForm(instance=student)

    return render(request, 'student_form.html', {'form': form})

@login_required
def student_delete(request, student_id):
    student = get_object_or_404(Student, pk=student_id)

    # Check if the user is an admin
    if not request.user.is_superuser:
        return redirect('student_list')  # Redirect if not admin

    if request.method == "POST":
        student.delete()
        return redirect('student_list')

    return render(request, 'student_confirm_delete.html', {'student': student})

def register(request):
    if request.method == "POST":
        form = UserRegistertionForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request , user)
            return redirect('student_list')
    else :
        form = UserRegistertionForm()
    return render(request , 'registration/register.html' , {'form' : form})


def generate_unique_username(name):
    base_username = name.lower().replace(" ", "_")  # Convert to lowercase and replace spaces
    username = base_username
    counter = 1

    while UserDict.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"  # Append a number if username exists
        counter += 1

    return username

@login_required
def student_profile(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    return render(request, 'student_profile.html', {'student': student})

@login_required
def student_timetable(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    # Replace with actual logic to fetch student timetable
    timetable = []
    return render(request, 'student_timetable.html', {'student': student, 'timetable': timetable})

# Check if user is superuser
def is_superuser(user):
    return user.is_superuser

@login_required
def student_result(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    results = Result.objects.filter(student=student)
    
    total_marks_obtained = sum(result.marks_obtained for result in results)
    total_marks = sum(result.total_marks for result in results)
    percentage = (total_marks_obtained / total_marks * 100) if total_marks else 0

    return render(request, 'student_result.html', {
        'student': student,
        'results': results,
        'total_marks_obtained': total_marks_obtained,
        'total_marks': total_marks,
        'percentage': percentage
    })


@login_required
@user_passes_test(is_superuser)
def add_result(request):
    if request.method == "POST":
        form = ResultForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = ResultForm()

    return render(request, 'add_result.html', {'form': form})

# Check if the user is a superuser
def superuser_required(user):
    return user.is_authenticated and user.is_superuser

@login_required
@user_passes_test(superuser_required)
def edit_result(request, result_id):
    result = get_object_or_404(Result, id=result_id)

    if request.method == "POST":
        result.subject = request.POST.get("subject")
        result.marks_obtained = request.POST.get("marks_obtained")
        result.total_marks = request.POST.get("total_marks")
        result.save()
        return redirect('results_list')  # Redirect to result list after update

    return render(request, 'edit_result.html', {'result': result})
 
@login_required
@user_passes_test(superuser_required)
def delete_result(request, result_id):
    result = get_object_or_404(Result, id=result_id)
    result.delete()  # Delete the result
    return redirect('results_list')  # Redirect to result list after deletion

def results_list(request):
    if request.user.is_superuser:
        results = Result.objects.all()
    else:
        results = Result.objects.filter(student__user=request.user)  # Assuming the student model has a 'user' field
    return render(request, 'results_list.html', {'results': results})
