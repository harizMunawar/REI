# Generated by Django 3.1.4 on 2020-12-21 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sekolah', '0015_auto_20201218_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sekolah',
            name='kepsek',
            field=models.CharField(max_length=255, null=True, verbose_name='Kepala Sekolah'),
        ),
    ]