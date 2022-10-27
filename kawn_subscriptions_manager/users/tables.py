import django_tables2 as tables

from .models import User


class UserTable(tables.Table):
    username = tables.Column(orderable=True, linkify=True)
    name = tables.Column(orderable=True, linkify=True)
    email = tables.Column(orderable=True, linkify=True)
    verified = tables.Column(orderable=True, linkify=True)
    type = tables.Column(orderable=True, linkify=True)

    class Meta:
        model = User
        template_name = "users/user_list.html"
