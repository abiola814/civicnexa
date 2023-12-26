# Generated by Django 4.2.7 on 2023-12-26 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiling', '0009_rename_address_userprofile_main_address_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='main_address',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='main_phone',
            new_name='nin',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
