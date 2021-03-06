# Generated by Django 3.0.5 on 2021-03-08 10:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('guru', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gelar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tingkat_gelar', models.CharField(choices=[('D1', 'Diploma 1'), ('D2', 'Diploma 2'), ('D3', 'Diploma 3'), ('D4', 'Diploma 4'), ('S1', 'Sarjana'), ('S2', 'Magister'), ('S3', 'Doktor')], max_length=2)),
                ('verbose_gelar', models.CharField(blank=True, max_length=255, null=True)),
                ('jurusan', models.CharField(choices=[('Administrasi', (('A.B.', 'Administrasi Bisnis'), ('Pn.', 'Administrasi Fiskal'), ('Adm.', 'Administrasi Negara'), ('A.P.', 'Administrasi Perkantoran'), ('I.P.', 'Ilmu Perpustakaan'))), ('Ekonomi', (('Ak.', 'Akuntansi'), ('E.', 'Ilmu Ekonomi'), ('E.', 'Manajemen'))), ('Kesehatan', (('Farm.', 'Farmasi'), ('Gz.', 'Ilmu Gizi'), ('Keb.', 'Kebidanan'), ('Ked.', 'Kedokteran'), ('K.G.', 'Kedokteran Gigi'), ('K.H.', 'Kedokteran Hewan'), ('Kep.', 'Keperawatan'), ('K.M.', 'Kesehatan Masyrakat'), ('Psi.', 'Psikologi'))), ('Kesenian', (('Ds.', 'Desain Komunikasi Visual'), ('Ds.', 'Desain Produk'), ('Sn.', 'Seni Kriya'), ('Sn.', 'Seni Musik'), ('Sn.', 'Seni Rupa'), ('Sn.', 'Seni Tari'))), ('Ilmu Budaya', (('Hum.', 'Humaniora'), ('Fil.', 'Filsafat'), ('Hum.', 'Ilmu Sejarah'), ('Par.', 'Pariwisata'), ('S.', 'Sastra'))), ('Matematika & IPA', (('Si.', 'Astronomi'), ('Si.', 'Biologi'), ('Si.', 'Fisika'), ('Si.', 'Geofisika'), ('Si.', 'Geologi'), ('Si.', 'Kimia'), ('Si.', 'Matematika'), ('Stat.', 'Statistika'))), ('Pendidikan', (('Pd.', 'Bimbingan Konseling'), ('Pd.', 'Kebijakan Pendidikan'), ('Pd.', 'Manajemen Pendidikan'), ('Pd.', 'Pendidikan Luar Biasa'), ('Pd.', 'Pendidikan Luar Sekolah'), ('Pd.', 'PGPAUD'), ('Pd.', 'PGSD'), ('Pd.', 'Teknologi Pendidikan'))), ('Pertanian', (('P.', 'Agribisnis'), ('P.', 'Agroteknologi'), ('P.', 'Ilmu Tanah'), ('Hut.', 'Kehutanan'), ('Pi.', 'Perikanan'), ('T.P.', 'Teknologi Hasil Pertanian'))), ('Sosial', (('Ant.', 'Antropologi Sosial'), ('H.Int.', 'Hubungan Internasional'), ('H.', 'Hukum'), ('Si.', 'Geografi'), ('Sos.', 'Ilmu Kesejahteraan Sosial'), ('I.Kom.', 'Ilmu Komunikasi'), ('IP.', 'Ilmu Politik'), ('Sos.', 'Kriminologi'), ('Sos.', 'Sosiologi'))), ('Teknik', (('Ars.', 'Arsitektur'), ('Kom.', 'Ilmu Komputer'), ('Kom.', 'Sistem Informasi'), ('Kom.', 'Teknik Informatika'), ('T.', 'Teknik Bioproses'), ('T.', 'Teknik Elektro'), ('T.', 'Teknik Elektronika'), ('T.', 'Teknik Fisika'), ('T.', 'Teknik Geodesi'), ('T.', 'Teknik Geofisika'), ('T.', 'Teknik Geologi'), ('T.', 'Teknik Industri'), ('T.', 'Teknik Kelautan'), ('T.', 'Teknik Kimia'), ('T.', 'Teknik Telekomunikasi'), ('T.', 'Teknik Lingkungan'), ('T.', 'Teknik Metalurgi'), ('T.', 'Teknik Mekatronika'), ('T.', 'Teknik Mesin'), ('T.', 'Teknik Nuklir'), ('T.', 'Teknik Otomotif'), ('T.', 'Teknik Permniyakan'), ('T.', 'Teknik Pertambangan'), ('T.', 'Teknik Sipil'), ('T.', 'Teknik Transportasi Laut')))], max_length=255)),
                ('verbose_jurusan', models.CharField(blank=True, max_length=255, null=True)),
                ('universitas', models.CharField(max_length=255)),
                ('guru', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
