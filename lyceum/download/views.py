import pathlib

import django.conf
import django.http


def download_image(request, path):
    path = pathlib.Path(django.conf.settings.MEDIA_ROOT) / path
    path.exists()
    return django.http.FileResponse(
        open(path, 'rb'), as_attachment=True, content_type='image',
    )


__all__ = ['download_image']
