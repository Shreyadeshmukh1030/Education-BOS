from rest_framework import serializers
from .models import Person, StudentProfile, InstructorProfile

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'gender']

class StudentProfileSerializer(serializers.ModelSerializer):
    person = PersonSerializer()
    name = serializers.SerializerMethodField()
    program = serializers.SerializerMethodField()
    group = serializers.SerializerMethodField()
    joined = serializers.SerializerMethodField()
    
    class Meta:
        model = StudentProfile
        fields = ['id', 'student_id', 'person', 'status', 'name', 'program', 'group', 'joined']
        
    def get_name(self, obj):
        return f"{obj.person.first_name} {obj.person.last_name}"
        
    def get_program(self, obj):
        return "B.Tech Computer Science" # Mocked for now
        
    def get_group(self, obj):
        return "Batch DS-01"
        
    def get_joined(self, obj):
        return obj.admission_date.strftime("%b %Y") if obj.admission_date else "Jan 2026"
