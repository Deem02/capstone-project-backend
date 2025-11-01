from rest_framework import permissions

class IsAdminRole(permissions.BasePermission):
    
    def has_permission(self, request, view):
        # Custome permission must be authenticated(logged in) and have an employee_profile or a superuser
        if not request.user.is_authenticated:
            return False
             
        if request.user.is_superuser:
            return True
        
        if hasattr(request.user,'employee_profile'):
            return request.user.employee_profile.role == 'ADMIN'
            
        return False
    
class IsAdminOrAssigneeForTask(permissions.BasePermission):
    # Admin can do anything
    # assigned to (employee) can Get theit tasks, PATCH 'is_completed'
    def has_object_permission(self, request, view, obj):
        # Admin cheeck 
        is_admin = request.user.is_superuser or (hasattr(request.user,'employee_profile') and request.user.employee_profile.role == 'ADMIN')
        if is_admin:
            return True
        # Assigne cheeck
        if obj.assignee != request.user:
            return False
        # they are assinge allow safe methods 
        if request.method in permissions.SAFE_METHODS:
            return True
        # allow only for 'is_completed'
        if request.method == 'PATCH':
            return 'is_completed' in request.data and len(request.data)==1
        return False
            