__all__ = []

import django.contrib
import django.contrib.admin

import catalog.models

django.contrib.admin.site.register(catalog.models.Category)
django.contrib.admin.site.register(catalog.models.Tag)


class GalleryInline(django.contrib.admin.TabularInline):
    fk_name = catalog.models.Gallery.product.field.name
    model = catalog.models.Gallery


@django.contrib.admin.register(catalog.models.Item)
class ItemAdmin(django.contrib.admin.ModelAdmin):
    inlines = [
        GalleryInline,
    ]
    list_display = (
        catalog.models.Item.name.field.name,
        catalog.models.Item.is_published.field.name,
        catalog.models.Item.MainImage.field.name,
    )
    list_editable = (catalog.models.Item.is_published.field.name,)
    list_display_links = (catalog.models.Item.name.field.name,)
    filter_horizontal = (catalog.models.Item.tags.field.name,)
    readonly_fields = (
        catalog.models.Item.created_at.field.name,
        catalog.models.Item.updated_at.field.name,
    )
