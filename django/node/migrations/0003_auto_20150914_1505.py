# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import node.models
import node.storage
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('node', '0002_auto_20150914_1447'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadFile',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, max_length=64, serialize=False, verbose_name='UUID key', primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('upload_file', models.FileField(storage=node.storage.OverwriteStorage(), upload_to=node.models.file_upload_path)),
                ('active', models.BooleanField(default=True)),
                ('category', models.ForeignKey(to='node.Category', null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='resource',
            name='category',
        ),
        migrations.DeleteModel(
            name='Resource',
        ),
    ]
