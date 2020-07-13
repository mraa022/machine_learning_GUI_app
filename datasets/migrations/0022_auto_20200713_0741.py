# Generated by Django 3.0.6 on 2020-07-13 07:41

import datasets.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0021_auto_20200713_0722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datasets',
            name='file',
            field=models.FileField(blank=True, null=True, unique=True, upload_to='datasets', validators=[datasets.models.validate_file_extension]),
        ),
    ]