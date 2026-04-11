from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

def role_required(allowed_roles):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            raise PermissionDenied
        return wrapper
    return decorator

def admin_required(view_func):
    return role_required(['admin'])(view_func)

def receptionist_required(view_func):
    return role_required(['admin', 'receptionist'])(view_func)

def housekeeping_required(view_func):
    return role_required(['admin', 'housekeeping'])(view_func)