from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import OuterRef, Subquery

from .tasks import process_webhook_task
from .models import Conversation, ConversationSummary
from .serializers import ConversationSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

class WebhookView(APIView):
    def post(self, request):
        try:
            event_type = request.data.get("type")
            timestamp_str = request.data.get("timestamp")
            data = request.data.get("data", {})

            # validação mínima antes de chamar a task
            if event_type not in ["NEW_CONVERSATION", "NEW_MESSAGE", "CLOSE_CONVERSATION"]:
                return Response({"error": "Unknown event type"}, status=status.HTTP_400_BAD_REQUEST)

            if not isinstance(data, dict) or "id" not in data:
                return Response({"error": "Missing or invalid 'data.id'"}, status=status.HTTP_400_BAD_REQUEST)

            # se for NEW_MESSAGE, validar conversation_id e direction
            if event_type == "NEW_MESSAGE":
                if "conversation_id" not in data or "direction" not in data or "content" not in data:
                    return Response({"error": "Missing message fields"}, status=status.HTTP_400_BAD_REQUEST)
                if data["direction"] not in ["SENT", "RECEIVED"]:
                    return Response({"error": "Invalid message direction"}, status=status.HTTP_400_BAD_REQUEST)

            # chama a task assíncrona
            process_webhook_task.delay(event_type, data, timestamp_str)

            return Response({"status": "queued"}, status=status.HTTP_202_ACCEPTED)

        except KeyError as e:
            return Response({"error": f"Missing key: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # captura qualquer outro erro para evitar HTTP 500
            return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


class GetConversations(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            latest_summary = ConversationSummary.objects.filter(
                conversation=OuterRef("pk")
            ).order_by("-date")

            conversations = Conversation.objects.all().annotate(
                latest_summary=Subquery(latest_summary.values("summary")[:1]),
                latest_summary_date=Subquery(latest_summary.values("date")[:1]),
            ).prefetch_related("messages")

            serializer = ConversationSerializer(conversations, many=True)
            return Response({"success": True, "conversations": serializer.data}, status=200)

        except Exception as e:
            return Response({"success": False, "error": str(e), "conversations": []}, status=400)


class ConversationDetailView(APIView):
    def get(self, request, pk):
        try:
            # tenta buscar a conversa
            conversation = get_object_or_404(Conversation, pk=pk)
            
            # serializa a conversa com as mensagens relacionadas
            serializer = ConversationSerializer(conversation)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Conversation.DoesNotExist:
            # caso a conversa não exista
            return Response({"error": "Conversation not found"}, status=status.HTTP_404_NOT_FOUND)

        except ValueError as e:
            # captura erros de tipo ou formatação do pk
            return Response({"error": f"Invalid ID format: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # captura qualquer outro erro inesperado
            return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        

class ConversationSummariesView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        summaries = ConversationSummary.objects.filter(conversation_id=pk).order_by('-date')
        data = [{"date": s.date, "summary": s.summary} for s in summaries]
        return Response({"success": True, "summaries": data}, status=200)