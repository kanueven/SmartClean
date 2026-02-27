from rest_framework.permissions import BasePermission


class IsAdminGroup(BasePermission):
    """User belongs to the 'admin' group."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and \
               request.user.groups.filter(name='admin').exists()


class IsCleanerGroup(BasePermission):
    """User belongs to the 'cleaner' group."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and \
               request.user.groups.filter(name='cleaner').exists()


class IsOwnerOrAdmin(BasePermission):
    """Object-level: owner of the cleaner profile or admin group member."""

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Admin group can do anything
        if request.user.is_superuser or request.user.groups.filter(name='admin').exists():
            return True
        # Cleaner can only touch their own profile
        return obj.user == request.user