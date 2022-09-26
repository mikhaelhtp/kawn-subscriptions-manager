from django.forms import ModelForm

from .models import Client

class ClientAddForm(ModelForm):
    class Meta:
        model = Client
        fields = ['name','business_name']

    def save(self, commit=True):
        client = super().save(commit=False)
        if commit:
            client.save()
        return client