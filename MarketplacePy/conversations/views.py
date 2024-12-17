from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q, Subquery, OuterRef, Case, When, F
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
        return Conversation.objects.filter(members=self.request.user)


class SendMessageView(LoginRequiredMixin, views.CreateView):
    form_class = SendMessageForm
    template_name = "conversations/start-conversation.html"

    def get_object(self, queryset=None):
        item = Item.objects.get(id=self.kwargs["item_id"])
        members = [self.request.user, item.user]

        conversation = Conversation.objects.filter(
            members=members[0]
        ).filter(
            members=members[1],
            item=item,
        ).distinct().first()

        if not conversation:
            conversation = Conversation.objects.create(
                item=item,
            )

            conversation.members.add(*members)

        return conversation

    def form_valid(self, form):
        conversation = self.get_object()

        form.instance.conversation = conversation
        form.instance.user = self.request.user

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "conversation_details",
            kwargs={
                "conversation_id": self.get_object().pk,
                "item_id": self.kwargs["item_id"]
            }
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["item"] = Item.objects.get(id=self.kwargs["item_id"])
        return context


class ConversationDetailView(LoginRequiredMixin, UserPassesTestMixin, views.DetailView):
    queryset = Conversation.objects.all() \
        .prefetch_related("messages")

    def get_object(self, queryset=None):
        return Conversation.objects.get(id=self.kwargs["conversation_id"])

    pk_url_kwarg = "conversation_id"
    template_name = "conversations/conversation-details.html"

    def test_func(self):
        return self.request.user in self.get_object().members.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["item"] = Item.objects.get(id=self.kwargs["item_id"])
        context["form"] = SendMessageForm
        return context
