from django.urls import path
from .views import add_emp  
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),  # Home page (this is the root URL, so it will trigger 'index' view)
    #path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', views.register, name='register'),
    path('manage-admin-employee/', views.manage_admin_employee, name='manage_admin_employee'),

    path('manage-emp/', views.add_emp, name='manage_emp'),
    path('manage-department/', views.add_department, name='manage_department'),
    path('manage-event-type/', views.manage_event_type, name='manage_event_type'),
    path('manage-venue/', views.add_venue, name='manage_venue'),
    path('manage-role/', views.add_role, name='manage_role'),
    path('manage-role-assignment/', views.add_role_assignment, name='manage_role_assignment'),
    path('manage-event/', views.add_event, name='manage_event'),
    path('manage-event-participation/', views.add_event_participation, name='manage_event_participation'),
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    #path('logout-success/', views.logout_success, name='logout_success'),
    path('add_event_type/', views.add_event_type, name='add_event_type'),
    path('edit-event-type/<int:type_id>/', views.edit_event_type, name='edit_event_type'),
    path('delete-event-type/<int:type_id>/', views.delete_event_type, name='delete_event_type'),
    path('manage-designation/', views.manage_designation, name='manage_designation'),
    path('add-designation/', views.add_designation, name='add_designation'),
    path('edit-designation/<int:designation_id>/', views.edit_designation, name='edit_designation'),
    path('delete-designation/<int:designation_id>/', views.delete_designation, name='delete_designation'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('principal-dashboard/', views.principal_dashboard, name='principal_dashboard'),
    path('access-denied/', views.access_denied, name='access_denied'),
    #path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('departments/', views.manage_department, name='manage_department'),
    path('departments/add/', views.add_department, name='add_department'),
    path('departments/edit/<int:dept_id>/', views.edit_department, name='edit_department'),
    path('departments/delete/<int:dept_id>/', views.delete_department, name='delete_department'),
    path('add-employee/', add_emp, name='add_emp'),
    path('teacher-details/<int:user_id>/', views.teacher_details, name='teacher_details'),
    path('employee/edit/<int:employee_id>/', views.edit_employee, name='edit_employee'),
        path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='registration/password_change.html',
        success_url='/password-change-done/'
    ), name='password_change'),

    path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='registration/password_change_done.html'
    ), name='password_change_done'),
]
