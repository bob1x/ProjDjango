# Generated by Django 5.0.4 on 2024-05-18 00:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('isety', '0005_evenement_inrest'),
    ]

    operations = [
        migrations.RenameField(
            model_name='evenement',
            old_name='inrest',
            new_name='interest',
        ),
    ]
