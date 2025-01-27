__all__ = []

import django.views.generic


class DescriptionView(
    django.views.generic.TemplateView,
):
    template_name = "about/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "О нас"

        return context
