# Generated by Django 5.1.3 on 2024-12-01 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phone_numbers', '0005_hammersystemuser_auth_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hammersystemuser',
            name='auth_code',
            field=models.CharField(max_length=4, null=True, verbose_name='Код авторизации'),
        ),
    ]
