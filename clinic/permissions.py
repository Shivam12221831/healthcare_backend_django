# from rest_framework.permissions import BasePermission

# class IsOwnerOfPatient(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         # obj is Patient instance
#         return getattr(obj, "created_by_id", None) == getattr(request.user, "id", None)
# class IsOwnerOfMappedPatient(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         # obj is PatientDoctorMap instance
#         return getattr(obj.patient, "created_by_id", None) == getattr(request.user, "id", None)

from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission to allow only the owner of a patient record to modify it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
