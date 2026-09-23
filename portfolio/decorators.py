from functools import wraps

from django.core.exceptions import PermissionDenied

def superuser_required(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            raise PermissionDenied("Superuser access is required.")
        return view_func(request, *args, **kwargs)

    return wrapped_view