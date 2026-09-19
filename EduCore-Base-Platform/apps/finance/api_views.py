from rest_framework import viewsets
from apps.core.api_views import BaseViewSet
from .models import FeeStructure, Invoice, Payment
from .serializers import FeeStructureSerializer, InvoiceSerializer, PaymentSerializer

class FeeStructureViewSet(BaseViewSet):
    queryset = FeeStructure.objects.all()
    serializer_class = FeeStructureSerializer


class InvoiceViewSet(BaseViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer


class PaymentViewSet(BaseViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
