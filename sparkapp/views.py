from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import UserForm, EmployeeForm, DepartmentForm, DesignationForm, EventTypeForm, VenueForm, RoleForm,EmployeeForm, EmployeeRoleAssignmentForm, EventForm, EventParticipationForm
from .models import Department, Designation, EventType, Role, EmployeeRoleAssignment, Event, EventParticipation
from django.contrib.auth.models import User, Group


def admin_group_required(user):
    return user.groups.filter(name='Admin').exists()

def teacher_group_required(user):
    return user.groups.filter(name='Teacher').exists()

def principal_group_required(user):
    return user.groups.filter(name='Principal').exists()


@login_required
def index(request):
    if request.user.groups.filter(name='Teacher').exists():
        return redirect('teacher_dashboard')
    elif request.user.groups.filter(name='Admin').exists():
        return redirect('admin_dashboard')
    elif request.user.groups.filter(name='Principal').exists():
        return redirect('principal_dashboard')
    else:
        return render(request, 'index.html')


# Add Employee
@login_required
def add_emp(request):
    if request.user.groups.filter(name='Teacher').exists():
        full_form = True  # Teacher gets the full form
    elif request.user.groups.filter(name='Admin').exists():
        full_form = False  # Admin gets a limited form
    else:
        return redirect('access_denied')  # Restrict other users

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        employee_form = EmployeeForm(request.POST, request.FILES) if full_form else EmployeeForm(request.POST)

        if user_form.is_valid() and employee_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])  # Set hashed password
            user.save()

            employee = employee_form.save(commit=False)
            employee.user = user
            employee.save()

            messages.success(request, 'Employee added successfully!')
            return redirect('index')
    else:
        user_form = UserForm()
        employee_form = EmployeeForm()

    return render(request, 'add_emp.html', {
        'user_form': user_form,
        'employee_form': employee_form,
        'full_form': full_form,
    })


# Department Views
@login_required
@user_passes_test(admin_group_required)
def add_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new department
            return redirect('index')
    else:
        form = DepartmentForm()
    return render(request, 'add_dept.html', {'form': form})


# Designation Views
@login_required
@user_passes_test(admin_group_required)
def manage_designation(request):
    designations = Designation.objects.all()
    return render(request, 'manage_designation.html', {'designations': designations})


# Add Designation
@login_required
@user_passes_test(admin_group_required)
def add_designation(request):
    if request.method == 'POST':
        form = DesignationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_designation')
    else:
        form = DesignationForm()
    return render(request, 'add_designation.html', {'form': form})


# Edit Designation
@login_required
@user_passes_test(admin_group_required)
def edit_designation(request, designation_id):
    designation = get_object_or_404(Designation, pk=designation_id)
    if request.method == 'POST':
        form = DesignationForm(request.POST, instance=designation)
        if form.is_valid():
            form.save()
            return redirect('manage_designation')
    else:
        form = DesignationForm(instance=designation)
    return render(request, 'edit_designation.html', {'form': form})


# Delete Designation
@login_required
@user_passes_test(admin_group_required)
def delete_designation(request, designation_id):
    designation = get_object_or_404(Designation, pk=designation_id)
    designation.delete()
    return redirect('manage_designation')


# Event Type Views
@login_required
@user_passes_test(admin_group_required)
def manage_event_type(request):
    event_types = EventType.objects.all()
    return render(request, 'manage_event_type.html', {'event_types': event_types})


# Add Event Type
@login_required
@user_passes_test(admin_group_required)
def add_event_type(request):
    if request.method == 'POST':
        form = EventTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Event Type added successfully.")
            return redirect('manage_event_type')
    else:
        form = EventTypeForm()

    return render(request, 'add_event_type.html', {'form': form})


# Edit Event Type
@login_required
@user_passes_test(admin_group_required)
def edit_event_type(request, type_id):
    event_type = get_object_or_404(EventType, type_id=type_id)
    
    # Initialize the form with the existing instance
    form = EventTypeForm(instance=event_type)

    if request.method == 'POST':
        form = EventTypeForm(request.POST, instance=event_type)
        if form.is_valid():
            form.save()
            messages.success(request, "Event Type updated successfully.")
            return redirect('manage_event_type')

    return render(request, 'edit_event_type.html', {'form': form, 'event_type': event_type})

# Delete Event Type
@login_required
@user_passes_test(admin_group_required)
def delete_event_type(request, type_id):
    event_type = get_object_or_404(EventType, type_id=type_id)
    event_type.delete()
    return redirect('manage_event_type')


# Venue Views
@login_required
@user_passes_test(admin_group_required)
def add_venue(request):
    if request.method == 'POST':
        form = VenueForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = VenueForm()
    return render(request, 'add_venue.html', {'form': form})


# Registration
def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            password = form.cleaned_data['password']  # Get password from the form
            user.set_password(password)  # Hash and set the password
            user.save()  # Save the user with the password
            login(request, user)
            messages.success(request, 'Registration successful!')

            # Redirect based on user role
            if user.is_superuser:
                return redirect('admin_dashboard')
            elif user.groups.filter(name='Teachers').exists():
                return redirect('teacher_dashboard')
            elif user.groups.filter(name='Principals').exists():
                return redirect('principal_dashboard')
            else:
                return redirect('index')
    else:
        form = UserForm()

    return render(request, 'register.html', {'form': form})


# Role Views
@login_required
@user_passes_test(admin_group_required)
def add_role(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new role
            return redirect('index')
    else:
        form = RoleForm()
    return render(request, 'add_roles.html', {'form': form})


# Employee Role Assignment Views
@login_required
@user_passes_test(teacher_group_required)
def add_role_assignment(request):
    employee = Employee.objects.get(user=request.user)  # Get logged-in employee

    if request.method == 'POST':
        form = EmployeeRoleAssignmentForm(request.POST, request.FILES, employee=employee)
        if form.is_valid():
            role_assignment = form.save(commit=False)
            role_assignment.emp_id = employee  # Assign employee automatically
            role_assignment.save()
            return redirect('index')  # Redirect after successful submission
    else:
        form = EmployeeRoleAssignmentForm(employee=employee)  # Pre-fill employee

    return render(request, 'add_role_assignment.html', {'form': form})


# Event Views
@login_required
@user_passes_test(admin_group_required)
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Event added successfully!")
            return redirect('index')
    else:
        form = EventForm()
    return render(request, 'add_event.html', {'form': form})


@login_required
@user_passes_test(teacher_group_required)

def add_event_participation(request):
    if request.method == 'POST':
        form = EventParticipationForm(request.POST, request.FILES)
        if form.is_valid():
            participation = form.save(commit=False)
            participation.emp_id = request.user.employee  # adjust this based on your setup
            participation.save()
            return redirect('teacher_dashboard')
    else:
        form = EventParticipationForm()

    return render(request, 'add_event_participation.html', {'form': form})


# Logout Views
def logout_view(request):
    logout(request)
    return redirect('logout_success')


def logout_success(request):
    return render(request, 'logout_success.html')


# Admin Dashboard View
@login_required
@user_passes_test(admin_group_required)
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')


# Teacher Dashboard View
@login_required
@user_passes_test(teacher_group_required)
def teacher_dashboard(request):
    return render(request, 'teacher_dashboard.html')


# Principal Dashboard View
@login_required
@user_passes_test(principal_group_required)
def principal_dashboard(request):
    return render(request, 'principal_dashboard.html')


# Access Denied View
@login_required
def access_denied(request):
    return render(request, 'access_denied.html')
# Manage Departments
@login_required
@user_passes_test(admin_group_required)
def manage_department(request):
    departments = Department.objects.all()
    return render(request, 'departments/manage_department.html', {'departments': departments})

# Add Department
@login_required
@user_passes_test(admin_group_required)
def add_department(request):
    form = DepartmentForm()
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_department')  # Redirect to department management page

    departments = Department.objects.all()  # Fetch all departments
    return render(request, 'departments/add_department.html', {'form': form, 'departments': departments})

# Edit Department
@login_required
@user_passes_test(admin_group_required)
def edit_department(request, dept_id):
    department = get_object_or_404(Department, dept_id=dept_id)
    
    if request.method == "POST":
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('manage_department')  # Redirect to manage_department
    
    else:
        form = DepartmentForm(instance=department)

    return render(request, 'departments/edit_department.html', {'form': form})

# Delete Department
@login_required
@user_passes_test(admin_group_required)
def delete_department(request, dept_id):
    department = get_object_or_404(Department, dept_id=dept_id)
    department.delete()
    return redirect('manage_department')  # Redirect to manage_department
@login_required
@user_passes_test(principal_group_required)
def principal_dashboard(request):
    teachers = User.objects.filter(groups__name='Teacher').select_related('employee')

    return render(request, 'principal_dashboard.html', {
        'teachers': teachers,
    })
from django.shortcuts import render, get_object_or_404
from sparkapp.models import Employee, EventParticipation, EmployeeRoleAssignment

def teacher_details(request, user_id):
    # Fetch Employee based on User ID
    employee = get_object_or_404(Employee, user__id=user_id)

    # Fetch events the teacher participated in
    event_participations = EventParticipation.objects.filter(emp_id=employee).select_related('event_id')

    # Fetch role assignments for the teacher
    role_assignments = EmployeeRoleAssignment.objects.filter(emp_id=employee).select_related('role_id')

    return render(request, 'teacher_details.html', {
        'employee': employee,
        'event_participations': event_participations,
        'role_assignments': role_assignments
    })


def manage_admin_employee(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            emp_name = form.cleaned_data["emp_name"]
            dept = form.cleaned_data["dept_id"]
            status = form.cleaned_data["status"]  # Get the status field from the form

            # Create User
            user = User.objects.create_user(username=username, email=email, password=password)

            # Create Employee
            employee = Employee.objects.create(emp_name=emp_name, email_id=email, dept_id=dept, user=user)

            # Assign Group based on Status
            if status == "Teacher" or status == "Staff":
                group_name = "Teacher"
            elif status == "Principal":
                group_name = "Principal"
            else:
                group_name = None

            # Ensure the group exists or create it
            if group_name:
                group, created = Group.objects.get_or_create(name=group_name)
                user.groups.add(group)

            return redirect("manage_admin_employee")
    
    else:
        form = EmployeeForm()

    employees = Employee.objects.select_related("dept_id").all()
    return render(request, "manage_admin_employee.html", {"form": form, "employees": employees})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Employee
from .forms import EmployeeForm,EmployeeEditForm

@login_required
def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, user__id=employee_id)

    # Ensure the logged-in user can only edit their own profile
    if request.user.id != employee.user.id:
        return redirect('home')  # Redirect to home or show an error

    if request.method == 'POST':
        form = EmployeeEditForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirect to profile page after saving
    else:
        form = EmployeeEditForm(instance=employee)

    return render(request, 'edit_employee.html', {'form': form})
