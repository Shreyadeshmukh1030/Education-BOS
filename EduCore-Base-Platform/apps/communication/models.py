from django.db import models
from apps.core.models import BaseModel
from apps.people.models import Person

class Message(BaseModel):
    sender = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=255)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"

class Notification(BaseModel):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    action_url = models.URLField(blank=True)

    def __str__(self):
        return f"Notification for {self.person}: {self.title}"
