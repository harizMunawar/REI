# Generated by Django 3.1.4 on 2020-12-18 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sekolah', '0014_auto_20201218_1831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sekolah',
            name='kepsek',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='sekolah',
            name='nip_kepsek',
            field=models.CharField(max_length=18, null=True, verbose_name='Nomor Induk'),
        ),
    ]
