from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.db.models import Avg
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
    queryset = Profile.objects.all().prefetch_related("user")
    template_name = "accounts/profile-details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items_per_page = 4
        profile = self.object

        # Get items for the user
        items = profile.user.item_set.all()

        # Paginate items
        paginator = Paginator(items, items_per_page)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Calculate average rating
        average_rating = profile.user.received_reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
        full_stars = int(average_rating)  # Number of full stars
        half_star = 1 if (average_rating - full_stars) >= 0.5 else 0  # Half star if applicable
        empty_stars = 5 - (full_stars + half_star)  # Remaining empty stars

        # Create lists for stars
        full_stars_list = range(full_stars)
        half_star_list = range(half_star)
        empty_stars_list = range(empty_stars)

        # Add to context
        context.update({
            'page_obj': page_obj,
            'full_stars_list': full_stars_list,
            'half_star_list': half_star_list,
            'empty_stars_list': empty_stars_list,
        })
        return context


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