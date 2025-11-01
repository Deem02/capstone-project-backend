from rest_framework.permissions import BasePermission

class IsAdminRole(BasePermission):
    
    def has_permission(self, request, view):
        # must be authenticated(logged in) and have an employee_profile or a superuser
        if not request.user.is_authenticated:
            return False
             
        if request.user.is_superuser:
            return True
        
        if hasattr(request.user,'employee_profile'):
            return request.user.employee_profile.role == 'ADMIN'
            
        return False
        