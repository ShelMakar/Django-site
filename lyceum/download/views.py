import pathlib

import django.conf
import django.http


def download_image(request, path):
    path = pathlib.Path(django.conf.settings.MEDIA_ROOT) / path
    path.exists()
    response = django.http.FileResponse(open(path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{path.name}"'
    return response


__all__ = ['download_image']
