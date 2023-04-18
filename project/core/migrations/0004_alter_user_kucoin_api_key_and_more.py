# Generated by Django 4.2 on 2023-04-18 21:30

from django.db import migrations, models
import django_cryptography.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_user_kucoin_passphrase'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='kucoin_api_key',
            field=django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=255, null=True)),
        ),
        migrations.AlterField(
            model_name='user',
            name='kucoin_api_secret',
            field=django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=255, null=True)),
        ),
        migrations.AlterField(
            model_name='user',
            name='kucoin_passphrase',
            field=django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=255, null=True)),
        ),
    ]
