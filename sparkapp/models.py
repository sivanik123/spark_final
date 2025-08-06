from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# Department model
class Department(models.Model):
    dept_id = models.AutoField(primary_key=True)
    dept_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.dept_name}"

# Designation model
class Designation(models.Model):
    designation_id = models.AutoField(primary_key=True)
    designation_name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.designation_name}'

class Employee(models.Model):   
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    emp_name = models.CharField(max_length=200)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    email_id = models.EmailField(unique=True)

    # Validate phone number format (example for Indian phone numbers)
    phone_validator = RegexValidator(regex=r'^\+?1?\d{9,15}$')
    phn_no = models.CharField(max_length=15, validators=[phone_validator])  # Phone number

    adhar_no = models.CharField(max_length=12, unique=True,null=True, blank=True)
    dept_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])

    DOB = models.DateField(null=True, blank=True)  # ✅ Now optional
    date_of_joining = models.DateField(null=True,blank=True)
    current_address = models.TextField(null=True,blank=True)
    residential_address = models.TextField(null=True,blank=True)
    status = models.CharField(max_length=50, choices=[('Active', 'Active'), ('Inactive', 'Inactive')],blank=True)
    designation_id = models.ForeignKey(Designation, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        designation = self.designation_id.designation_name if self.designation_id else "No Designation"
        return f'{self.emp_name} ({designation})'

# EventType model
class EventType(models.Model):
    type_id = models.AutoField(primary_key=True)
    type_description = models.CharField(max_length=1000, blank=False)

    def __str__(self):
        return self.type_description

# Venue model
class Venue(models.Model):
    venue_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    address = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.address}"
    
# Role model
class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=100)
    role_description = models.TextField()

    def __str__(self):
        return self.role_name  

# EmployeeRoleAssignment model
class EmployeeRoleAssignment(models.Model):
    MODE_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
    ]
    emp_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE)
    assigned_date = models.DateField()
    relieved_date = models.DateField(null=True, blank=True)
    document = models.FileField(upload_to="role_documents/", null=True, blank=True)
    mode = models.CharField(max_length=10, choices=MODE_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"{self.emp_id.emp_name} - {self.role_id.role_name}"
    
# Event model
class Event(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    type_id = models.ForeignKey(EventType, on_delete=models.CASCADE)
    from_date = models.DateTimeField()  # Using DateTimeField instead of DateField to allow time as well
    to_date = models.DateTimeField()    # Same as above
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('principal', 'Principal'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='teacher')

    # Fix related_name conflicts
    groups = models.ManyToManyField(Group, related_name="customuser_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions", blank=True)

class AdminEmployee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return f"{self.name} ({self.department.dept_name})"
    
class EventParticipation(models.Model):
    emp_id = models.ForeignKey('Employee', on_delete=models.CASCADE)
    event_id = models.ForeignKey('Event', on_delete=models.CASCADE)
    doc_link = models.FileField(upload_to='participation_docs/', null=True, blank=True)
    role = models.CharField(max_length=100)

    MODE_CHOICES = [
        ('Online', 'Online'),
        ('Offline', 'Offline'),
    ]
    mode = models.CharField(max_length=10, choices=MODE_CHOICES, default='online', null=True, blank=True)

    def __str__(self):
        return f"{self.emp_id.emp_name} - {self.event_id.title}"
