# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import node.models
import node.storage
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('node', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, max_length=64, serialize=False, verbose_name='UUID key', primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('resource', models.FileField(storage=node.storage.OverwriteStorage(), upload_to=node.models.file_upload_path)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='node',
            name='category',
        ),
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default='A', unique=True, max_length=150),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Node',
        ),
        migrations.AddField(
            model_name='resource',
            name='category',
            field=models.ForeignKey(to='node.Category', null=True),
        ),
    ]
