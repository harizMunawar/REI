from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.db.utils import IntegrityError
from solo.models import SingletonModel
from django.dispatch import receiver
from helpers.choice import JENIS_EKSKUL, TINGKAT_SEKOLAH, SEMESTER_CHOICE, MATAPELAJARAN_CHOICE, KELAS_CHOICE, TINGKAT_KELAS_CHOICE
from guru.models import Guru
import os

class Sekolah(SingletonModel):    
    nama = models.CharField(max_length=255)
    tingkat = models.CharField(verbose_name='Tingkat Sekolah', max_length=3, choices=TINGKAT_SEKOLAH)
    tingkat_verbose = models.CharField(max_length=255, null=True, blank=True, verbose_name='Tingkat Sekolah (Lengkap)')
    npsn = models.CharField(max_length=8)
    alamat = models.CharField(max_length=255)
    kode_pos = models.CharField(max_length=5)
    no_telepon = models.CharField(verbose_name='Nomor Telepon', max_length=20)
    kelurahan = models.CharField(max_length=50)
    kecamatan = models.CharField(max_length=50)
    kota = models.CharField(verbose_name='Kota/Kabupaten', max_length=50)
    provinsi = models.CharField(max_length=50)
    website = models.CharField(max_length=50)
    email = models.EmailField()
    kepsek = models.OneToOneField(Guru, verbose_name='Kepala Sekolah', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "Informasi Sekolah"

    class Meta:
        verbose_name = "Informasi Sekolah"

@receiver(models.signals.pre_save, sender=Sekolah)
def presave_sekolah(sender, instance, **kwargs):
    if instance.tingkat == 'SMK': instance.tingkat_verbose = 'Sekolah Menengah Kejuruan'
    elif instance.tingkat == 'SMA': instance.tingkat_verbose = 'Sekolah Menengah Atas'
    elif instance.tingkat == 'SMP': instance.tingkat_verbose = 'Sekolah Menengah Pertama'
    elif instance.tingkat == 'SD': instance.tingkat_verbose = 'Sekolah Dasar'

class TahunPelajaran(models.Model):
    mulai = models.CharField(verbose_name='Tahun Mulai', max_length=4)
    akhir = models.CharField(verbose_name='Tahun Berakhir', max_length=4)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.mulai}/{self.akhir}'

@receiver(models.signals.pre_save, sender=TahunPelajaran)
def presave_tp(sender, instance, **kwargs):
    try:
        tp = TahunPelajaran.objects.filter(is_active=True)
        if tp and instance.is_active:
            for tp in tp:                                        
                tp.is_active = False
                tp.save()
    except ObjectDoesNotExist:
        pass

    try:
        tp = TahunPelajaran.objects.filter(mulai=instance.mulai, akhir=instance.akhir)
        if tp and instance not in tp:
            raise ValidationError('That Tahun Pelajaran already exists')
    except ObjectDoesNotExist:
        pass

@receiver(models.signals.post_save, sender=TahunPelajaran)
def postsave_tp(sender, instance, created, **kwargs):
    if created:
        Semester.objects.get_or_create(tahun_pelajaran=instance, semester='Ganjil', is_active=False)
        Semester.objects.get_or_create(tahun_pelajaran=instance, semester='Genap', is_active=False)

class Semester(models.Model):
    nama = models.CharField(max_length=255, editable=False, null=True)
    tahun_pelajaran = models.ForeignKey(TahunPelajaran, on_delete=models.CASCADE, related_name='semester')
    semester = models.CharField(max_length=6, choices=SEMESTER_CHOICE)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.nama

    def save(self, *args, **kwargs):
        self.nama = f'{self.tahun_pelajaran} {self.semester}'
        super(Semester, self).save(*args, **kwargs)
        

@receiver(models.signals.pre_save, sender=Semester)
def only_one_is_active_instance(sender, instance, **kwargs):
    try:
        if instance.is_active:
            tp = TahunPelajaran.objects.get(semester=instance)
            tp.is_active = True
            tp.save()
            semester = Semester.objects.filter(is_active=True)
            if semester:
                for semester in semester:                                        
                    semester.is_active = False
                    semester.save()
    except ObjectDoesNotExist:
        pass

    try:
        semester = Semester.objects.filter(tahun_pelajaran=instance.tahun_pelajaran, semester=instance.semester)
        if semester and instance not in semester:
            raise ValidationError('That Semester already exists')
    except ObjectDoesNotExist:
        pass
    except ValidationError:
        pass


class Jurusan(models.Model):
    nama = models.CharField(verbose_name='Nama Lengkap', max_length=255)
    singkat = models.CharField(verbose_name='Nama Singkat', max_length=10, null=True, blank=True)

    def __str__(self):
        return self.singkat or self.nama

@receiver(models.signals.pre_save, sender=Jurusan)
def unique_together_nama_singkat(sender, instance, **kwargs):
    try:
        jurusan = Jurusan.objects.filter(nama=instance.nama, singkat=instance.singkat)
        if jurusan and instance not in jurusan:
            raise ValidationError('That Jurusan already exists')
    except ObjectDoesNotExist:
        pass


class MataPelajaran(models.Model):
    nama = models.CharField(verbose_name='Nama Mata Pelajaran', max_length=255)
    singkat = models.CharField(verbose_name='Nama Singkat Mata Pelajaran', max_length=20, null=True, blank=True, default=None)
    kelompok = models.CharField(verbose_name='Kelompok Mata Pelajaran', max_length=5, choices=MATAPELAJARAN_CHOICE)

    def __str__(self):
        if self.singkat: return f'{self.singkat}/{self.kelompok}'
        else: return f'{self.nama}/{self.kelompok}'

    def save(self, *args, **kwargs):
        if self.singkat: self.singkat = str(self.singkat).upper()
        super(MataPelajaran, self).save(*args, **kwargs)

@receiver(models.signals.pre_save, sender=MataPelajaran)
def unique_together_all_mapel(sender, instance, **kwargs):
    try:
        mapel = MataPelajaran.objects.filter(nama=instance.nama, singkat=instance.singkat, kelompok=instance.kelompok)
        if mapel and instance not in mapel:
            raise ValidationError('That Mata Pelajaran already exists')
    except ObjectDoesNotExist:
        pass


class KKM(models.Model):
    matapelajaran = models.ForeignKey(MataPelajaran, on_delete=models.CASCADE, related_name='kkm')
    tahun_pelajaran = models.ForeignKey(TahunPelajaran, on_delete=models.CASCADE, related_name='kkm')
    pengetahuan = models.SmallIntegerField(verbose_name='KKM Pengetahuan', default=0)
    keterampilan = models.SmallIntegerField(verbose_name='KKM Keterampilan', default=0)

    def __str__(self):
        return f'{self.matapelajaran}({self.tahun_pelajaran})'

@receiver(models.signals.pre_save, sender=KKM)
def unique_together_tp_mapel(sender, instance, **kwargs):
    try:
        kkm = KKM.objects.filter(matapelajaran=instance.matapelajaran, tahun_pelajaran=instance.tahun_pelajaran)
        if kkm and instance not in kkm:
            raise ValidationError('Nilai for that Mata Pelajaran in that Tanggal Pendidikan already exists')
    except ObjectDoesNotExist:
        pass

@receiver(models.signals.post_save, sender=KKM)
def set_kkm_range(sender, instance, **kwargs):
    if int(instance.pengetahuan) < 0 or int(instance.pengetahuan) > 100 or int(instance.keterampilan) < 0 or int(instance.keterampilan) > 100:
        if int(instance.pengetahuan) < 0 or int(instance.pengetahuan) > 100:
            instance.pengetahuan = 0
        if int(instance.keterampilan) < 0 or int(instance.keterampilan) > 100:
            instance.keterampilan = 0
        instance.save()
        raise IntegrityError


class Kelas(models.Model):
    tingkat = models.CharField(max_length=3, choices=TINGKAT_KELAS_CHOICE)
    jurusan = models.ForeignKey(Jurusan, on_delete=models.PROTECT, related_name='kelas', null=True, blank=True)
    kelas = models.CharField(max_length=1, choices=KELAS_CHOICE)
    matapelajaran = models.ManyToManyField(MataPelajaran, related_name='kelas', blank=True)
    walikelas = models.ForeignKey(Guru, on_delete=models.SET_NULL, related_name='kelas', null=True, blank=True)
    tahun_pelajaran = models.ForeignKey(TahunPelajaran, on_delete=models.PROTECT, related_name='kelas', null=True)
    nama = models.CharField(max_length=255, editable=False, null=True, blank=True)

    def __str__(self):
        return f'{self.tingkat}-{self.jurusan}-{self.kelas} {self.tahun_pelajaran}'

    def save(self, *args, **kwargs):
        if not self.jurusan:
            self.nama = f'{self.tingkat}-{self.kelas}'
            self.jurusan = None
        else:
            self.nama = f'{self.tingkat}-{self.jurusan}-{self.kelas}'
        super(Kelas, self).save(*args, **kwargs)

@receiver(models.signals.pre_save, sender=Kelas)
def unique_together_all_kelas(sender, instance, **kwargs):
    try:
        kelas = Kelas.objects.filter(tingkat=instance.tingkat, jurusan=instance.jurusan, kelas=instance.kelas, tahun_pelajaran=instance.tahun_pelajaran)
        if kelas and instance not in kelas:
            raise ValidationError('Kelas with all of that exact value already exists')
    except ObjectDoesNotExist:
        pass


class Ekskul(models.Model):
    nama = models.CharField(max_length=255)
    jenis = models.CharField(max_length=255, choices=JENIS_EKSKUL, verbose_name='Jenis Ekskul')

    def __str__(self):
        return self.nama
        
@receiver(models.signals.pre_save, sender=Ekskul)
def unique_together_all_ekskul(sender, instance, **kwargs):
    try:
        ekskul = Ekskul.objects.filter(nama=instance.nama, jenis=instance.jenis)
        if ekskul and instance not in ekskul:
            raise ValidationError('Ekskul with all of that exact value already exists')
    except ObjectDoesNotExist:
        pass

class Rapor(models.Model):
    from siswa.models import Siswa
    siswa = models.ForeignKey(Siswa, related_name='rapor', on_delete=models.CASCADE, null=True)
    semester = models.ForeignKey(Semester, related_name='rapor', on_delete=models.CASCADE)
    rapor = models.TextField(verbose_name='Lokasi PDF Rapor', null=True)

    def __str__(self):
        return f'{self.siswa} - {self.semester}'

@receiver(models.signals.pre_save, sender=Rapor)
def rapor_pre_save(sender, instance, **kwargs):
    try:
        rapor = Rapor.objects.filter(siswa=instance.siswa, semester=instance.semester)
        if rapor and instance not in rapor:
            raise ValidationError('That Siswa already have Rapor for this semester')
    except ObjectDoesNotExist:
        pass

    try:
        old_file = sender.objects.get(pk=instance.pk).rapor
    except sender.DoesNotExist:
        return False
    new_file = instance.rapor
    if not old_file == new_file:
        if os.path.isfile(old_file):
            os.remove(old_file)

@receiver(models.signals.post_delete, sender=Rapor)
def auto_delete_rapor_on_delete(sender, instance, **kwargs):
    if instance.rapor:
        if os.path.isfile(instance.rapor):
            os.remove(instance.rapor)