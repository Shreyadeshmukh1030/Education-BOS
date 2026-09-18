from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Invoice, Payment
from .forms import InvoiceForm

@login_required
def dashboard(request):
    return render(request, 'finance/dashboard.html')

@login_required
def invoice_list(request):
    invoices = Invoice.objects.filter(is_active=True).select_related('person', 'fee_structure')
    return render(request, 'finance/invoice_list.html', {'invoices': invoices})

@login_required
def invoice_create(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('finance:invoice_list')
    else:
        form = InvoiceForm()
    return render(request, 'finance/invoice_form.html', {'form': form, 'title': 'Create Invoice'})

@login_required
def payment_list(request):
    payments = Payment.objects.filter(is_active=True).select_related('invoice')
    return render(request, 'finance/payment_list.html', {'payments': payments})
