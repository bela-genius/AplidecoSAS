from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Conversation, Message
from .services import find_answer


@api_view(["POST"])
@permission_classes([AllowAny])
def chat_message(request):
    text = (request.data.get("message") or "").strip()
    if not text:
        return Response({"error": "El mensaje no puede estar vacío."}, status=400)

    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    conversation, _ = Conversation.objects.get_or_create(session_key=session_key)
    Message.objects.create(conversation=conversation, sender=Message.Sender.USER, text=text)

    answer = find_answer(text)
    Message.objects.create(conversation=conversation, sender=Message.Sender.BOT, text=answer)

    return Response({"reply": answer})
