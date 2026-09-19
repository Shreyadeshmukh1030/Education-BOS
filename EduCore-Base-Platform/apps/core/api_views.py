from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

class BaseViewSet(viewsets.ModelViewSet):
    """
    Base ViewSet that provides standard custom endpoints for bulk actions, export, and import.
    """
    
    @action(detail=False, methods=['post'])
    def bulk_action(self, request):
        action_type = request.data.get('action')
        ids = request.data.get('ids', [])
        payload = request.data.get('payload', {})
        
        if not action_type or not ids:
            return Response({"error": "action and ids are required"}, status=status.HTTP_400_BAD_REQUEST)
            
        # Standard implementation for delete and status updates
        queryset = self.get_queryset().filter(id__in=ids)
        
        if action_type == 'delete':
            # Soft delete assumption
            queryset.update(is_active=False)
            return Response({"message": f"{len(ids)} items archived successfully."})
            
        elif action_type == 'change_status':
            new_status = payload.get('status')
            if new_status:
                queryset.update(status=new_status)
                return Response({"message": f"{len(ids)} items status updated to {new_status}."})
                
        return Response({"error": f"Unsupported action: {action_type}"}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['get'])
    def export(self, request):
        # Placeholder for export logic returning CSV or XLSX
        format_type = request.query_params.get('format', 'csv')
        return Response({"message": f"Export in {format_type} format successful (mocked)."})

    @action(detail=False, methods=['post'])
    def import_data(self, request):
        # Placeholder for import logic
        return Response({"message": "Data imported successfully (mocked).", "count": 0})
        
    @action(detail=False, methods=['get'])
    def stats(self, request):
        # Default stats - can be overridden by subclasses
        return Response({
            "total": self.get_queryset().count(),
            "active": self.get_queryset().filter(is_active=True).count()
        })

from .models import ModuleDefinition, OrganizationModule
from .serializers import ModuleDefinitionSerializer, OrganizationModuleSerializer

class ModuleDefinitionViewSet(BaseViewSet):
    queryset = ModuleDefinition.objects.all().order_by('sort_order')
    serializer_class = ModuleDefinitionSerializer

class OrganizationModuleViewSet(BaseViewSet):
    queryset = OrganizationModule.objects.all()
    serializer_class = OrganizationModuleSerializer

