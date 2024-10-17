import django.contrib

import catalog.models


@django.contrib.admin.register(catalog.models.Item)
class ItemAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        catalog.models.Item.id.field.name,
        catalog.models.Item.name.field.name,
        catalog.models.Item.is_published.field.name,
    )
    list_editable = (catalog.models.Item.is_published.field.name,)
    list_display_links = (catalog.models.Item.name.field.name,)
    filter_horizontal = (catalog.models.Item.tags.field.name,)


@django.contrib.admin.register(catalog.models.Category)
class CategoryAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        catalog.models.Category.id.field.name,
        catalog.models.Category.name.field.name,
        catalog.models.Category.is_published.field.name,
        catalog.models.Category.slug.field.name,
        catalog.models.Category.weight.field.name,
        catalog.models.Category.normalized_name.field.name,
    )


@django.contrib.admin.register(catalog.models.Tag)
class TagAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        catalog.models.Tag.id.field.name,
        catalog.models.Tag.name.field.name,
        catalog.models.Tag.is_published.field.name,
        catalog.models.Tag.slug.field.name,
        catalog.models.Tag.normalized_name.field.name,
    )
