# Generated by Django 3.2.3 on 2021-06-18 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20210617_1305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='deleted',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
