from rest_framework.permissions import BasePermission,SAFE_METHODS

class IsOwnerOrAdminOrReadOnly(BasePermission):
    """
    Allow access only to the owner of the client profile or an admin.
    """
    def has_object_permission(self, request, view, obj):
         # Safe methods (GET, HEAD, OPTIONS) allowed for all authenticated users
        if request.method in SAFE_METHODS:
            return True
        # Admin can do anything
        if request.user.is_superuser or request.user.groups.filter(name = 'admin').exists():
            return True
        # Owner can access their own profile
        return obj.user == request.user