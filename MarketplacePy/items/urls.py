from django.urls import path, include

from MarketplacePy.items import views

urlpatterns = (
    path("add/", views.ItemAddView.as_view(), name="item_add"),
    path("<int:pk>/", include([
        path("", views.ItemDetailsView.as_view(), name="item_details"),
        path("edit/", views.ItemEditView.as_view(), name="item_edit"),
        path("delete/", views.ItemDeleteView.as_view(), name="item_delete"),
    ])),
    path("photos/<int:pk>/delete/", views.PhotoDeleteView.as_view(), name="photo_delete"),
)