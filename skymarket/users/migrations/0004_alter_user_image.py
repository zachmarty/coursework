# Generated by Django 5.0.6 on 2024-06-29 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.URLField(blank=True, null=True, verbose_name='Аватар'),
        ),
    ]