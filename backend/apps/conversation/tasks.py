from celery import shared_task
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import IntegrityError
from datetime import datetime

from .models import Conversation, Message, ConversationSummary
from .services import generate_summary

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


@shared_task
def generate_daily_summaries():
    """Executa 1x ao dia: pega últimas 50 mensagens de cada conversa e gera resumo via IA."""
    conversations = Conversation.objects.all()

    for conv in conversations:
        last_50 = conv.messages.order_by('-created_at')[:50]
        if not last_50.exists():
            continue

        # Monta texto para enviar ao LLM
        messages_text = "\n".join([f"{m.direction}: {m.content}" for m in reversed(last_50)])

        try:
            summary_text = generate_summary(messages_text)
            ConversationSummary.objects.update_or_create(
                conversation=conv,
                date=timezone.now().date(),
                defaults={"summary": summary_text},
            )
        except Exception as e:
            # log para debug
            print(f"Erro ao gerar resumo para conversa {conv.id}: {e}")