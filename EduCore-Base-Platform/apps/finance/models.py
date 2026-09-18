from django.db import models
from apps.core.models import BaseModel
from apps.people.models import Person
from apps.enrollment.models import Enrollment

class FeeStructure(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} (${self.amount})"

class Invoice(BaseModel):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Partial', 'Partially Paid'),
        ('Paid', 'Paid'),
        ('Overdue', 'Overdue'),
        ('Cancelled', 'Cancelled'),
    ]
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='invoices')
    enrollment = models.ForeignKey(Enrollment, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices')
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.SET_NULL, null=True, blank=True)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"INV-{self.id} - {self.person} ({self.status})"

    def save(self, *args, **kwargs):
        if self.amount_paid >= self.amount_due:
            self.status = 'Paid'
        elif self.amount_paid > 0 and self.status == 'Pending':
            self.status = 'Partial'
        super().save(*args, **kwargs)

class Payment(BaseModel):
    METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('Card', 'Credit/Debit Card'),
        ('Transfer', 'Bank Transfer'),
        ('Online', 'Online Gateway'),
    ]
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=50, choices=METHOD_CHOICES)
    reference_number = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"PAY-{self.id} for {self.invoice} (${self.amount})"
