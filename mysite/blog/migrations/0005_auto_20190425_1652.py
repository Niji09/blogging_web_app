# Generated by Django 2.2 on 2019-04-25 11:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20190425_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='viewer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
