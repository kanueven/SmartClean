from rest_framework.permissions import BasePermission

class IsOwnerOrAdmin(BasePermission):
    """
    Allow access only to the owner of the client profile or an admin.
    """
    def has_object_permission(self, request, view, obj):
        # Admin can do anything
        if request.user.is_staff:
            return True
        # Owner can access their own profile
        return obj.user == request.user