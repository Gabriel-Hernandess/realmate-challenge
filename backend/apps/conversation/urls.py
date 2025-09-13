from django.urls import path
from .views import WebhookView, ConversationDetailView, GetConversations

urlpatterns = [
    path("webhook/", WebhookView.as_view(), name="webhook"),
    path("conversations/", GetConversations.as_view(), name="get-conversations"),
    path("conversations/<uuid:pk>/", ConversationDetailView.as_view(), name="conversation-detail"),
]