from django.contrib.auth import get_user_model
from django.db import models

from MarketplacePy.common.models import TimeStampedMixin, HasUser

UserModel = get_user_model()


class Conversation(TimeStampedMixin):
    item = models.ForeignKey(
        to="items.Item",
        on_delete=models.CASCADE
    )

    sender = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
        related_name="sent_conversations"
    )

    recipient = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
        related_name="received_conversations"
    )

    class Meta:
        ordering = ["-updated_at"]


class Message(HasUser, TimeStampedMixin):
    conversation = models.ForeignKey(
        to="conversations.Conversation",
        on_delete=models.CASCADE,
        related_name="messages",
    )

    content = models.TextField()

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Message by {self.user.username} in conversation {self.conversation}"

