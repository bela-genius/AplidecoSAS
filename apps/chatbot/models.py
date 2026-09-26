from django.db import models


class KnowledgeEntry(models.Model):
    """Entrada de conocimiento que el bot usa para responder preguntas puntuales."""

    trigger_keywords = models.CharField(
        max_length=255,
        help_text="Palabras clave separadas por coma que activan esta respuesta.",
    )
    question_example = models.CharField(max_length=255, blank=True)
    answer = models.TextField()
    is_active = models.BooleanField(default=True)
    priority = models.PositiveIntegerField(default=0, help_text="Mayor valor = mayor prioridad.")

    class Meta:
        ordering = ["-priority"]
        verbose_name_plural = "Knowledge entries"

    def __str__(self) -> str:
        return self.question_example or self.trigger_keywords

    def keywords(self) -> list[str]:
        return [k.strip().lower() for k in self.trigger_keywords.split(",") if k.strip()]


class Conversation(models.Model):
    session_key = models.CharField(max_length=64, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    class Sender(models.TextChoices):
        USER = "user", "Usuario"
        BOT = "bot", "Bot"

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.CharField(max_length=10, choices=Sender.choices)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
