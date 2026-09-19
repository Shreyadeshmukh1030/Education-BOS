from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Invoice, Payment, FeeStructure
from .forms import InvoiceForm
from apps.core.permissions import (
    role_required,
    render_403,
    check_invoice_access,
    get_scoped_invoices,
    get_scoped_payments,
    ROLE_SUPER_ADMIN,
    ROLE_ORG_ADMIN,
    ROLE_ACCOUNTANT,
    ROLE_STUDENT,
    ROLE_PARENT,
)
from apps.core.audit import log_audit

@login_required
@role_required(ROLE_SUPER_ADMIN, ROLE_ORG_ADMIN, ROLE_ACCOUNTANT, ROLE_STUDENT, ROLE_PARENT)
def dashboard(request):
    return redirect('finance:invoice_list')

@login_required
@role_required(ROLE_SUPER_ADMIN, ROLE_ORG_ADMIN, ROLE_ACCOUNTANT)
def fee_list(request):
    fees = FeeStructure.objects.filter(is_active=True)
    return render(request, 'finance/fee_list.html', {'fees': fees})

@login_required
@role_required(ROLE_SUPER_ADMIN, ROLE_ORG_ADMIN, ROLE_ACCOUNTANT, ROLE_STUDENT, ROLE_PARENT)
def invoice_list(request):
    # Apply Scoped Queryset
    invoices = get_scoped_invoices(request.user).order_by('-created_at')
    return render(request, 'finance/invoice_list.html', {'invoices': invoices})

@login_required
@role_required(ROLE_SUPER_ADMIN, ROLE_ORG_ADMIN, ROLE_ACCOUNTANT)
def invoice_create(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            inv = form.save()
            log_audit(
                action="CREATE",
                resource="Invoice",
                resource_id=inv.id,
                description=f"Generated invoice #{inv.id.hex[:6]} for {inv.person} (₹{inv.amount_due})",
                request=request
            )
            return redirect('finance:invoice_list')
    else:
        form = InvoiceForm()
    return render(request, 'finance/invoice_form.html', {'form': form, 'title': 'Create Student Invoice'})

@login_required
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice.objects.select_related('person', 'fee_structure'), pk=pk)
    
    # Object-Level Scope Authorization
    if not check_invoice_access(request.user, invoice):
        return render_403(
            request,
            message="You do not have authorization to view this student invoice. It is outside your personal account or billing scope.",
            resource=f"/finance/invoices/{pk}/"
        )

    payments = Payment.objects.filter(invoice=invoice).order_by('-created_at')
    
    if request.method == 'POST':
        # Settle invoice
        amount = invoice.amount_due - invoice.amount_paid
        if amount > 0:
            ref_num = f'TXN-SIM-{invoice.id.hex[:6].upper()}'
            Payment.objects.create(
                invoice=invoice,
                amount=amount,
                method='Online',
                reference_number=ref_num
            )
            invoice.amount_paid = invoice.amount_due
            invoice.status = 'Paid'
            invoice.save()
            
            log_audit(
                action="PAYMENT",
                resource="Invoice",
                resource_id=invoice.id,
                description=f"Settled payment of ₹{amount} for invoice #{invoice.id.hex[:6]} (Ref: {ref_num})",
                request=request
            )
        return redirect('finance:invoice_detail', pk=pk)

    return render(request, 'finance/invoice_detail.html', {'invoice': invoice, 'payments': payments})

@login_required
@role_required(ROLE_SUPER_ADMIN, ROLE_ORG_ADMIN, ROLE_ACCOUNTANT, ROLE_STUDENT, ROLE_PARENT)
def payment_list(request):
    # Apply Scoped Queryset
    payments = get_scoped_payments(request.user).order_by('-created_at')
    return render(request, 'finance/payment_list.html', {'payments': payments})
