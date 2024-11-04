import django.conf
import django.contrib.messages
import django.core.mail
import django.shortcuts

import feedback.forms


def feedback_view(request):
    template = 'feedback/feedback.html'
    form = feedback.forms.FeedbackForm(request.POST or None)
    server_mail = django.conf.settings.DEFAULT_FROM_EMAIL
    if form.is_valid() and request.method == 'POST':
        name = form.cleaned_data['name']
        text = form.cleaned_data['text']
        mail = form.cleaned_data['mail']
        django.core.mail.send_mail(
            name,
            text,
            server_mail,
            [mail],
        )
        django.contrib.messages.success(request, 'Форма успешно отправлена')
        return django.shortcuts.redirect('feedback:feedback')

    context = {
        'form': form,
    }
    return django.shortcuts.render(request, template, context)


__all__ = ['feedback_view']
