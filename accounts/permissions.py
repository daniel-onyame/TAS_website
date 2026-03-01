from functools import wraps
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework import status

TASUser = get_user_model()


def is_django_admin(user):
    """Check if user is a Django admin (full permissions)."""
    return user.is_superuser or user.is_staff




def is_staff(user):
    """Check if user is a staff member."""
    return user.user_type in ['staff', 'admin']


def is_instructor(user):
    """Check if user is an instructor."""
    return user.user_type == 'instructor'


def is_student(user):
    """Check if user is a student."""
    return user.user_type == 'student'


def is_tas_user(user):
    """Check if user is a TAS School Management System user."""
    return not user.is_superuser


def django_admin_required(view_func):
    """Decorator to ensure only Django admin users can access a view."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not is_django_admin(request.user):
            raise PermissionDenied("Only Django admin users can access this resource.")
        return view_func(request, *args, **kwargs)
    return wrapper




def staff_required(view_func):
    """Decorator to ensure only staff users can access a view."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not is_staff(request.user):
            raise PermissionDenied("Only staff users can access this resource.")
        return view_func(request, *args, **kwargs)
    return wrapper


def tas_user_required(view_func):
    """Decorator to ensure only TAS users can access a view."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not is_tas_user(request.user):
            raise PermissionDenied("Only TAS School Management System users can access this resource.")
        return view_func(request, *args, **kwargs)
    return wrapper


# REST Framework Permissions
class IsDjangoAdmin(BasePermission):
    """Permission class to allow only Django admin users."""
    
    def has_permission(self, request, view):
        return is_django_admin(request.user)
    
    def has_object_permission(self, request, view, obj):
        return is_django_admin(request.user)




class IsStaff(BasePermission):
    """Permission class to allow only staff users."""
    
    def has_permission(self, request, view):
        return is_staff(request.user)
    
    def has_object_permission(self, request, view, obj):
        return is_staff(request.user)


class IsInstructor(BasePermission):
    """Permission class to allow only instructor users."""
    
    def has_permission(self, request, view):
        return is_instructor(request.user)
    
    def has_object_permission(self, request, view, obj):
        return is_instructor(request.user)


class IsStudent(BasePermission):
    """Permission class to allow only student users."""
    
    def has_permission(self, request, view):
        return is_student(request.user)
    
    def has_object_permission(self, request, view, obj):
        return is_student(request.user)


class IsTASUser(BasePermission):
    """Permission class to allow only TAS users."""
    
    def has_permission(self, request, view):
        return is_tas_user(request.user)
    
    def has_object_permission(self, request, view, obj):
        return is_tas_user(request.user)


class IsTASUserOrDjangoAdmin(BasePermission):
    """Permission class to allow TAS users or Django admin users."""
    
    def has_permission(self, request, view):
        return is_tas_user(request.user) or is_django_admin(request.user)
    
    def has_object_permission(self, request, view, obj):
        return is_tas_user(request.user) or is_django_admin(request.user)


class IsStaffOrDjangoAdmin(BasePermission):
    """Permission class to allow staff or Django admin users."""
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        # Allow Django staff users, TAS staff users, TAS admin users, and Django superusers
        return (request.user.is_staff or 
                request.user.is_superuser or 
                is_staff(request.user) or 
                is_django_admin(request.user) or
                getattr(request.user, 'user_type', None) in ['staff', 'admin'])
    
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        # Allow Django staff users, TAS staff users, TAS admin users, and Django superusers
        return (request.user.is_staff or 
                request.user.is_superuser or 
                is_staff(request.user) or 
                is_django_admin(request.user) or
                getattr(request.user, 'user_type', None) in ['staff', 'admin'])




class IsStudentOrInstructorOrStaffOrDjangoAdmin(BasePermission):
    """Permission class to allow students, instructors, staff, or Django admin users."""
    
    def has_permission(self, request, view):
        return (is_student(request.user) or is_instructor(request.user) or 
                is_staff(request.user) or is_django_admin(request.user))
    
    def has_object_permission(self, request, view, obj):
        return (is_student(request.user) or is_instructor(request.user) or 
                is_staff(request.user) or is_django_admin(request.user))


class TASUserPermissionMixin:
    """Mixin to add TAS user permission checks to views."""
    
    def get_permissions(self):
        """Return permissions based on the action."""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Only Django admins can modify
            permission_classes = [IsDjangoAdmin]
        else:
            # TAS users can view
            permission_classes = [IsTASUserOrDjangoAdmin]
        return [permission() for permission in permission_classes]


class StaffPermissionMixin:
    """Mixin to add staff permission checks to views."""
    
    def get_permissions(self):
        """Return permissions based on the action."""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Staff or Django admins can modify
            permission_classes = [IsStaffOrDjangoAdmin]
        else:
            # Staff or Django admins can view
            permission_classes = [IsStaffOrDjangoAdmin]
        return [permission() for permission in permission_classes]


def get_user_type_display(user):
    """Get the display name for the user type."""
    if is_django_admin(user):
        return "Django Admin"
    elif is_staff(user):
        return "Staff"
    elif is_instructor(user):
        return "Instructor"
    elif is_student(user):
        return "Student"
    elif is_tas_user(user):
        return user.get_user_type_display()
    else:
        return "Unknown"


def get_user_permissions_level(user):
    """Get the permissions level for a user."""
    if is_django_admin(user):
        return "full"
    elif is_staff(user):
        return "staff"
    elif is_instructor(user):
        return "instructor"
    elif is_student(user):
        return "student"
    else:
        return "none"


def can_manage_students(user):
    """Check if user can manage students (staff, Django admin)."""
    return is_staff(user) or is_django_admin(user)


def can_manage_instructors(user):
    """Check if user can manage instructors (staff, Django admin)."""
    return is_staff(user) or is_django_admin(user)


def can_manage_reports(user):
    """Check if user can manage reports (staff, Django admin)."""
    return is_staff(user) or is_django_admin(user)


def can_assign_instructors(user):
    """Check if user can assign instructors to courses (staff, Django admin)."""
    return is_staff(user) or is_django_admin(user) 