import django.db
import django.forms


class Feedback(django.db.models.Model):
    name = django.db.models.CharField(max_length=100)
    text = django.db.models.TextField()
    created_on = django.db.models.DateTimeField(auto_now_add=True, null=True)
    mail = django.db.models.EmailField()


__all__ = ['Feedback']
