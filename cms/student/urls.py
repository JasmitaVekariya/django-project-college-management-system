from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('create/', views.student_create, name='student_create'),
    path('<int:student_id>/delete/', views.student_delete, name='student_delete'),
    path('<int:student_id>/edit/', views.student_edit, name='student_edit'),
    path('<int:student_id>/', views.student_profile, name='student_profile'),
    path('<int:student_id>/result/', views.student_result, name='student_result'),
    path('<int:student_id>/timetable/', views.student_timetable, name='student_timetable'),
    path('add-result/', views.add_result, name='add_result'),  # Superuser result entry
    path('<int:student_id>/result/', views.student_result, name='student_result'),  # Viewing results
    path('results/', views.results_list, name='results_list'),
    path('results/edit/<int:result_id>/', views.edit_result, name='edit_result'),
    path('results/delete/<int:result_id>/', views.delete_result, name='delete_result'),
    path('register/', views.register, name='register'),

]
