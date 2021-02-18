# Generated by Django 3.0.5 on 2021-02-17 17:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sekolah', '0009_auto_20210217_1634'),
    ]

    operations = [
        migrations.RenameField(
            model_name='semester',
            old_name='tahunpelajaran',
            new_name='tahun_pelajaran',
        ),
        migrations.RenameField(
            model_name='tahunpelajaran',
            old_name='tahun_akhir',
            new_name='akhir',
        ),
        migrations.RenameField(
            model_name='tahunpelajaran',
            old_name='tahun_mulai',
            new_name='mulai',
        ),
        migrations.RemoveField(
            model_name='kelas',
            name='semester',
        ),
        migrations.RemoveField(
            model_name='kkm',
            name='semester',
        ),
        migrations.RemoveField(
            model_name='rapor',
            name='last_updated',
        ),
        migrations.AddField(
            model_name='kelas',
            name='tahun_pelajaran',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='kelas', to='sekolah.TahunPelajaran'),
        ),
        migrations.AddField(
            model_name='kkm',
            name='tahun_pelajaran',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='kkm', to='sekolah.TahunPelajaran'),
            preserve_default=False,
        ),
    ]