# Generated by Django 3.1.4 on 2020-12-14 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sekolah',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=255)),
                ('tingkat', models.CharField(choices=[('SD', 'Sekolah Dasar'), ('SMP', 'Sekolah Menengah Pertama'), ('SMA', 'Sekolah Menengah Atas'), ('SMK', 'Sekolah Kejuruan')], max_length=3, verbose_name='Tingkat Sekolah')),
                ('npsn', models.CharField(max_length=8)),
                ('alamat', models.TextField()),
                ('kode_pos', models.CharField(max_length=5)),
                ('no_telepon', models.CharField(max_length=20, verbose_name='Nomor Telepon')),
                ('kelurahan', models.CharField(max_length=50)),
                ('kecamatan', models.CharField(max_length=50)),
                ('kota', models.CharField(max_length=50, verbose_name='Kota/Kabupaten')),
                ('provinsi', models.CharField(max_length=50)),
                ('website', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
            ],
            options={
                'verbose_name': 'Informasi Sekolah',
            },
        ),
    ]
