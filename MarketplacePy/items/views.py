from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Exists, Q, OuterRef
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views

from MarketplacePy.conversations.models import Conversation
from MarketplacePy.items.forms import ItemPhotoAddForm, ItemAddForm, ItemPhotoEditForm, SearchItemForm, PriceRangeForm
from MarketplacePy.items.models import Item, ItemPhoto, Category, ItemLike


class ItemAddView(LoginRequiredMixin, views.View):
    template_name = 'items/item-add.html'

    def get_context_data(self, **kwargs):
        context = {
            'photo_form': kwargs.get('photo_form', ItemPhotoAddForm()),
            'product_form': kwargs.get('product_form', ItemAddForm())
        }
        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        photo_form = ItemPhotoAddForm(request.POST, request.FILES)
        product_form = ItemAddForm(request.POST)

        if photo_form.is_valid() and product_form.is_valid():
            item_instance = product_form.save(commit=False)
            item_instance.user = request.user
            item_instance.save()
            photo_form.save_photos(user=request.user, item=item_instance)

            if not photo_form.errors:
                return redirect(
                    "item_details",
                    pk=item_instance.pk
                )
            return redirect(
                "item_edit",
                pk=item_instance.pk,
            )

        return render(request, self.template_name, self.get_context_data(
            photo_form=photo_form, product_form=product_form,
        ))


class ItemDetailsView(LoginRequiredMixin, views.DetailView):
    queryset = Item.objects.all() \
        .prefetch_related("photos")

    template_name = 'items/item-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["conversation"] = Conversation.objects.filter(
            Q(members__in=[self.request.user, self.get_object().user]),
            item=self.object,
        ).first()
        return context


class ItemEditView(LoginRequiredMixin, views.View):
    template_name = "items/item-edit.html"

    def get_object(self, *args, **kwargs):
        return Item.objects.get(pk=self.kwargs["pk"])

    def get_success_url(self):
        return reverse_lazy(
            "item_details",
            kwargs={"pk": self.get_object().pk}
        )

    def get_context_data(self, **kwargs):
        context = {
            'item': self.get_object(),
            'images': self.get_object().photos.all(),
            'photo_form': ItemPhotoEditForm(),
            'item_form': ItemAddForm(
                instance=self.get_object()),
        }

        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        photo_form = ItemPhotoEditForm(request.POST, request.FILES)
        item_form = ItemAddForm(request.POST, instance=self.get_context_data()['item'])

        if photo_form.is_valid() and item_form.is_valid():
            item_instance = item_form.save(commit=False)

            photo_form.save_photos(user=request.user, item=item_instance)
            if not photo_form.errors:
                item_instance.save()
                return redirect(self.get_success_url())

        return render(request, self.template_name, {
            'photo_form': photo_form,  # Pass the photo form with errors
            'item_form': item_form,  # Pass the product form with errors
            'item': self.get_context_data()["item"],  # Pass the product for context
            'images': self.get_object().photos.all(),
        })


class ItemDeleteView(LoginRequiredMixin, views.DeleteView):
    model = Item
    template_name = "items/item-delete.html"
    success_url = reverse_lazy('home_page')


class PhotoDeleteView(LoginRequiredMixin, views.DeleteView):
    model = ItemPhoto

    def get_success_url(self):
        return reverse_lazy(
            'item_edit',
            kwargs={'pk': self.object.item.pk}
        )


class ItemsBrowseView(views.ListView):
    template_name = 'items/items-browse.html'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchItemForm
        context['categories'] = Category.objects.all()
        context['price_form'] = PriceRangeForm
        return context

    def get_queryset(self):
        if self.request.user.is_authenticated:
            items = Item.objects.all()\
                .annotate(
                has_like=Exists(
                    ItemLike.objects.filter(item=OuterRef('pk'), user=self.request.user)
                )
            )
        else:
            items = Item.objects.all()

        query = self.request.GET.get('query_param', '')
        category_id = self.request.GET.get('category', 0)
        min_price = self.request.GET.get('min_price', 0)
        max_price = self.request.GET.get('max_price', 9999)

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


class AppUserProductsView(LoginRequiredMixin, views.ListView):
    template_name = "items/my-items.html"
    context_object_name = "my_items"

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)