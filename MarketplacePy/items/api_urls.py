from django.urls import path
from MarketplacePy.items import api_views as views

urlpatterns = [
    path('like/<int:item_id>/', views.LikeApiView.as_view(), name='like-api'),
]