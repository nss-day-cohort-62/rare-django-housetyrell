# Generated by Django 4.2.1 on 2023-05-05 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rareapi', '0002_subscription'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='ended_on',
        ),
    ]
