# Generated by Django 4.0.6 on 2022-07-28 00:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("address_book", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="address",
            old_name="ing",
            new_name="lng",
        ),
    ]
