# Generated by Django 3.0.7 on 2020-07-26 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_auto_20200726_2317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.PositiveIntegerField(choices=[(1, 'one'), (2, 'two'), (3, 'three'), (4, 'four'), (5, 'five')]),
        ),
    ]
