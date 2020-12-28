# Generated by Django 3.1.4 on 2020-12-22 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sekolah', '0016_auto_20201221_1745'),
        ('siswa', '0006_auto_20201217_0022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nilai',
            name='keterampilan',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='nilai',
            name='pengetahuan',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='nilai',
            name='semester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nilai', to='sekolah.semester'),
        ),
        migrations.CreateModel(
            name='Absensi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('izin', models.PositiveSmallIntegerField()),
                ('sakit', models.PositiveSmallIntegerField()),
                ('bolos', models.PositiveSmallIntegerField()),
                ('semester', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='absensi', to='sekolah.semester')),
                ('siswa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='absensi', to='siswa.siswa')),
            ],
        ),
    ]