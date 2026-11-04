from rest_framework.permissions import BasePermission, SAFE_METHODS

# I might not use this and instead utilize DjangoModelPermissionsOrAnonReadOnly
class IsSuperUserOrReadOnly(BasePermission):
    message = "Only the portfolio owner may alter data."
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.is_superuser
        )
