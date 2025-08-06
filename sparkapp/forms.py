from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import (
    Employee, Department, Designation, EventType, Venue, Role, 
    EmployeeRoleAssignment, Event, EventParticipation, AdminEmployee
)

### ---- Department & Designation Forms ---- ###
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['dept_name']
        widgets = {
            'dept_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Department Name'}),
        }

class DesignationForm(forms.ModelForm):
    class Meta:
        model = Designation
        fields = ['designation_name']
        widgets = {
            'designation_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Designation Name'}),
        }

### ---- User & Employee Forms ---- ###
class UserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'emp_name', 'profile_pic', 'email_id', 'phn_no', 'adhar_no',
            'dept_id', 'gender', 'DOB', 'date_of_joining',
            'current_address', 'residential_address', 'status', 'designation_id',
        ]
        widgets = {
            'DOB': forms.DateInput(attrs={'type': 'date'}),
            'date_of_joining': forms.DateInput(attrs={'type': 'date'}),
            'current_address': forms.Textarea(attrs={'rows': 3}),
            'residential_address': forms.Textarea(attrs={'rows': 3}),
        }

class UserEmployeeForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()

    class Meta:
        model = Employee
        fields = [
            'emp_name', 'profile_pic', 'phn_no', 'adhar_no',
            'dept_id', 'gender', 'DOB', 'date_of_joining',
            'current_address', 'residential_address', 'status', 'designation_id',
        ]

### ---- Event & Venue Forms ---- ###
class EventTypeForm(forms.ModelForm):
    type_description = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4, 'cols': 50, 'placeholder': 'Enter event type description...'
    }))

    class Meta:
        model = EventType
        fields = ['type_description']

class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ['name', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Venue Name'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Venue Address', 'rows': 3}),
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'type_id', 'from_date', 'to_date', 'venue']
        widgets = {
            'from_date': forms.DateInput(attrs={'type': 'date'}),
            'to_date': forms.DateInput(attrs={'type': 'date'}),
        }

from django import forms
from .models import EventParticipation, Employee

class EventParticipationForm(forms.ModelForm):
    class Meta:
        model = EventParticipation
        fields = ['event_id']  # Only show event and mode

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Optional: Customize dropdown if needed (e.g., filter only upcoming events)
        self.fields['event_id'].queryset = Event.objects.all()  # or your filter
        self.fields['event_id'].label = "Select Event"
        #self.fields['mode'].label = "Mode (Online/Offline)"



### ---- Role Management Forms ---- ###
class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['role_name', 'role_description']
        widgets = {
            'role_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Role Name'}),
            'role_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter Role Description'}),
        }


class EmployeeRoleAssignmentForm(forms.ModelForm):
    class Meta:
        model = EmployeeRoleAssignment
        fields = ['role_id', 'assigned_date', 'relieved_date', 'mode', 'document']
        widgets = {
            'assigned_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'relieved_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'mode': forms.Select(attrs={'class': 'form-control'}),
            'document': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, employee=None, **kwargs):
        super().__init__(*args, **kwargs)

        # Automatically set the emp_id if employee is provided
        if employee:
            self.instance.emp_id = employee


### ---- Admin Employee Form (Fixed) ---- ###
class AdminEmployeeForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = AdminEmployee
        fields = ['name', 'department', 'email']

    def save(self, commit=True):
        admin_employee = super().save(commit=False)
        user = User.objects.create_user(
            username=admin_employee.email,  
            email=admin_employee.email, 
            password=self.cleaned_data['password']
        )
        admin_employee.user = user
        if commit:
            user.save()
            admin_employee.save()
        return admin_employee
    
        dept_id = forms.ModelChoiceField(queryset=Department.objects.all(), required=True, label="Department")


from django import forms

from django import forms
from .models import Department

class EmployeeForm(forms.Form):
    EMPLOYEE_STATUS_CHOICES = [
        ('Teacher', 'Teacher'),
        ('Staff', 'Staff'),
        ('Principal', 'Principal'),
    ]
    
    emp_name = forms.CharField(label="Emp Name", max_length=100, required=True)
    email = forms.EmailField(label="Email ID", required=True, help_text="Enter a valid email address.")
    dept_id = forms.ModelChoiceField(queryset=Department.objects.all(), required=True, label="Department")
    username = forms.CharField(label="Username", max_length=100, required=True, help_text="Choose a unique username.")
    password = forms.CharField(label="Password", widget=forms.PasswordInput, required=True)
    status = forms.ChoiceField(choices=EMPLOYEE_STATUS_CHOICES, label="Status", required=True)

    # Optionally, add custom validation for the password field
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return password



from django import forms
from .models import Employee

class EmployeeEditForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'emp_name', 'profile_pic', 'email_id', 'phn_no', 
            'adhar_no', 'dept_id', 'gender', 'DOB', 'date_of_joining', 
            'current_address', 'residential_address', 'status', 'designation_id'
        ]
