from django.urls import path

from MarketplacePy.home import views

urlpatterns = (
    path("", views.HomePageView.as_view(), name="home_page"),
)