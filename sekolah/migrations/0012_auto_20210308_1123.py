# Generated by Django 3.0.5 on 2021-03-08 11:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sekolah', '0011_auto_20210218_1932'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sekolah',
            name='nip_kepsek',
        ),
        migrations.AlterField(
            model_name='sekolah',
            name='kepsek',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Kepala Sekolah'),
        ),
    ]
