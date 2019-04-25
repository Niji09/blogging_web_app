# Generated by Django 2.2 on 2019-04-21 06:42

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('text', models.TextField()),
                ('create_date', models.DateTimeField(default=datetime.datetime(2019, 4, 21, 6, 42, 21, 339573, tzinfo=utc))),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('auther', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auther', models.CharField(max_length=256)),
                ('text', models.TextField()),
                ('create_date', models.DateTimeField(default=datetime.datetime(2019, 4, 21, 6, 42, 21, 339573, tzinfo=utc))),
                ('approve_comment', models.BooleanField(default=False)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.Post')),
            ],
        ),
    ]
