# Generated by Django 3.2 on 2021-05-12 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pycompiler', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='snippet',
            name='filename',
            field=models.CharField(default='new', max_length=100),
            preserve_default=False,
        ),
    ]
