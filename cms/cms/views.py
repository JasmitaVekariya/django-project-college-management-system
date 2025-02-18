from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

def index(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')  # If logged in, show index page
    else:
        return redirect('login')  # If not logged in, redirect to login page

# View for CE Department Time Table
def timetable_ce(request):
    # You can pass any data you want to render the timetable dynamically here
    # For example, you could query your database for the time table, subjects, etc.
    return render(request, 'timetable/timetable_ce.html')

# View for IT Department Time Table
def timetable_it(request):
    # Logic for fetching and rendering IT department time table
    return render(request, 'timetable/timetable_it.html')

# View for EC Department Time Table
def timetable_ec(request):
    # Logic for fetching and rendering EC department time table
    return render(request, 'timetable/timetable_ec.html')


@login_required
def custom_logout_redirect(request):
    if request.user.is_superuser:
        return redirect('index')  # Redirect superusers to index page
    else:
        return redirect('index')  # Redirect normal users to index page