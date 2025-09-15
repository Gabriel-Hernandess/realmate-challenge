from rest_framework import serializers
from django.db.models import OuterRef, Subquery
from .models import Conversation, Message, ConversationSummary

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "direction", "content", "created_at"]

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    latest_summary = serializers.SerializerMethodField()
    latest_summary_date = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ["id", "state", "created_at", "messages", "latest_summary", "latest_summary_date"]

    def get_latest_summary(self, obj):
        summary = getattr(obj, "latest_summary", None)
        if summary:
            return summary
        last_summary = ConversationSummary.objects.filter(conversation=obj).order_by("-date").first()
        return last_summary.summary if last_summary else None

    def get_latest_summary_date(self, obj):
        summary_date = getattr(obj, "latest_summary_date", None)
        if summary_date:
            return summary_date
        last_summary = ConversationSummary.objects.filter(conversation=obj).order_by("-date").first()
        return last_summary.date if last_summary else None