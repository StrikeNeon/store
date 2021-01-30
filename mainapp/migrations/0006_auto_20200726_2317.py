# Generated by Django 3.0.7 on 2020-07-26 19:17

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainapp', '0005_banner_subscribed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='banner_pic',
            field=models.ImageField(upload_to='media/banners'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='subscribed',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)]),
        ),
        migrations.AlterField(
            model_name='userprofileinfo',
            name='profile_pic',
            field=models.ImageField(blank=True, upload_to='media/profile_pics'),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('review_text', models.TextField(verbose_name='review text')),
                ('rating', models.PositiveIntegerField(choices=[('one', 1), ('two', 2), ('three', 3), ('four', 4), ('five', 5)])),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Merch', verbose_name='reviewed product')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='reviewer id')),
            ],
        ),
    ]
