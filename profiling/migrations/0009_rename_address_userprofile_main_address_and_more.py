# Generated by Django 4.2.7 on 2023-12-26 10:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiling', '0008_rename_name_of_bank_bank_bank_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='address',
            new_name='main_address',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='phone',
            new_name='main_phone',
        ),
    ]