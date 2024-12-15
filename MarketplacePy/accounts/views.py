from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import views as auth_views

from MarketplacePy.accounts.forms import AppUserCreationForm, AppUserLoginForm, ProfileEditForm
from MarketplacePy.accounts.models import Profile

UserModel = get_user_model()


class AppUserRegisterView(views.CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("login")


class AppUserLoginView(auth_views.LoginView):
    form_class = AppUserLoginForm
    template_name = "accounts/login.html"

    def form_valid(self, form):
        super().form_valid(form)
        profile_instance, _ = Profile.objects.get_or_create(user=self.request.user)
        return HttpResponseRedirect(self.get_success_url())


class AppUserLogoutView(auth_views.LogoutView):
    ...


class ProfileDetailsView(LoginRequiredMixin, views.DetailView):
    queryset = Profile.objects.all()
    template_name = "accounts/profile-details.html"


class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, views.UpdateView):
    model = Profile
    template_name = "accounts/profile-edit.html"
    form_class = ProfileEditForm

    def test_func(self):
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        return self.request.user == profile.user

    def get_success_url(self):
        return reverse_lazy(
            "profile_details",
            kwargs={"pk": self.object.pk}
        )


class ProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, views.DeleteView):
    model = UserModel
    template_name = "accounts/profile-delete.html"
    success_url = reverse_lazy("index")

    def test_func(self):
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        return self.request.user == profile.user