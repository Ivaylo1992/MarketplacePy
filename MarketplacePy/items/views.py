from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views

from MarketplacePy.items.forms import ItemPhotoAddForm, ItemAddForm, ItemPhotoEditForm
from MarketplacePy.items.models import Item, ItemPhoto


class ItemAddView(views.View):
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


class ItemDetailsView(views.DetailView):
    queryset = Item.objects.all() \
        .prefetch_related("photos")

    template_name = 'items/item-details.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["conversation"] = Conversation.objects.filter(
    #         Q(members__in=[self.request.user, self.get_object().user]),
    #         product=self.object,
    #     ).first()
    #     return context


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
            'product': self.get_object(),
            'images': self.get_object().photos.all(),
            'photo_form': ItemPhotoEditForm(),
            'product_form': ItemAddForm(
                instance=self.get_object()),
        }

        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        photo_form = ItemPhotoEditForm(request.POST, request.FILES)
        product_form = ItemAddForm(request.POST, instance=self.get_context_data()['product'])

        if photo_form.is_valid() and product_form.is_valid():
            item_instance = product_form.save(commit=False)

            photo_form.save_photos(user=request.user, item=item_instance)
            if not photo_form.errors:
                item_instance.save()
                return redirect(self.get_success_url())

        return render(request, self.template_name, {
            'photo_form': photo_form,  # Pass the photo form with errors
            'product_form': product_form,  # Pass the product form with errors
            'item': self.get_object(),  # Pass the product for context
            'images': self.get_object().photos.all(),
        })


class ItemDeleteView(views.DeleteView):
    model = Item
    template_name = "items/item-delete.html"
    success_url = reverse_lazy('index')


class PhotoDeleteView(views.DeleteView):
    model = ItemPhoto

    def get_success_url(self):
        return reverse_lazy(
            'item_edit',
            kwargs={'pk': self.object.item.pk}
        )