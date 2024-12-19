from django.views import generic as views

from MarketplacePy.accounts.models import AppUser
from MarketplacePy.items.models import Category, Item


class HomePageView(views.ListView):
    queryset = Category.objects.prefetch_related(
        "items",
        "items__photos"
    ).all()
    template_name = "home/home-page.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["users_count"] = AppUser.objects.count()
        context["items"] = Item.objects.all()
        return context
