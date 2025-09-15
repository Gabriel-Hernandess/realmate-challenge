from django.urls import path
from .views import WebhookView, ConversationDetailView, GetConversations, ConversationSummariesView

urlpatterns = [
    path("webhook/", WebhookView.as_view(), name="webhook"),
    path("conversations/", GetConversations.as_view(), name="get-conversations"),
    path("conversations/<uuid:pk>/", ConversationDetailView.as_view(), name="conversation-detail"),
    path("conversations/<uuid:pk>/summaries/", ConversationSummariesView.as_view()),
]