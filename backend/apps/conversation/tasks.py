from celery import shared_task
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import IntegrityError
from datetime import datetime

from .models import Conversation, Message

@shared_task
def process_webhook_task(event_type, data, timestamp_str=None):
    timestamp = datetime.fromisoformat(timestamp_str) if timestamp_str else timezone.now()

    if event_type == "NEW_CONVERSATION":
        Conversation.objects.get_or_create(
            id=data["id"],
            defaults={"created_at": timestamp}
        )

    elif event_type == "NEW_MESSAGE":
        conversation = get_object_or_404(Conversation, id=data.get("conversation_id"))
        if conversation.state == Conversation.State.CLOSED:
            return {"error": "Conversation is closed"}

        try:
            Message.objects.get_or_create(
                id=data["id"],
                defaults={
                    "conversation": conversation,
                    "direction": data["direction"],
                    "content": data["content"],
                    "created_at": timestamp
                }
            )
        except IntegrityError:
            return {"error": "Message with this ID already exists"}

    elif event_type == "CLOSE_CONVERSATION":
        conversation = get_object_or_404(Conversation, id=data.get("id"))
        conversation.state = Conversation.State.CLOSED
        conversation.save()