from rest_framework import serializers
from .models import Person, StudentProfile, InstructorProfile, StaffProfile, GuardianProfile

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

class StudentProfileSerializer(serializers.ModelSerializer):
    person = PersonSerializer(read_only=True)
    name = serializers.SerializerMethodField()
    program = serializers.SerializerMethodField()
    group = serializers.SerializerMethodField()
    joined = serializers.SerializerMethodField()
    
    class Meta:
        model = StudentProfile
        fields = '__all__'
        
    def get_name(self, obj):
        return f"{obj.person.first_name} {obj.person.last_name}"
        
    def get_program(self, obj):
        enrollment = obj.person.enrollments.first() if hasattr(obj.person, 'enrollments') else None
        return enrollment.program.name if enrollment and enrollment.program else "Not Enrolled"
        
    def get_group(self, obj):
        enrollment = obj.person.enrollments.first() if hasattr(obj.person, 'enrollments') else None
        return enrollment.academic_session.name if enrollment and enrollment.academic_session else "Unassigned"
        
    def get_joined(self, obj):
        return obj.admission_date.strftime("%b %Y") if obj.admission_date else "Jan 2026"

class InstructorProfileSerializer(serializers.ModelSerializer):
    person = PersonSerializer(read_only=True)
    class Meta:
        model = InstructorProfile
        fields = '__all__'

class StaffProfileSerializer(serializers.ModelSerializer):
    person = PersonSerializer(read_only=True)
    class Meta:
        model = StaffProfile
        fields = '__all__'

class GuardianProfileSerializer(serializers.ModelSerializer):
    person = PersonSerializer(read_only=True)
    class Meta:
        model = GuardianProfile
        fields = '__all__'
