from django.http import HttpResponseForbidden
from .permissions import has_permission

def permission_required(perm_code):
    def decorator(view_func):
        def wrapped(request, *args, **kwargs):
            if not has_permission(request.user, perm_code):
                return HttpResponseForbidden("You do not have permission.")
            return view_func(request, *args, **kwargs)
        return wrapped
    return decorator