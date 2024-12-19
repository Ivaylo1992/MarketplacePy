from django.contrib.auth import get_user_model
from django.db import models

from MarketplacePy.common.models import TimeStampedMixin, HasUser

UserModel = get_user_model()


class Conversation(TimeStampedMixin):
    item = models.ForeignKey(
        to="items.Item",
        on_delete=models.CASCADE
    )

    members = models.ManyToManyField(
        to=UserModel,
        related_name="conversations",
    )

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"Conversation ID{self.id} for {self.item.name}"

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
        return f"Message by {self.user.profile.get_name} in conversation {self.conversation}"
