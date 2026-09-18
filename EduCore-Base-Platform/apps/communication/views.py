from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message, Notification
from .forms import MessageForm

@login_required
def dashboard(request):
    return render(request, 'communication/dashboard.html')

@login_required
def message_list(request):
    messages = Message.objects.filter(is_active=True).select_related('sender', 'receiver')
    return render(request, 'communication/message_list.html', {'messages': messages})

@login_required
def message_compose(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            # Typically set sender based on logged-in user profile, mocked for now
            # msg.sender = request.user.person 
            form.save()
            return redirect('communication:message_list')
    else:
        form = MessageForm()
    return render(request, 'communication/message_form.html', {'form': form, 'title': 'Compose Message'})

@login_required
def notification_list(request):
    notifications = Notification.objects.filter(is_active=True).select_related('person')
    return render(request, 'communication/notification_list.html', {'notifications': notifications})
