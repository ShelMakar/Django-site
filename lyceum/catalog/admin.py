import django.contrib
import django.contrib.admin

import catalog.models


class MainImageAdminInline(django.contrib.admin.TabularInline):
    model = catalog.models.MainImage
    max_num = 1


class SecondImagesAdminInline(django.contrib.admin.TabularInline):
    model = catalog.models.SecondImages


@django.contrib.admin.register(catalog.models.Item)
class ItemAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        'preview',
        catalog.models.Item.name.field.name,
        catalog.models.Item.is_published.field.name,
    )
    list_editable = (catalog.models.Item.is_published.field.name,)
    list_display_links = (catalog.models.Item.name.field.name,)
    filter_horizontal = (catalog.models.Item.tags.field.name,)
    inlines = [
        MainImageAdminInline,
        SecondImagesAdminInline,
    ]

    @django.contrib.admin.display(description="превью")
    def preview(self, obj):
        main_image_instance = obj.mainimage.first()
        if main_image_instance:
            return main_image_instance.image_tmb()
        return "Нет изображения"


@django.contrib.admin.register(catalog.models.Category)
class CategoryAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        catalog.models.Category.name.field.name,
        catalog.models.Category.is_published.field.name,
        catalog.models.Category.slug.field.name,
        catalog.models.Category.weight.field.name,
        catalog.models.Category.normalized_name.field.name,
    )


@django.contrib.admin.register(catalog.models.Tag)
class TagAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        catalog.models.Tag.name.field.name,
        catalog.models.Tag.is_published.field.name,
        catalog.models.Tag.slug.field.name,
        catalog.models.Tag.normalized_name.field.name,
    )




django.contrib.admin.site.register(catalog.models.MainImage)

__all__ = [
    'TagAdmin',
    'CategoryAdmin',
    'ItemAdmin',
    'MainImageAdminInline',
    'SecondImagesAdminInline',
]
