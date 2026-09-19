from .models import AuditLog

def log_audit(action, resource, resource_id="", description="", user=None, request=None):
    """
    Records an entry in the system audit log.
    Captures user, IP address, action, and details.
    """
    ip_address = None
    if request:
        if not user and request.user.is_authenticated:
            user = request.user
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0].strip()
        else:
            ip_address = request.META.get('REMOTE_ADDR')

    try:
        AuditLog.objects.create(
            user=user if user and user.is_authenticated else None,
            action=action,
            resource=resource,
            resource_id=str(resource_id),
            description=description,
            ip_address=ip_address,
        )
    except Exception as e:
        # Logging failure should not crash main transaction
        import logging
        logging.getLogger(__name__).warning(f"Failed to record audit log: {e}")
