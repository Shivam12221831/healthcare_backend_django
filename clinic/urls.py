from django.urls import path
from . import views

urlpatterns = [
    # Patients
    path("patients/", views.PatientListCreateView.as_view(), name="patient-list-create"),
    path("patients/<uuid:pk>/", views.PatientDetailView.as_view(), name="patient-detail"),

    # Doctors
    path("doctors/", views.DoctorListCreateView.as_view(), name="doctor-list-create"),
    path("doctors/<uuid:pk>/", views.DoctorDetailView.as_view(), name="doctor-detail"),

    # Mappings
    path("mappings/", views.PatientDoctorMappingListCreateView.as_view(), name="mapping-list-create"),
    path("mappings/<uuid:patient_id>/", views.PatientDoctorMappingByPatientView.as_view(), name="mapping-by-patient"),
    path("mappings/delete/<uuid:pk>/", views.PatientDoctorMappingDeleteView.as_view(), name="mapping-delete"),
]
