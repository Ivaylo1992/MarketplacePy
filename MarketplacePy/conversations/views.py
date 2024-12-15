from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views import generic as views

from MarketplacePy.conversations.forms import SendMessageForm
from MarketplacePy.conversations.models import Conversation
from MarketplacePy.items.models import Item


# Create your views here.
class InboxView(LoginRequiredMixin, views.ListView):
    template_name = "conversations/inbox.html"
    context_object_name = "conversations"

    def get_queryset(self):
        return Conversation.objects.filter(
            Q(recipient=self.request.user) | Q(sender=self.request.user)
        )


class SendMessageView(LoginRequiredMixin, views.CreateView):
    form_class = SendMessageForm
    template_name = "conversations/start-conversation.html"

    def get_object(self, queryset=None):
        item = self.get_context_data()['item']
        sender = self.request.user
        recipient = item.user

        conversation = Conversation.objects.filter(
            sender=sender,
            recipient=recipient,
            item=item
        ).first()

        # Creates a new Conversation if it doesn't already exist
        if not conversation:
            conversation = Conversation.objects.create(
                sender=sender,
                recipient=recipient,
                item=item,
            )

        return conversation

    def form_valid(self, form):
        form.instance.conversation = self.get_object()
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["item"] = Item.objects.get(id=self.kwargs["item_id"])
        return context

    def get_success_url(self):
        result = reverse_lazy(
            "conversation_details",
            kwargs={
                "conversation_id": self.get_object().pk,
                "item_id": self.kwargs["item_id"],
            }
        )

        return result


class ConversationDetailView(LoginRequiredMixin, UserPassesTestMixin, views.DetailView):
    queryset = Conversation.objects.all() \
        .prefetch_related("messages")

    pk_url_kwarg = "conversation_id"
    template_name = "conversations/conversation-details.html"

    def test_func(self):
        return self.request.user == self.get_object().sender \
            or self.request.user == self.get_object().recipent

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["item"] = Item.objects.get(id=self.kwargs["item_id"])
        context["form"] = SendMessageForm
        return context
