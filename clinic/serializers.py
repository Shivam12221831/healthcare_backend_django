from rest_framework import serializers
from .models import Patient, Doctor, PatientDoctorMapping
from django.contrib.auth.models import User

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ["id", "name", "specialty", "email", "phone", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_email(self, value):
    # If updating, allow the same email
        doctor_id = self.instance.id if self.instance else None
        if Doctor.objects.exclude(id=doctor_id).filter(email=value).exists():
            raise serializers.ValidationError("A doctor with this email already exists.")
        return value

    def validate_phone(self, value):
        # If updating, allow the same phone number
        doctor_id = self.instance.id if self.instance else None
        if Doctor.objects.exclude(id=doctor_id).filter(phone=value).exists():
            raise serializers.ValidationError("A doctor with this phone number already exists.")
        return value
    
class PatientSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = ["id","first_name","last_name","age","gender","date_of_birth","phone","address","created_by","created_at","updated_at"]
        read_only_fields = ["id", "created_by", "created_at","updated_at"]

    def validate_age(self, value):
        if value <= 0 or value > 120:
            raise serializers.ValidationError("Age seems unrealistic.")
        return value
    
    # Custom method to get the first_name of the created_by user
    def get_created_by(self, obj):
        return obj.created_by.first_name if obj.created_by else None

class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDoctorMapping
        fields = ["id", "patient", "doctor", "notes", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate(self, data):
        request = self.context.get("request")
        patient = data.get("patient")
        doctor = data.get("doctor")

        # Check if the logged-in user is the one who created the patient
        if request and request.user and patient and patient.created_by != request.user:
            raise serializers.ValidationError("You can only map doctors for your own patients.")
        
        # Check if this patient-doctor mapping already exists
        if PatientDoctorMapping.objects.filter(patient=patient, doctor=doctor).exists():
            raise serializers.ValidationError("This doctor is already assigned to the patient.")
        
        return data