# Generated by Django 3.2.15 on 2022-09-20 06:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20220913_1046'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salesmore',
            name='user',
        ),
        migrations.RemoveField(
            model_name='supervisormore',
            name='user',
        ),
        migrations.DeleteModel(
            name='AdminMore',
        ),
        migrations.DeleteModel(
            name='SalesMore',
        ),
        migrations.DeleteModel(
            name='SupervisorMore',
        ),
    ]
