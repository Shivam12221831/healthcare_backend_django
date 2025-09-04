# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import PatientViewSet, DoctorViewSet, MappingViewSet, DoctorsForPatientView

# router = DefaultRouter()
# router.register(r"patients", PatientViewSet, basename="patient")
# router.register(r"doctors", DoctorViewSet, basename="doctor")
# router.register(r"mappings", MappingViewSet, basename="mapping")

# urlpatterns = [
#     path("", include(router.urls)),
#     path("mappings/<uuid:patient_id>/", DoctorsForPatientView.as_view(), name="mappings-by-patient"),
# ]

from django.urls import path
from . import views

urlpatterns = [
    # Patients
    path("patients/", views.PatientListCreateView.as_view(), name="patient-list-create"),
    path("patients/<int:pk>/", views.PatientDetailView.as_view(), name="patient-detail"),

    # Doctors
    path("doctors/", views.DoctorListCreateView.as_view(), name="doctor-list-create"),
    path("doctors/<int:pk>/", views.DoctorDetailView.as_view(), name="doctor-detail"),

    # Mappings
    path("mappings/", views.PatientDoctorMappingListCreateView.as_view(), name="mapping-list-create"),
    path("mappings/<int:patient_id>/", views.PatientDoctorMappingByPatientView.as_view(), name="mapping-by-patient"),
    path("mappings/delete/<int:pk>/", views.PatientDoctorMappingDeleteView.as_view(), name="mapping-delete"),
]
