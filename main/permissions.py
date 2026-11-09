from rest_framework.permissions import BasePermission, DjangoModelPermissionsOrAnonReadOnly, SAFE_METHODS
from .models import Experience

# I might not use this and instead utilize DjangoModelPermissionsOrAnonReadOnly
class IsSuperUserOrReadOnly(BasePermission):
    message = "Only the portfolio owner may alter data."
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.is_superuser
        )

class ExperiencePermissions(DjangoModelPermissionsOrAnonReadOnly):
    def _queryset(self, view):
        return Experience.objects.all()
