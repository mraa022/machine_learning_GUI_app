# Generated by Django 3.0.6 on 2020-07-16 06:47

import datasets.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0027_auto_20200716_0641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datasets',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=datasets.models.path_and_rename, validators=[datasets.models.validate_file_extension]),
        ),
    ]
