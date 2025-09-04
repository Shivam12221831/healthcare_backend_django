from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Patient, Doctor, PatientDoctorMapping
from .serializers import PatientSerializer, DoctorSerializer, PatientDoctorMappingSerializer
from .permissions import IsOwner
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.models import User

class PatientListCreateView(generics.ListCreateAPIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Patient.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        print("Request user:", self.request.user)
        user = User.objects.get(email=self.request.user.email)
        # Ensure that the `created_by` field is assigned to the authenticated user
        if self.request.user.is_authenticated:
            try:
                # Try saving the patient and print the instance after saving
                patient = serializer.save(created_by=user)
                print("Patient saved:", patient)
            except Exception as e:
                # Catch and print any exceptions that occur during save
                print("Error saving patient:", e)
                raise e  # Re-raise the error so the system still catches it and handles it
        else:
            raise PermissionDenied("Authentication required.")

        
class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Patient.objects.filter(created_by=self.request.user)

class DoctorListCreateView(generics.ListCreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]


class DoctorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]

class PatientDoctorMappingListCreateView(generics.ListCreateAPIView):
    queryset = PatientDoctorMapping.objects.all()
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [permissions.IsAuthenticated]


class PatientDoctorMappingByPatientView(generics.ListAPIView):
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PatientDoctorMapping.objects.filter(patient_id=self.kwargs["patient_id"])


class PatientDoctorMappingDeleteView(generics.DestroyAPIView):
    queryset = PatientDoctorMapping.objects.all()
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        """
        Override the perform_destroy method to add custom response
        after deleting the instance.
        """
        # Perform the actual deletion of the object
        instance.delete()

    def delete(self, request, *args, **kwargs):
        """
        Override the delete method to provide a custom response
        after the object is deleted.
        """
        # Call the original delete method to delete the object
        response = super().delete(request, *args, **kwargs)

        # Return a custom success message after deletion
        return Response(
            {"detail": "Patient-Doctor mapping successfully deleted."},
            status=status.HTTP_204_NO_CONTENT
        )