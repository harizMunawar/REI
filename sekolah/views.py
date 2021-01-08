from guru.models import Guru
from siswa.models import Absensi, Siswa
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models.query_utils import Q
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Kelas, MataPelajaran, Sekolah, Semester
from .forms import KelasForm, SekolahForm, SemesterForm
from django.db.models.deletion import ProtectedError
from django.core.paginator import Paginator
from REI.decorators import staftu_required, validdirs_required
from helpers import active_semester, get_initial, form_value, get_validwalikelas, get_validsiswabaru, get_validpelajaran, realkelas
from helpers.nilai_helpers import zip_eksnilai, zip_pelkkm, zip_pelnilai, zip_nilrapor
from django.contrib import messages

from helpers import generate_pdf
from django.http import HttpResponse, FileResponse

@method_decorator(login_required, name='dispatch')
class detail_sekolah(View):
    def get(self, request):
        request.session['page'] = 'Detail Sekolah'
        sekolah = Sekolah.objects.get()
        sekolah_form = SekolahForm(initial=get_initial(sekolah))
        context = {
            'sekolah_form': sekolah_form,
        }
        return render(request, 'pages/detail-sekolah.html', context)

    def post(self, request):
        sekolah_form = SekolahForm(request.POST)
        if sekolah_form.is_valid():
            Sekolah.objects.update(**form_value(sekolah_form))
            messages.success(request, 'Data Sekolah berhasil diubah')
            return redirect('detail-sekolah')
    
@method_decorator(staftu_required, name='dispatch')
class list_semester(View):
    def get(self, request):
        request.session['page'] = 'Daftar Semester'
        if 'search' in request.GET and request.GET['search'] != '':
            list_semester = Semester.objects.filter(
                Q(nama__istartswith=request.GET['search']) |
                Q(tahun_mulai__icontains=request.GET['search']) |
                Q(tahun_akhir__icontains=request.GET['search']) |
                Q(semester__icontains=request.GET['search'])
            ).order_by('-tahun_mulai', '-tahun_akhir', '-semester')
        else:
            list_semester = Semester.objects.all().order_by('-tahun_mulai', '-tahun_akhir', '-semester')
        
        paginator = Paginator(list_semester, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        number_of_pages = [(number+1) for number in range(page_obj.paginator.num_pages)]
        context = {
            'list_semester': page_obj,
            'page_obj': page_obj,
            'create_form': SemesterForm(),
            'number_of_pages': number_of_pages,
        }
        return render(request, 'pages/semester/semester.html', context)

@method_decorator(staftu_required, name='dispatch')
class buat_semester(View):
    def post(self, request):
        semester_form = SemesterForm(request.POST)
        try:
            if semester_form.is_valid():
                semester = Semester.objects.create(**form_value(semester_form), is_active=False)
                messages.success(request, 'Semester berhasil dibuat')
        except ValidationError:
            messages.error(request, 'Semester dengan data persis seperti itu sudah ada')
        finally:
            return redirect('list-semester')

@method_decorator(staftu_required, name='dispatch')
class aktifkan_semester(View):
    def get(self, request, semester):
        semester = Semester.objects.get(pk=semester)
        semester.is_active = True
        semester.save()
        return redirect('list-semester')

@method_decorator(staftu_required, name='dispatch')
class hapus_semester(View):
    def get(self, request, semester):
        try:
            Semester.objects.get(pk=semester).delete()
            messages.success(request, 'Semester berhasil dihapus')
        except ProtectedError:
            messages.error(request, 'Semester masih memiliki kelas aktif, tidak dapat dihapus')
        finally:
            return redirect('list-semester')

@method_decorator(login_required, name='dispatch')
class list_kelas(View):
    def get(self, request):
        request.session['page'] = 'Daftar Kelas'
        if 'search' in request.GET and request.GET['search'] != '':
            list_kelas = Kelas.objects.filter(
                Q(semester=active_semester()) & (
                Q(nama__icontains=request.GET['search']) |
                Q(walikelas__nama__icontains=request.GET['search']))
                ).order_by('jurusan', 'tingkat', 'kelas')
        else:
            list_kelas = Kelas.objects.filter(semester=active_semester()).order_by('jurusan', 'tingkat', 'kelas')
        
        kelas_form = KelasForm()
        paginator = Paginator(list_kelas, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        number_of_pages = [(number+1) for number in range(page_obj.paginator.num_pages)]
        context = {
            'page_obj': page_obj,
            'number_of_pages': number_of_pages,
            'list_kelas': list_kelas,
            'kelas_form': kelas_form,
        }
        return render(request, 'pages/kelas/kelas.html', context)

@method_decorator(staftu_required, name='dispatch')
class buat_kelas(View):
    def post(self, request):
        kelas_form = KelasForm(request.POST)
        try:
            if kelas_form.is_valid():
                kelas = Kelas.objects.create(**form_value(kelas_form), semester=active_semester())
                messages.success(request, 'Kelas berhasil dibuat, segera lengkapi data kelas tadi')
        except ValidationError:
            messages.error(request, 'Kelas itu sudah ada')
        finally:
            return redirect('list-kelas')

@method_decorator(staftu_required, name='dispatch')
class hapus_kelas(View):
    def get(self, request, kelas):
        try:
            Kelas.objects.get(nama=kelas, semester=active_semester()).delete()
            messages.success(request, f'Kelas {kelas} berhasil dihapus dari semester {active_semester()}')
        except ProtectedError:
            messages.error(request, 'Kelas masih memiliki siswa, tidak dapat dihapus')
        finally:
            return redirect('list-kelas')

@method_decorator(login_required, name='dispatch')
class detail_kelas(View):
    def get(self, request, kelas):
        request.session['page'] = f'Detail {kelas}'
        try:
            kelas = Kelas.objects.get(nama=kelas, semester=active_semester())
        except ObjectDoesNotExist:
            raise Http404

        if kelas.walikelas == request.user or request.user.is_superuser: auth_walikelas = True
        else: auth_walikelas = False 

        context = {
            'kelas': kelas,
            'auth_walikelas': auth_walikelas,
            'list_siswa': Siswa.objects.filter(kelas=kelas).order_by('nama'),
            'list_matapelajaran': MataPelajaran.objects.filter(kelas=kelas).order_by('kelompok', 'nama'),
        }
        return render(request, 'pages/kelas/detail-kelas.html', context)

@method_decorator(staftu_required, name='dispatch')
class walikelas_kelas(View):
    def get(self, request, kelas):
        request.session['page'] = f'Walikelas {kelas}'
        kelas = Kelas.objects.get(nama=kelas, semester=active_semester())
        active_walikelas = Guru.objects.get(kelas=kelas)
        valid_walikelas = get_validwalikelas()
        context = {
            'kelas': kelas,
            'active_walikelas': active_walikelas,
            'valid_walikelas': valid_walikelas,
        }
        return render(request, 'pages/kelas/ubah-walikelas.html', context)

@method_decorator(staftu_required, name='dispatch')
class ganti_walikelas(View):
    def post(self, request, kelas):
        kelas = Kelas.objects.get(nama=kelas, semester=active_semester())
        if request.POST['new_walikelas']:
            new_walikelas = Guru.objects.get(nip=request.POST['new_walikelas'])
            kelas.walikelas = new_walikelas
            kelas.save()
            messages.success(request, f'Walikelas untuk {kelas.nama} berhasil diubah')
        return redirect('walikelas-kelas', kelas=kelas.nama)

@method_decorator(staftu_required, name='dispatch')
class anggota_kelas(View):
    def get(self, request, kelas):
        request.session['page'] = f'Anggota Kelas {kelas}'
        kelas = Kelas.objects.get(nama=kelas, semester=active_semester())
        context = {
            'kelas': kelas,
            'list_siswa': Siswa.objects.filter(kelas=kelas).order_by('nama'),
            'siswa_baru': get_validsiswabaru()
        }
        return render(request, 'pages/kelas/anggota-kelas.html', context)

@method_decorator(staftu_required, name='dispatch')
class tambah_anggota(View):
    def get(self, request, kelas, siswa):
        siswa = Siswa.objects.get(nis=siswa)
        kelas = Kelas.objects.get(nama=kelas, semester=active_semester())
        siswa.kelas = kelas
        siswa.save()
        messages.success(request, f'{siswa.nama} berhasil menjadi anggota kelas {kelas.nama}')
        return redirect('anggota-kelas', kelas=kelas.nama)

@method_decorator(staftu_required, name='dispatch')
class hapus_anggota(View):
    def get(self, request, kelas, siswa):
        siswa = Siswa.objects.get(nis=siswa)
        siswa.kelas = None
        siswa.save()
        messages.success(request, f'{siswa.nama} berhasil dihapus dari anggota kelas {kelas}')
        return redirect('anggota-kelas', kelas=kelas)

@method_decorator(staftu_required, name='dispatch')
class pelajaran_kelas(View):
    def get(self, request, kelas):
        request.session['page'] = f'Matapelajaran {kelas}'
        kelas = Kelas.objects.get(nama=kelas, semester=active_semester())
        context = {
            'kelas': kelas,
            'list_matapelajaran': zip_pelkkm(MataPelajaran.objects.filter(kelas=kelas), active_semester()),
            'matapelajaran_baru': zip_pelkkm(get_validpelajaran(kelas.nama), active_semester()),
        }
        return render(request, 'pages/kelas/pelajaran-kelas.html', context)

@method_decorator(staftu_required, name='dispatch')
class tambah_pelajaran(View):
    def get(self, request, kelas, pelajaran):
        matapelajaran = MataPelajaran.objects.get(pk=pelajaran)
        kelas = Kelas.objects.get(nama=kelas, semester=active_semester())
        kelas.matapelajaran.add(matapelajaran)
        messages.success(request, f'{matapelajaran.nama} berhasil ditambahkan ke kelas {kelas.nama}')
        return redirect('pelajaran-kelas', kelas=kelas.nama)

@method_decorator(staftu_required, name='dispatch')
class hapus_pelajaran(View):
    def get(self, request, kelas, pelajaran):
        matapelajaran = MataPelajaran.objects.get(pk=pelajaran)
        kelas = Kelas.objects.get(nama=kelas, semester=active_semester())
        kelas.matapelajaran.remove(matapelajaran)
        messages.success(request, f'{matapelajaran.nama} berhasil dihapus dari kelas {kelas.nama}')
        return redirect('pelajaran-kelas', kelas=kelas.nama)

@method_decorator(login_required, name='dispatch')
@method_decorator(validdirs_required, name='dispatch')
class rapor_view(View):
    def get(self, request, nis, **kwargs):
        try:
            siswa = Siswa.objects.get(nis=nis)
            if siswa.gender == 'P': jenkel_siswa = 'Pria'
            else: jenkel_siswa = 'Wanita'
        except ObjectDoesNotExist:
            raise Http404
        sekolah = Sekolah.objects.get()
        if sekolah.tingkat == 'SMK': tingkat = 'Sekolah Menengah Kejuruan'
        elif sekolah.tingkat == 'SMA': tingkat = 'Sekolah Menengah Atas'
        elif sekolah.tingkat == 'SMP': tingkat = 'Sekolah Menengah Pertama'
        elif sekolah.tingkat == 'SD': tingkat = 'Sekolah Dasar'
        else:
            messages.error(request, 'Lengkapi data sekolah terlebih dahulu')
            return redirect('detail-sekolah')

        context = {
            'siswa': siswa,
            'jenkel_siswa': jenkel_siswa,
            'kelas': realkelas(siswa),
            'matapelajaran': zip_nilrapor(siswa, active_semester()),
            'ekskul': zip_eksnilai(siswa, active_semester()),
            'absensi': Absensi.objects.get_or_create(siswa=siswa, semester=active_semester())[0],
            'sekolah': sekolah,
            'tingkat_sekolah': tingkat,
        }

        generate_pdf(siswa, kwargs['pdf_dir'], context)
        with open(f'{kwargs["pdf_dir"]}/{siswa.nama}.pdf', 'rb') as result:            
            response = HttpResponse(result, content_type='application/pdf;')
            if request.GET['action'] == 'unduh':
                response['Content-Disposition'] = f'attachment; filename={siswa.nama}.pdf'
                response['Content-Transfer-Encoding'] = 'binary'
            elif request.GET['action'] == 'pratinjau':
                response['Content-Disposition'] = f'inline; filename={siswa.nama}.pdf'
                response['Content-Transfer-Encoding'] = 'binary'
            else:
                return redirect('dashboard')

            return response