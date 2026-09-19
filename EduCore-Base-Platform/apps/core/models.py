import uuid
from django.db import models
from django.conf import settings

class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

class ModuleDefinition(BaseModel):
    key           = models.SlugField(unique=True)        # 'finance'
    name          = models.CharField(max_length=100)     # 'Finance & Fees'
    description   = models.TextField(blank=True)
    icon          = models.CharField(max_length=50)      # lucide icon name
    category      = models.CharField(max_length=50)      # core | academic | operations | commercial | addon
    is_core       = models.BooleanField(default=False)   # cannot be disabled
    depends_on    = models.JSONField(default=list)       # ['people','academics']
    version       = models.CharField(max_length=20, default='1.0.0')
    sort_order    = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

class OrganizationModule(BaseModel):
    organization  = models.ForeignKey('organizations.Organization', related_name='modules', on_delete=models.CASCADE)
    module        = models.ForeignKey(ModuleDefinition, on_delete=models.CASCADE)
    enabled       = models.BooleanField(default=False)
    settings      = models.JSONField(default=dict)       # per-client module config

    class Meta:
        unique_together = ('organization', 'module')
        
    def __str__(self):
        return f"{self.organization.name} - {self.module.name} ({'On' if self.enabled else 'Off'})"

class AuditLog(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_logs')
    action = models.CharField(max_length=50)  # CREATE, UPDATE, DELETE, GRADE, PAYMENT
    resource = models.CharField(max_length=100)
    resource_id = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.action}] {self.resource} by {self.user or 'System'}"

