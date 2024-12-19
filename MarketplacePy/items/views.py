from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Exists, Q, OuterRef
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic as views

from MarketplacePy.conversations.models import Conversation
from MarketplacePy.items.forms import ItemPhotoAddForm, ItemAddForm, SearchItemForm, PriceRangeForm, \
    ItemEditForm
from MarketplacePy.items.models import Item, ItemPhoto, Category, ItemLike


class ItemAddView(LoginRequiredMixin, views.CreateView):
    model = Item
    form_class = ItemAddForm
    success_url = reverse_lazy("my_items")
    template_name = "items/item-add.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ItemDetailsView(LoginRequiredMixin, views.DetailView):
    queryset = Item.objects.all() \
        .prefetch_related("photos")

    template_name = "items/item-details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["conversation"] = Conversation.objects.filter(
            members=self.request.user,
            item=self.object,
        ).filter(
            members=self.object.user
        ).distinct().first()

        return context


class ItemEditView(LoginRequiredMixin, UserPassesTestMixin, views.UpdateView):
    model = Item
    form_class = ItemEditForm
    template_name = "items/item-edit.html"

    def test_func(self):
        user = self.get_object().user
        return self.request.user == user

    def get_success_url(self):
        return reverse_lazy(
            "item_details",
            kwargs={"pk": self.object.pk}
        )


class AddItemPhotoView(LoginRequiredMixin, UserPassesTestMixin, views.FormView):
    form_class = ItemPhotoAddForm
    template_name = "items/item-photo-add.html"

    def form_valid(self, form):
        item = self.get_context_data()["item"]
        user = self.request.user

        photo_instances = form.save_photos(user, item)

        if form.errors:
            return self.form_invalid(form)

        return super().form_valid(form)

    def form_invalid(self, form):
        item = self.get_context_data()["item"]
        photos = self.get_context_data()["photos"]

        return render(
            self.request,
            self.template_name,
            {
                "item": item,
                "photos": photos,
                "form": form,
            }
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["item"] = Item.objects.get(pk=self.kwargs["pk"])
        context["photos"] = context["item"].photos.all()

        return context

    def test_func(self):
        user = self.get_context_data()["item"].user
        return self.request.user == user

    def get_success_url(self):
        return reverse_lazy(
            "photo_add",
            kwargs={"pk": self.kwargs["pk"]}
        )


class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, views.DeleteView):
    model = Item
    template_name = "items/item-delete.html"
    success_url = reverse_lazy("my_items")

    def test_func(self):
        user = self.get_object().user
        return self.request.user == user


class PhotoDeleteView(LoginRequiredMixin, UserPassesTestMixin, views.DeleteView):
    model = ItemPhoto

    def test_func(self):
        user = self.get_object().user
        return self.request.user == user

    def get_success_url(self):
        return reverse_lazy(
            "photo_add",
            kwargs={"pk": self.object.item.pk}
        )


class ItemsBrowseView(views.ListView):
    template_name = "items/items-browse.html"
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["search_form"] = SearchItemForm
        context["categories"] = Category.objects.all()
        context["price_form"] = PriceRangeForm

        return context

    def get_queryset(self):
        if self.request.user.is_authenticated:
            items = Item.objects.all() \
                .annotate(
                has_like=Exists(
                    ItemLike.objects.filter(item=OuterRef("pk"), user=self.request.user)
                )
            )
        else:
            items = Item.objects.all()

        query = self.request.GET.get("query_param", "")
        category_id = self.request.GET.get("category", 0)
        min_price = self.request.GET.get("min_price", 0)
        max_price = self.request.GET.get("max_price", 9999)

        items = items.filter(Q(price__gte=min_price) & Q(price__lte=max_price))

        if category_id:
            items = items.filter(category_id=category_id)

        if query:
            items = items.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )

        return items


class LikedItemsView(LoginRequiredMixin, views.ListView):
    template_name = "items/liked-items.html"
    context_object_name = "liked_items"

    def get_queryset(self):
        return Item.objects.filter(likes__user=self.request.user)


class AppUserItemsView(LoginRequiredMixin, views.ListView):
    template_name = "items/my-items.html"
    context_object_name = "my_items"

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)
