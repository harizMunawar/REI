# Generated by Django 3.1.4 on 2020-12-14 18:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sekolah', '0005_auto_20201215_0103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matapelajaran',
            name='kelompok',
            field=models.CharField(choices=[('NA', 'Normatif Adaptif'), ('WS', 'Kejuruan'), ('MULOK', 'Muatan Lokal')], max_length=5, verbose_name='Kelompok Mata Pelajaran'),
        ),
        migrations.CreateModel(
            name='KKM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pengetahuan', models.SmallIntegerField(max_length=100, verbose_name='KKM Pengetahuan')),
                ('keterampilan', models.SmallIntegerField(max_length=100, verbose_name='KKM Keterampilan')),
                ('matapelajaran', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sekolah.matapelajaran')),
                ('tgl_pendidikan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sekolah.tanggalpendidikan')),
            ],
        ),
    ]
