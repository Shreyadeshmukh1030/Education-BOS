from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from .models import Message, Notification
from .forms import MessageForm
from apps.people.models import Person

@login_required
def dashboard(request):
    total_messages = Message.objects.filter(is_active=True).count()
    unread_messages = Message.objects.filter(is_active=True, is_read=False).count()
    total_notifications = Notification.objects.filter(is_active=True).count()
    unread_notifications = Notification.objects.filter(is_active=True, is_read=False).count()
    
    recent_messages = Message.objects.filter(is_active=True).select_related('sender', 'receiver').order_by('-created_at')[:6]
    recent_notifications = Notification.objects.filter(is_active=True).select_related('person').order_by('-created_at')[:8]
    
    # Campus Bulletin Announcements
    bulletin_announcements = [
        {
            'title': 'Diwali & Mid-Semester Recess Schedule 2026',
            'category': 'Academic Notice',
            'date': 'Oct 28 - Nov 03, 2026',
            'badge': 'Holiday',
            'summary': 'All academic sessions, practical labs, and evaluation examinations will remain suspended during the festive recess. Hostel and library facilities will operate on restricted hours.',
            'urgent': False,
        },
        {
            'title': 'Mandatory Mid-Term Exam Admit Card Verification',
            'category': 'Examinations',
            'date': 'Nov 10, 2026',
            'badge': 'Urgent',
            'summary': 'Students with attendance below 75% are instructed to report to the Dean of Academic Affairs office with supporting medical/leave documentation prior to Nov 05.',
            'urgent': True,
        },
        {
            'title': 'EduCore Smart India Hackathon & Innovation Summit',
            'category': 'Events & Placements',
            'date': 'Dec 12-14, 2026',
            'badge': 'Event',
            'summary': 'Registrations are now open for inter-departmental teams. Cash prize pool of ₹2,50,000 sponsored by tech partners. Submit project synopses by Nov 20.',
            'urgent': False,
        },
    ]

    context = {
        'total_messages': total_messages,
        'unread_messages': unread_messages,
        'total_notifications': total_notifications,
        'unread_notifications': unread_notifications,
        'recent_messages': recent_messages,
        'recent_notifications': recent_notifications,
        'bulletin_announcements': bulletin_announcements,
    }
    return render(request, 'communication/dashboard.html', context)

@login_required
def message_list(request):
    filter_tab = request.GET.get('tab', 'all')
    search_query = request.GET.get('q', '').strip()
    
    qs = Message.objects.filter(is_active=True).select_related('sender', 'receiver')
    
    if filter_tab == 'unread':
        qs = qs.filter(is_read=False)
    elif filter_tab == 'read':
        qs = qs.filter(is_read=True)
        
    if search_query:
        qs = qs.filter(
            Q(subject__icontains=search_query) |
            Q(body__icontains=search_query) |
            Q(sender__first_name__icontains=search_query) |
            Q(sender__last_name__icontains=search_query) |
            Q(receiver__first_name__icontains=search_query) |
            Q(receiver__last_name__icontains=search_query)
        )
        
    messages = qs.order_by('-created_at')
    
    context = {
        'messages': messages,
        'filter_tab': filter_tab,
        'search_query': search_query,
        'total_count': Message.objects.filter(is_active=True).count(),
        'unread_count': Message.objects.filter(is_active=True, is_read=False).count(),
    }
    return render(request, 'communication/message_list.html', context)

@login_required
def message_detail(request, pk):
    message = get_object_or_404(Message, pk=pk, is_active=True)
    if not message.is_read:
        message.is_read = True
        message.read_at = timezone.now()
        message.save()
    return render(request, 'communication/message_detail.html', {'message': message})

@login_required
def message_compose(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            # Assign sender from user person if exists, or fallback
            sender_person = Person.objects.filter(email=request.user.email).first()
            if not sender_person:
                sender_person = Person.objects.first()
            msg.sender = sender_person
            msg.save()
            return redirect('communication:message_list')
    else:
        form = MessageForm()
    return render(request, 'communication/message_form.html', {'form': form, 'title': 'Compose Internal Message'})

@login_required
def notification_list(request):
    filter_status = request.GET.get('status', 'all')
    search_query = request.GET.get('q', '').strip()
    
    qs = Notification.objects.filter(is_active=True).select_related('person')
    
    if filter_status == 'unread':
        qs = qs.filter(is_read=False)
    elif filter_status == 'read':
        qs = qs.filter(is_read=True)
        
    if search_query:
        qs = qs.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(person__first_name__icontains=search_query) |
            Q(person__last_name__icontains=search_query)
        )
        
    notifications = qs.order_by('-created_at')
    
    context = {
        'notifications': notifications,
        'filter_status': filter_status,
        'search_query': search_query,
        'total_count': Notification.objects.filter(is_active=True).count(),
        'unread_count': Notification.objects.filter(is_active=True, is_read=False).count(),
    }
    return render(request, 'communication/notification_list.html', context)

@login_required
def mark_all_notifications_read(request):
    Notification.objects.filter(is_active=True, is_read=False).update(is_read=True)
    return redirect('communication:notification_list')
