from rest_framework import serializers
from .models import ModuleDefinition, OrganizationModule

class ModuleDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModuleDefinition
        fields = '__all__'

class OrganizationModuleSerializer(serializers.ModelSerializer):
    module_details = ModuleDefinitionSerializer(source='module', read_only=True)
    
    class Meta:
        model = OrganizationModule
        fields = '__all__'
