import uuid
from django.db import models

class Conversation(models.Model):
    class State(models.TextChoices):
        OPEN = "OPEN", "Open"
        CLOSED = "CLOSED", "Closed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    state = models.CharField(max_length=6, choices=State.choices, default=State.OPEN)
    created_at = models.DateTimeField()

    def __str__(self):
        return f"Conversation {self.id} ({self.state})"


class Message(models.Model):
    class Direction(models.TextChoices):
        SENT = "SENT", "Sent"
        RECEIVED = "RECEIVED", "Received"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, related_name="messages", on_delete=models.CASCADE)
    direction = models.CharField(max_length=8, choices=Direction.choices)
    content = models.TextField()
    created_at = models.DateTimeField()

    def __str__(self):
        return f"Message {self.id} ({self.direction})"