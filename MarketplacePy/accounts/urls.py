from django.urls import path, include
from MarketplacePy.accounts import views

urlpatterns = (
    path("register/", views.AppUserRegisterView.as_view(), name="register"),
    path("login/", views.AppUserLoginView.as_view(), name="login"),
    path("profile/<int:pk>/", include([
        path("", views.ProfileDetailsView.as_view(), name="profile_details"),
        path("edit/", views.ProfileEditView.as_view(), name="profile_edit"),
        path("delete/", views.ProfileDeleteView.as_view(), name="profile_edit"),
    ]))
)