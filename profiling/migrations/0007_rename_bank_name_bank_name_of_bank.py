# Generated by Django 4.2.7 on 2023-12-25 10:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiling', '0006_userprofile_gender'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bank',
            old_name='bank_name',
            new_name='name_of_bank',
        ),
    ]