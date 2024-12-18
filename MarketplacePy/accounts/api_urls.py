from django.urls import path
from .api_views import UserReviewView

urlpatterns = [
    path('reviews/<int:reviewed_user_id>/', UserReviewView.as_view(), name='user-review'),
]