from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.db.models.deletion import SET_NULL
from django.db.models.fields.related import ForeignKey
from solo.models import SingletonModel
from django.dispatch import receiver
from helpers.choice import TINGKAT_SEKOLAH, SEMESTER_CHOICE, MATAPELAJARAN_CHOICE, KELAS_CHOICE
from guru.models import Guru

class Sekolah(SingletonModel):    
    nama = models.CharField(max_length=255)
    tingkat = models.CharField(verbose_name='Tingkat Sekolah', max_length=3, choices=TINGKAT_SEKOLAH)
    npsn = models.CharField(max_length=8)
    alamat = models.TextField()
    kode_pos = models.CharField(max_length=5)
    no_telepon = models.CharField(verbose_name='Nomor Telepon', max_length=20)
    kelurahan = models.CharField(max_length=50)
    kecamatan = models.CharField(max_length=50)
    kota = models.CharField(verbose_name='Kota/Kabupaten', max_length=50)
    provinsi = models.CharField(max_length=50)
    website = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return "Informasi Sekolah"

    class Meta:
        verbose_name = "Informasi Sekolah"


class Semester(models.Model):
    tahun_mulai = models.CharField(verbose_name='Tahun Mulai', max_length=4)
    tahun_akhir = models.CharField(verbose_name='Tahun Berakhir', max_length=4)
    semester = models.CharField(max_length=1, choices=SEMESTER_CHOICE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.tahun_mulai}/{self.tahun_akhir} {self.semester}'

@receiver(models.signals.pre_save, sender=Semester)
def only_one_is_active_instance(sender, instance, **kwargs):
    tp = Semester.objects.filter(is_active=True)
    if tp and instance.is_active:
        for tp in tp:                                        
            tp.is_active = False
            tp.save()
    
    tp = Semester.objects.filter(tahun_mulai=instance.tahun_mulai, tahun_akhir=instance.tahun_akhir, semester=instance.semester)
    if tp and instance not in tp:
        raise ValidationError('Nilai for that Mata Pelajaran in that Tanggal Pendidikan already exists')


class Jurusan(models.Model):
    nama = models.CharField(verbose_name='Nama Lengkap', max_length=255)
    singkat = models.CharField(verbose_name='Nama Singkat', max_length=10)

    def __str__(self):
        return self.singkat


class MataPelajaran(models.Model):
    nama = models.CharField(verbose_name='Nama Mata Pelajaran', max_length=255)
    singkat = models.CharField(verbose_name='Nama Singkat Mata Pelajaran', max_length=20)
    kelompok = models.CharField(verbose_name='Kelompok Mata Pelajaran', max_length=5, choices=MATAPELAJARAN_CHOICE)

    def __str__(self):
        return f'{self.singkat}/{self.kelompok}'

    def save(self, *args, **kwargs):
        self.singkat = str(self.singkat).upper()
        super(MataPelajaran, self).save(*args, **kwargs)


class KKM(models.Model):
    matapelajaran = models.ForeignKey(MataPelajaran, on_delete=models.CASCADE, related_name='kkm')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='kkm')
    pengetahuan = models.SmallIntegerField(verbose_name='KKM Pengetahuan')
    keterampilan = models.SmallIntegerField(verbose_name='KKM Keterampilan')

    def __str__(self):
        return f'{self.matapelajaran}({self.semester})'

    def save(self, *args, **kwargs):
        if self.pengetahuan < 0: self.pengetahuan = 0
        if self.pengetahuan > 100: self.pengetahuan = 100
        if self.keterampilan < 0: self.keterampilan = 0
        if self.keterampilan > 100: self.keterampilan = 100
        super(KKM, self).save(*args, **kwargs)

@receiver(models.signals.pre_save, sender=KKM)
def unique_together_tp_mapel(sender, instance, **kwargs):
    kkm = KKM.objects.filter(matapelajaran=instance.matapelajaran, semester=instance.semester)
    if kkm and instance not in kkm:
        raise ValidationError('Nilai for that Mata Pelajaran in that Tanggal Pendidikan already exists')


class Tingkat(models.Model):
    tingkat = models.SmallIntegerField(unique=True)

    def __str__(self):
        return str(self.tingkat)

    def save(self, *args, **kwargs):
        if self.tingkat < 1: self.tingkat = 1
        if self.tingkat > 13: self.tingkat = 13
        super(Tingkat, self).save(*args, **kwargs)

class Kelas(models.Model):
    tingkat = models.ForeignKey(Tingkat, on_delete=models.PROTECT, related_name='kelas')
    jurusan = models.ForeignKey(Jurusan, on_delete=models.PROTECT, related_name='kelas', null=True, blank=True)
    kelas = models.CharField(max_length=1, choices=KELAS_CHOICE)
    matapelajaran = models.ManyToManyField(MataPelajaran, related_name='kelas', blank=True)
    walikelas = models.ForeignKey(Guru, on_delete=models.SET_NULL, related_name='kelas', null=True, blank=True)
    semester = models.ForeignKey(Semester, on_delete=models.PROTECT, related_name='kelas', null=True)

    def __str__(self):
        if self.jurusan:
            return f'{self.tingkat}-{self.jurusan}-{self.kelas}-{self.semester}'
        else:
            return f'{self.tingkat}-{self.kelas}-{self.semester}'

    def save(self, *args, **kwargs):
         if not self.jurusan:
              self.jurusan = None
         super(Kelas, self).save(*args, **kwargs)

    def clean(self, *args, **kwargs):
         if not self.jurusan:
              self.jurusan = None
         super(Kelas, self).save(*args, **kwargs)

@receiver(models.signals.pre_save, sender=Kelas)
def unique_together_all(sender, instance, **kwargs):
    kelas = Kelas.objects.filter(tingkat=instance.tingkat, jurusan=instance.jurusan, kelas=instance.kelas, semester=instance.semester)
    if kelas and instance not in kelas:
        raise ValidationError('Kelas with all of that exact value already exists')