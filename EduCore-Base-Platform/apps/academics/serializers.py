from rest_framework import serializers
from .models import AcademicSession, Program, AcademicTerm, Subject, SubjectOffering

class AcademicSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicSession
        fields = '__all__'


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'


class AcademicTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicTerm
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class SubjectOfferingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectOffering
        fields = '__all__'
