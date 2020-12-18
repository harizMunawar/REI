# Generated by Django 3.1.4 on 2020-12-18 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sekolah', '0013_remove_kelas_angkatan'),
    ]

    operations = [
        migrations.AddField(
            model_name='sekolah',
            name='kepsek',
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sekolah',
            name='nip_kepsek',
            field=models.CharField(default=None, max_length=18, verbose_name='Nomor Induk'),
            preserve_default=False,
        ),
    ]
