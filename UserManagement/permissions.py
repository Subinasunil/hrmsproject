from rest_framework import permissions
# 

from .models import CustomUser
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from rest_framework.permissions import BasePermission
from django_tenants.utils import tenant_context
from tenant_users.tenants.models import UserTenantPermissions

# from django.contrib.auth.models import Permission
# from django.contrib.contenttypes.models import ContentType
# from django.db.models import Q

# def get_model_permissions(model):
#     content_type = ContentType.objects.get_for_model(model)
#     permissions = Permission.objects.filter(
#         Q(content_type=content_type)
#     )
#     return permissions


class IsEssUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow is_ess users to view their own data.
    """

    def has_object_permission(self, request, view, obj):
        # Allow read permissions for all users
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed for is_ess users editing their own data
        return obj.is_ess and obj == request.user


#superuser class for permission
#important
from rest_framework.permissions import IsAdminUser
class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsSuperAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser
    
class IsSelfOrSuperAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or obj == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsOwnerOrHRAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow all read-only actions
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow HR admins to perform write actions
        return request.user.is_authenticated and request.user.is_staff
    
class BranchPermission(permissions.BasePermission):
    """
    Custom permission to only allow users with specific object-level permissions.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False
        

        # Retrieve UserTenantPermissions efficiently using `get` (if unique) or `filter`
        try:
            user_permissions = UserTenantPermissions.objects.get(profile=request.user)
        except UserTenantPermissions.DoesNotExist:
            return False

        # Check if the user's group has any of the necessary permissions (assuming Group has many-to-many relationship with Permission)
        required_permissions = ['view_brnch_mstr', 'delete_brnch_mstr', 'add_brnch_mstr', 'change_brnch_mstr']
        for permission in required_permissions:
            if permission in [p.codename for p in user_permissions.group.permissions.all()]:
                return True

        return False



    
class EmployeePermission(permissions.BasePermission):
    """
    Custom permission to allow only users with specific permissions to access employee data.
    """

    def has_permission(self, request, view):
        # Check if the user has the required permissions
        if request.user.is_authenticated:
            # Only users with 'Can CRUD Employees' permission can perform CRUD operations
            if request.method in permissions.SAFE_METHODS:
                return True  # Allow safe methods (GET, HEAD, OPTIONS)
            return request.user.has_perm('EmpManagement.can_crud_employees')
        return False  # Deny access to unauthenticated users

    def has_object_permission(self, request, view, obj):
        # Check if the user can access the specific employee object
        if request.user.is_authenticated:
            # ESS users can only access their own employee details
            if request.user.is_ess:
                return obj.created_by == request.user
            return True  # Other users can access any employee
        return False  # Deny access to unauthenticated users

class DepartmentPermission(permissions.BasePermission):
    """
    Custom permission to only allow users with specific permissions to access company API.
    """

    def has_permission(self, request, view):
        permissions_checked = [
            'OrganisationManager.view_dept_master',
            'OrganisationManager.delete_dept_master',
            'OrganisationManager.add_dept_master',
            'OrganisationManager.change_dept_master'
        ]
    
        for permission in permissions_checked:
            print(f"Checking permission {permission}: {request.user.has_perm(permission)}")

        if request.user.has_perm('OrganisationManager.view_dept_master') or \
            request.user.has_perm('OrganisationManager.delete_dept_master') or \
            request.user.has_perm('OrganisationManager.add_dept_master') or \
            request.user.has_perm('OrganisationManager.change_dept_master'):
            return True
        return False

    
class DesignationPermission(BasePermission):
    """
    Custom permission to only allow users with specific permissions to access company API.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False
        

        # Retrieve UserTenantPermissions efficiently using `get` (if unique) or `filter`
        try:
            user_permissions = UserTenantPermissions.objects.get(profile=request.user)
        except UserTenantPermissions.DoesNotExist:
            return False

        # Check if the user's group has any of the necessary permissions (assuming Group has many-to-many relationship with Permission)
        required_permissions = ['view_desgntn_master', 'delete_desgntn_master', 'add_desgntn_master', 'change_desgntn_master']
        for permission in required_permissions:
            if permission in [p.codename for p in user_permissions.group.permissions.all()]:
                return True

        return False
class CategoryPermission(permissions.BasePermission):
    """
    Custom permission to only allow users with specific permissions to access company API.
    """

    def has_permission(self, request, view):
        # Check if the user has the necessary permissions
        if request.user.has_perm('OrganisationManager.view_ctgry_master') or \
           request.user.has_perm('OrganisationManager.delete_ctgry_master') or \
           request.user.has_perm('OrganisationManager.add_ctgry_master') or \
           request.user.has_perm('OrganisationManager.change_ctgry_master'):
            return True
        return False
    

class UserPermission(permissions.BasePermission):
    """
    Custom permission to only allow users with specific permissions to access company API.
    """

    def has_permission(self, request, view):
        # Check if the user has the necessary permissions
        if request.user.has_perm('UserManagement.view_user') or \
           request.user.has_perm('UserManagement.delete_user') or \
           request.user.has_perm('UserManagement.add_user') or \
           request.user.has_perm('UserManagement.change_user'):
            return True
        return False


from rest_framework import permissions

class HasSchemaAccess(permissions.BasePermission):
    """
    Custom permission to check if the user has access to the schema (company) mentioned in their profile.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Check if the request's tenant is the same as the user's company
            user_company = request.user.companies.first()  # Assuming user can belong to only one company
            if user_company:
                # Check if the user's company matches the request's tenant
                requested_tenant = getattr(request, 'tenant', None)
                return user_company == requested_tenant
        # If user is not authenticated or doesn't have access, deny permission
        return False
