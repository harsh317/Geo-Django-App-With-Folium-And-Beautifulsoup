# Generated by Django 3.1.4 on 2020-12-21 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mesurements', '0005_auto_20201221_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mesurementsofdistance',
            name='location',
            field=models.CharField(max_length=85),
        ),
    ]
