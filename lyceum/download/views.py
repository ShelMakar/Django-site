import pathlib

import django.conf
import django.http


def download_image(request, path):
    file_path = pathlib.Path(django.conf.settings.MEDIA_ROOT) / path
    if not file_path.exists():
        return django.http.HttpResponseNotFound('изображение не найдено')
    response = django.http.FileResponse(
        open(file_path, 'rb'),
        as_attachment=True,
        content_type='image',
    )
    response['Content-Disposition'] = 'attachment; filename="%s"' % file_path
    return response


__all__ = ['download_image']
