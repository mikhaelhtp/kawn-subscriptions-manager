from django.forms import ModelForm

from .models import Client


class ClientAddForm(ModelForm):
    class Meta:
        model = Client
        fields = ["name"]

    def save(self, commit=True):
        client = super().save(commit=False)
        if commit:
            client.save()
        return client
