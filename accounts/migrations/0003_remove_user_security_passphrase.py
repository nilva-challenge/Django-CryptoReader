# Generated by Django 3.2.8 on 2022-07-23 14:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20220722_1554'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='security_passphrase',
        ),
    ]