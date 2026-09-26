from .models import KnowledgeEntry

FALLBACK_ANSWER = (
    "No tengo una respuesta exacta para eso todavía, pero puedes escribirnos por "
    "WhatsApp o redes sociales y con gusto te ayudamos."
)


def find_answer(user_text: str) -> str:
    text = user_text.lower()
    for entry in KnowledgeEntry.objects.filter(is_active=True):
        if any(keyword in text for keyword in entry.keywords()):
            return entry.answer
    return FALLBACK_ANSWER
