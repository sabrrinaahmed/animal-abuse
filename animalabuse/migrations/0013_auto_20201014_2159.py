# Generated by Django 3.1.2 on 2020-10-14 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animalabuse', '0012_auto_20201014_2158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animalabuse',
            name='image',
            field=models.URLField(null=True),
        ),
    ]
