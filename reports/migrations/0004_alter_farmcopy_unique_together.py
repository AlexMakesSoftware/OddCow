# Generated by Django 4.2.2 on 2023-07-19 11:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("reports", "0003_alter_farmcopy_unique_together"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="farmcopy",
            unique_together={("county", "parish", "holding_number")},
        ),
    ]