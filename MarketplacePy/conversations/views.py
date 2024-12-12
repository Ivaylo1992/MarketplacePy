from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
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
            members__in=[self.request.user],
        ).prefetch_related(
            "messages")


class SendMessageView(LoginRequiredMixin, views.CreateView):
    form_class = SendMessageForm
    template_name = "conversations/start-conversation.html"

    def get_object(self, queryset=None):
        item = self.get_context_data()['item']
        members = (self.request.user, item.user)

        conversation = Conversation.objects.filter(members__in=members, item=item).first()
        # Creates a new Conversation if it doesn't already exist
        if not conversation:
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(*members)

        return conversation

    def form_valid(self, form):
        form.instance.conversation = self.get_object()
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["item"] = Item.objects.get(id=self.kwargs["item_id"])
        context["item_photo"] = context["item"].photos.first()
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


class ConversationDetailView(LoginRequiredMixin, views.DetailView):
    queryset = Conversation.objects.all() \
        .prefetch_related("messages")

    pk_url_kwarg = "conversation_id"
    template_name = "conversations/conversation-details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["item"] = Item.objects.get(id=self.kwargs["item_id"])
        context["item_photo"] = context["item"].photos.first()
        context["form"] = SendMessageForm
        return context
