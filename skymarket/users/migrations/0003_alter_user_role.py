# Generated by Django 5.0.6 on 2024-06-26 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_last_login_alter_user_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('1', 'USER'), ('2', 'ADMIN')], default='1', verbose_name='Роль'),
        ),
    ]
