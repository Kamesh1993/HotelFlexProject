# Generated by Django 2.0.4 on 2018-11-29 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_roombooking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roombooking',
            name='phone',
            field=models.IntegerField(max_length=12),
        ),
    ]
