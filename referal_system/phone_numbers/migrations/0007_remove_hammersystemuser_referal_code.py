# Generated by Django 5.1.3 on 2024-12-01 16:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phone_numbers', '0006_alter_hammersystemuser_auth_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hammersystemuser',
            name='referal_code',
        ),
    ]
