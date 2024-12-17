from django.urls import path

from MarketplacePy.conversations import views

urlpatterns = (
    path("inbox/", views.InboxView.as_view(), name="inbox"),
    path(
        "conversation/item_id-<int:item_id>/",
        views.SendMessageView.as_view(), name="send_message"),
    path(
        "item_id-<int:item_id>/conversation/<int:conversation_id>/",
        views.ConversationDetailView.as_view(),
        name="conversation_details"
    ),
)