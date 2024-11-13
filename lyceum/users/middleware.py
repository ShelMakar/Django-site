from django.utils.deprecation import MiddlewareMixin

from users.models import User


class ProxyUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated and isinstance(request.user, User):
            request.user = User.objects.get(pk=request.user.pk)


__all__ = []
