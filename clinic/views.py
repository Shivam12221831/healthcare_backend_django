# from rest_framework import viewsets, permissions, generics
# from django.shortcuts import get_object_or_404
# from .models import Patient, Doctor, PatientDoctorMapping
# from .serializers import PatientSerializer, DoctorSerializer, MappingSerializer
# from .permissions import IsOwnerOfPatient

# class PatientViewSet(viewsets.ModelViewSet):
#     serializer_class = PatientSerializer
#     permission_classes = [permissions.IsAuthenticated, IsOwnerOfPatient]

#     def get_queryset(self):
#         return Patient.objects.filter(created_by=self.request.user).order_by("-created_at")

# class DoctorViewSet(viewsets.ModelViewSet):
#     serializer_class = DoctorSerializer
#     queryset = Doctor.objects.all().order_by("name")

#     def get_permissions(self):
#         if self.request.method in permissions.SAFE_METHODS:
#             return [permissions.AllowAny()]
#         return [permissions.IsAuthenticated()]

# class MappingViewSet(viewsets.ModelViewSet):
#     serializer_class = MappingSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return PatientDoctorMapping.objects.filter(patient__created_by=self.request.user).select_related("patient", "doctor").order_by("-created_at")

# class DoctorsForPatientView(generics.ListAPIView):
#     serializer_class = DoctorSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         patient_id = self.kwargs["patient_id"]
#         patient = get_object_or_404(Patient, pk=patient_id, created_by=self.request.user)
#         return Doctor.objects.filter(mappings__patient=patient).distinct().order_by("name")

from rest_framework import generics, permissions
from .models import Patient, Doctor, PatientDoctorMapping
from .serializers import PatientSerializer, DoctorSerializer, PatientDoctorMappingSerializer
from .permissions import IsOwner
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.models import User

# class PatientListCreateView(generics.ListCreateAPIView):
#     serializer_class = PatientSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return Patient.objects.filter(created_by=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(created_by=self.request.user)
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
        return Patient.objects.filter(user=self.request.user)

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
