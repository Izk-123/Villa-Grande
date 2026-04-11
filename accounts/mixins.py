from django.http import HttpResponseForbidden
from .permissions import has_permission

class PermissionRequiredMixin:
    """
    Mixin for Class‑Based Views that checks a permission before dispatch.
    Set `permission_required` on the view.
    """
    permission_required = None

    def dispatch(self, request, *args, **kwargs):
        if not has_permission(request.user, self.permission_required):
            return HttpResponseForbidden("You do not have permission to access this page.")
        return super().dispatch(request, *args, **kwargs)