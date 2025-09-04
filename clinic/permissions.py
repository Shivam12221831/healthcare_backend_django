from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission to allow only the owner of a patient record to modify it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user
