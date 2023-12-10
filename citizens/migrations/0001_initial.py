# Generated by Django 4.2.7 on 2023-12-10 16:30

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=None, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg'])])),
                ('first_name', models.CharField(max_length=50)),
                ('gender', models.CharField(default='Female', max_length=6)),
                ('last_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(max_length=50)),
                ('dob', models.CharField(max_length=50)),
                ('state_of_origin', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100, null=True)),
                ('phone', models.CharField(max_length=50)),
                ('occupation', models.CharField(max_length=100, null=True)),
                ('marital_status', models.CharField(choices=[('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced'), ('Widowed', 'Widowed')], max_length=20, null=True)),
                ('health_code', models.CharField(editable=False, max_length=20, null=True)),
                ('bloodgroup', models.CharField(choices=[('O+', 'O positive'), ('O-', 'O negative'), ('A-', 'A negative'), ('A+', 'A positive'), ('B-', 'B negative'), ('B+', 'B positive'), ('AB-', 'AB negative'), ('AB+', 'AB positive')], max_length=3, null=True)),
                ('genotype', models.CharField(choices=[('AA', 'AA'), ('AS', 'AS'), ('SS', 'SS'), ('SC', 'SC'), ('AC', 'AC')], max_length=3, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Relatives',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('gender', models.CharField(blank=True, max_length=50, null=True)),
                ('occupation', models.CharField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(max_length=50)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='citizens.profile')),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='role',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='citizens.role'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='NextOfKin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('relationship', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=50)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nextofkin', to='citizens.profile')),
            ],
        ),
    ]
