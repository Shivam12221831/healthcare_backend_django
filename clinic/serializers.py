from rest_framework import serializers
# from .models import Patient, Doctor, PatientDoctorMap
from .models import Patient, Doctor, PatientDoctorMapping

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ["id", "name", "specialty", "email", "phone", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
    
    def validate_email(self, value):
        if Doctor.objects.filter(email=value).exists():
            raise serializers.ValidationError("A doctor with this email already exists.")
        return value

    def validate_phone(self, value):
        if Doctor.objects.filter(phone=value).exists():
            raise serializers.ValidationError("A doctor with this phone number already exists.")
        return value

class PatientSerializer(serializers.ModelSerializer):
    # created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Patient
        fields = ["id","first_name","last_name","age","gender","date_of_birth","phone","address","created_at","updated_at"]
        read_only_fields = ["id", "created_by", "created_at","updated_at"]

    def validate_age(self, value):
        if value <= 0 or value > 120:
            raise serializers.ValidationError("Age seems unrealistic.")
        return value
    def create(self, validated_data):
        # You can manually handle the `created_by` field here if needed
        created_by = validated_data.pop('created_by', None)
        patient = Patient.objects.create(**validated_data)
        if created_by:
            patient.created_by = created_by
            patient.save()
        return patient

class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDoctorMapping
        fields = ["id","patient","doctor","notes","created_at","updated_at"]
        read_only_fields = ["id","created_at","updated_at"]

    def validate(self, attrs):
        request = self.context.get("request")
        patient = attrs.get("patient")
        if request and request.user and patient and patient.created_by != request.user:
            raise serializers.ValidationError("You can only map doctors for your own patients.")
        return attrs
    def validate(self, data):
        patient = data["patient"]
        doctor = data["doctor"]
        if PatientDoctorMapping.objects.filter(patient=patient, doctor=doctor).exists():
            raise serializers.ValidationError("This doctor is already assigned to the patient.")
        return data

# class MappingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PatientDoctorMapping
#         fields = ["id","patient","doctor","notes","created_at","updated_at"]
#         read_only_fields = ["id","created_at","updated_at"]

#     def validate(self, attrs):
#         request = self.context.get("request")
#         patient = attrs.get("patient")
#         if request and request.user and patient and patient.created_by != request.user:
#             raise serializers.ValidationError("You can only map doctors for your own patients.")
#         return attrs