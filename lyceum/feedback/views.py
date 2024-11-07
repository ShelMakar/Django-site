import django.conf
import django.contrib.messages
import django.core.mail
import django.shortcuts

import feedback.forms
import feedback.models


def feedback_view(request):
    template = 'feedback/feedback.html'
    form = feedback.forms.FeedbackForm(request.POST or None)
    user_form = feedback.forms.FeedbackContactForm(request.POST or None)
    file_form = feedback.forms.FileFieldForm(
        request.POST or None, request.FILES or None,
    )
    if (
        request.method == 'POST'
        and form.is_valid()
        and user_form.is_valid()
        and file_form.is_valid()
    ):
        fb = form.save(commit=False)
        fb.status = 'received'
        fb.save()
        text = form.cleaned_data.get('text')
        mail = user_form.cleaned_data.get('mail')
        feedback.models.FeedbackContact.objects.create(
            name=user_form.cleaned_data.get('name'),
            mail=mail,
            user_info=fb,
        )

        for file in file_form.cleaned_data.get('file'):
            file.create(file=file)

        django.core.mail.send_mail(
            'Что-то',
            text,
            django.conf.settings.DEFAULT_FROM_EMAIL,
            [mail],
            fail_silently=False,
        )
        feedback.models.StatusLog.objects.create(
            feedback=fb,
            from_status='',
            to=fb.status,
        )
        django.contrib.messages.success(request, 'Форма успешно отправлена')
        return django.shortcuts.redirect('feedback:feedback')

    context = {
        'form': form,
        'file_form': file_form,
        'user_form': user_form,
    }
    return django.shortcuts.render(request, template, context)


__all__ = ['feedback_view']
