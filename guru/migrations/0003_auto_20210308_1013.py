# Generated by Django 3.0.5 on 2021-03-08 10:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('guru', '0002_gelar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gelar',
            name='guru',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
