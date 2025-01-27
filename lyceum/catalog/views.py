__all__ = []

import datetime

import django.conf
import django.contrib.auth.decorators
import django.db.models.functions
import django.http
import django.shortcuts
import django.urls
import django.utils
import django.utils.decorators
import django.utils.translation
import django.views.generic

import catalog.models
import rating.forms
import rating.models


class ItemListView(
    django.views.generic.ListView,
):
    model = catalog.models.Item
    template_name = "catalog/item_list.html"

    def get_queryset(self):
        return catalog.models.Item.objects.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Cписок товаров"
        context["items"] = self.get_queryset()
        return context


class ItemDetailView(
    django.views.generic.DetailView,
):
    template_name = "catalog/item.html"
    model = catalog.models.Item
    pk_url_kwarg = "converter"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Подробнее о товаре: {context['item'].name}"
        product = self.get_object()
        ratings = rating.models.Rating.objects.filter(product=product)
        context["average_rating"] = (
            ratings.aggregate(
                django.db.models.Avg(
                    rating.models.Rating.rating.field.name,
                ),
            )["rating__avg"]
            or 0
        )
        context["ratings_count"] = ratings.count()

        if self.request.user.is_authenticated:
            user_rating = ratings.filter(user=self.request.user).first()
            context["user_rating"] = user_rating
            context["rating_form"] = rating.forms.PostRating(
                instance=user_rating,
            )

        return context

    @django.utils.decorators.method_decorator(
        django.contrib.auth.decorators.login_required,
    )
    def post(self, request, *args, **kwargs):
        product = self.get_object()
        user_rating = rating.models.Rating.objects.filter(
            user=request.user,
            product=product,
        ).first()

        form = rating.forms.PostRating(request.POST, instance=user_rating)
        if form.is_valid():
            rat = form.save(commit=False)
            rat.user = request.user
            rat.product = product
            rat.save()
            return django.shortcuts.redirect(
                django.urls.reverse("catalog:item_detail", args=[product.pk]),
            )

        return self.get(request, *args, **kwargs)

    def get_success_url(self):
        return self.request.path


class NewItemsView(
    django.views.generic.ListView,
):
    template_name = "catalog/item_list.html"
    model = catalog.models.Item

    def get_queryset(self):
        now = django.db.models.functions.Now()
        one_week_ago = now - datetime.timedelta(
            days=7,
        )
        tomorrow = now + datetime.timedelta(
            days=1,
        )

        return catalog.models.Item.objects.published().filter(
            created_at__range=(
                one_week_ago,
                tomorrow,
            ),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items"] = self.get_queryset()
        context["title"] = "Cписок новых товаров"
        return context


class FridayItemsView(
    django.views.generic.ListView,
):
    template_name = "catalog/item_list.html"
    model = catalog.models.Item

    def get_queryset(self):
        return catalog.models.Item.objects.published().filter(
            updated_at__week_day=6,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items"] = self.get_queryset()
        context["title"] = "Пятница"
        return context


class UnverifiedItemsView(
    django.views.generic.ListView,
):
    template_name = "catalog/item_list.html"
    model = catalog.models.Item

    def get_queryset(self):
        updated_at_minus_one = django.db.models.F(
            "updated_at",
        ) - datetime.timedelta(seconds=1)
        updated_at_plus_one = django.db.models.F(
            "updated_at",
        ) + datetime.timedelta(seconds=1)

        return catalog.models.Item.objects.published().filter(
            created_at__range=(updated_at_minus_one, updated_at_plus_one),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items"] = self.get_queryset()
        context["title"] = "Непроверенные"
        return context


class RegularView(django.views.generic.View):
    def get(self, request, p, *args, **kwargs):
        return django.http.HttpResponse(p)


class ConverterView(django.views.generic.View):
    def get(self, request, num, *args, **kwargs):
        return django.http.HttpResponse(num)
