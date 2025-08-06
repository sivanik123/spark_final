from django.contrib import admin
from .models import Department, Designation, Employee,EventType,Venue,Role,EmployeeRoleAssignment, Event,EventParticipation

# Customizing the Department admin
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('dept_id', 'dept_name')  # Display fields in the admin list view
    search_fields = ('dept_name',)  # Add search functionality for department names
    ordering = ('dept_name',)  # Default ordering by department name

# Customizing the Designation admin
@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display = ('designation_id', 'designation_name')  # Display fields in the admin list view
    search_fields = ('designation_name',)  # Add search functionality for designation names
    ordering = ('designation_name',)  # Default ordering by designation name

# Customizing the Employee admin
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('emp_name', 'email_id', 'phn_no', 'adhar_no', 'dept_id', 'designation_id', 'status')  # Fields to display in the admin list view
    list_filter = ('dept_id', 'designation_id', 'status')  # Add filters for department, designation, and status
    search_fields = ('emp_name', 'email_id', 'adhar_no')  # Add search functionality for name, email, and Aadhaar
    ordering = ('emp_name',)  # Default ordering by employee name
    fieldsets = (
        ('Personal Information', {
            'fields': ('user','emp_name', 'profile_pic', 'email_id', 'phn_no', 'adhar_no', 'gender', 'DOB')
        }),
        ('Job Details', {
            'fields': ('dept_id', 'designation_id', 'date_of_joining', 'status')
        }),
        ('Address Information', {
            'fields': ('current_address', 'residential_address')
        }),
    )  # Organize fields into logical groups


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ('type_id', 'type_description')
    list_filter = ('type_description',)
    search_fields = ('type_description',)
    
@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('venue_id', 'name', 'address')  # Display fields in the admin list view
    search_fields = ('name', 'address')  # Add search functionality for venue name and address
    ordering = ('name',)  # Default ordering by venue name

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_id', 'role_name', 'role_description')  # Fields to display in the admin list view
    search_fields = ('role_name',)  # Add search functionality for role names
    ordering = ('role_name',)  # Default ordering by role name

@admin.register(EmployeeRoleAssignment)
class EmployeeRoleAssignmentAdmin(admin.ModelAdmin):
    list_display = ('emp_id', 'role_id', 'assigned_date', 'relieved_date')  # Fields to display in the admin list view
    search_fields = ('emp_id__emp_name', 'role_id__role_name')  # Search by employee name or role name
    list_filter = ('assigned_date', 'relieved_date')  # Filter options

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'type_id', 'from_date', 'to_date', 'venue')  # Columns to display in admin
    list_filter = ('type_id', 'venue')  # Add filters for type and venue
    search_fields = ('title',)  # Add search for title
    ordering = ('from_date',)  # Default ordering by start date

@admin.register(EventParticipation)
class EventParticipationAdmin(admin.ModelAdmin):
    list_display = ('emp_id', 'event_id')  # Display fields
    list_filter = ('event_id',)  # Filter by event
    search_fields = ('emp_id__emp_name', 'event_id__title')  # Search by employee name or event title