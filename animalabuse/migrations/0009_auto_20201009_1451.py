# Generated by Django 3.1.2 on 2020-10-09 14:51

from django.db import migrations
import localflavor.us.models


class Migration(migrations.Migration):

    dependencies = [
        ('animalabuse', '0008_delete_offensetype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animalabuse',
            name='state',
            field=localflavor.us.models.USStateField(blank=True, max_length=2, null=True),
        ),
    ]