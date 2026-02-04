from flask import Flask, render_template, request, redirect, url_for, flash, send_file, make_response
import mysql.connector
from fpdf import FPDF
import os

app = Flask(__name__)
app.secret_key = 'Chandra123'

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'db_transaksi_nilai_chandra'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

def deskripsi_otomatis(nilai):
    nilai = float(nilai)
    if nilai >= 90:
        return "Sangat Baik Nilai anda"
    elif nilai >= 80:
        return "Tingkatkan lagi nilai"
    elif nilai >= 70:
        return "Nilai Anda cukup baik tingkat kan lagi nilai nya"
    elif nilai >= 60:
        return "Nilai anda kurang, tingkatkan lagi nilainya "
    else:
        return "Nilai Anda Sangat Kurang Baik , perbaiki nilai nya"
class PDF(FPDF):
    def __init__(self, siswa=None, semester=None, tahun=None):
        super().__init__()
        self.siswa = siswa
        self.semester = semester
        self.tahun = tahun

    def header(self):
        if self.page_no() == 1:

            self.set_font("Arial", "B", 14)
            self.cell(0, 7, "PEMERINTAH DAERAH PROVINSI JAWA BARAT", ln=1, align="C")
            self.cell(0, 7, "DINAS PENDIDIKAN", ln=1, align="C")
            self.set_font("Arial", "B", 13)
            self.cell(0, 7, "SMK NEGERI 1 CIMAHI", ln=1, align="C")

            self.set_font("Arial", size=10)
            self.cell(0, 6, "Jl. Mahar Martanegara No.48, Kelurahan Utama, Kec. Cimahi Selatan", ln=1, align="C")

            self.ln(2)
            self.set_line_width(0.8)
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(6)

            self.set_font("Arial", "B", 12)
            self.cell(0, 10, "LAPORAN HASIL BELAJAR TENGAH SEMESTER", ln=1, align="C")
            self.ln(4)

    
            self.set_font("Arial", size=10)
            self.cell(35, 7, "Nama")
            self.cell(60, 7, f": {self.siswa['nama_chandra']}")
            self.cell(35, 7, "Kelas")
            self.cell(0, 7, f": {self.siswa['nama_kelas_chandra']}", ln=1)

            self.cell(35, 7, "NIS / NISN")
            self.cell(60, 7, f": {self.siswa['NIS_CHANDRA']}")
            self.cell(35, 7, "Semester")
            self.cell(0, 7, f": {self.semester}", ln=1)

            self.cell(35, 7, "Sekolah")
            self.cell(60, 7, ": SMKN 1 CIMAHI")
            self.cell(35, 7, "Tahun Ajaran")
            self.cell(0, 7, f": {self.tahun}", ln=1)

            self.ln(6)


def header_tabel(pdf):
    pdf.set_font("Arial", "B", 10)
    pdf.cell(10, 8, "No", 1, 0, "C")
    pdf.cell(60, 8, "Mata Pelajaran", 1, 0, "C")
    pdf.cell(25, 8, "Nilai Akhir", 1, 0, "C")
    pdf.cell(0, 8, "Deskripsi", 1, 1, "C")
    pdf.set_font("Arial", size=10)

def check_page_break(pdf, row_height):
    if pdf.get_y() + row_height > pdf.page_break_trigger:
        pdf.add_page()
        header_tabel(pdf)  

def cetak_nilai(pdf, judul, data):
    pdf.ln(4)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 8, judul, ln=1)

    header_tabel(pdf)

    pdf.set_font("Arial", size=10)
    no = 1

    for n in data:
        line_height = 8
        deskripsi = n['deskripsi_chandra']

        nb_lines = pdf.get_string_width(deskripsi) / 95
        row_height = max(line_height, int(nb_lines + 1) * line_height)

        check_page_break(pdf, row_height)

        x = pdf.get_x()
        y = pdf.get_y()

        pdf.cell(10, row_height, str(no), 1, 0, "C")
        pdf.cell(60, row_height, n['nama_mapel_chandra'], 1)
        pdf.cell(25, row_height, f"{n['nilai_akhir']:.0f}", 1, 0, "C")
        pdf.multi_cell(95, line_height, deskripsi, 1)

        pdf.set_xy(x, y + row_height)
        no += 1    


@app.route('/')
def data_nilai_chandra():
    try:
        selected_kelas = request.args.get("kelas")
        selected_tahun = request.args.get("tahun")
        selected_semester = request.args.get("semester")


        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)


        query = """
            SELECT
            a.id_nilai_chandra,
            a.NIS_CHANDRA,
            c.nama_chandra,
            d.nama_kelas_chandra,
            b.nama_mapel_chandra,
            a.nilai_tugas_chandra,
            a.nilai_uts_chandra,
            a.nilai_uas_chandra,
            a.deskripsi_chandra,
            a.semester_chandra,
            a.tahun_ajaran_chandra,
            ((a.nilai_tugas_chandra + a.nilai_uts_chandra + a.nilai_uas_chandra)/3) AS nilai_akhir
        FROM tbl_nilai_chandra a
        JOIN tbl_mapel_chandra b ON a.id_mapel_chandra = b.id_mapel_chandra
        JOIN tbl_siswa_chandra c ON a.NIS_CHANDRA = c.NIS_CHANDRA
        JOIN tbl_kelas_chandra d ON d.id_kelas_chandra=c.id_kelas_chandra
        WHERE 1=1
        """

        params = []

        if selected_kelas:
            query += " AND d.id_kelas_chandra = %s"
            params.append(selected_kelas)

        if selected_tahun:
            query += " AND a.tahun_ajaran_chandra = %s"
            params.append(selected_tahun)

        if selected_semester:
            query += " AND a.semester_chandra = %s"
            params.append(selected_semester)

        query += " ORDER BY a.tahun_ajaran_chandra, a.semester_chandra"
        cursor.execute(query, params)
        siswa = cursor.fetchall()


        cursor.execute("SELECT tahun_ajaran_chandra FROM tbl_nilai_chandra WHERE tahun_ajaran_chandra")
        daftar_tahun_chandra = cursor.fetchall()

        cursor.execute("SELECT NIS_CHANDRA, nama_chandra,id_kelas_chandra FROM tbl_siswa_chandra")
        daftar_siswa_chandra= cursor.fetchall()

        cursor.execute("SELECT id_kelas_chandra, nama_kelas_chandra FROM tbl_kelas_chandra")
        daftar_kelas_chandra = cursor.fetchall()

        cursor.execute("SELECT id_mapel_chandra, nama_mapel_chandra FROM tbl_mapel_chandra")
        daftar_mapel_chandra= cursor.fetchall()
        cursor.execute("""
            SELECT DISTINCT tahun_ajaran_chandra
            FROM tbl_nilai_chandra
            ORDER BY tahun_ajaran_chandra
        """)
        daftar_tahun_chandra = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template(
            'data_nilai_chandra.html',
            siswa=siswa,
            daftar_siswa_chandra=daftar_siswa_chandra,
            daftar_mapel_chandra=daftar_mapel_chandra,
            daftar_tahun_chandra=daftar_tahun_chandra,
            daftar_kelas_chandra=daftar_kelas_chandra,
            kelas=selected_kelas,
            tahun=selected_tahun,
            semester=selected_semester
        )

    except Exception as e:
        return f"<h3 style='color:red'>Gagal koneksi ke database: {e}</h3>"


@app.route("/cetak_rapor_chandra")
def cetak_rapor_chandra():
    kelas = request.args.get('kelas')
    semester = request.args.get('semester')
    tahun = request.args.get('tahun')

    if not kelas or not semester or not tahun:
        flash('Pilih kelas, semester, dan tahun dulu!', 'error')
        return redirect(url_for('data_nilai_chandra'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT s.*, k.nama_kelas_chandra
        FROM tbl_siswa_chandra s
        JOIN tbl_kelas_chandra k ON s.id_kelas_chandra = k.id_kelas_chandra
        WHERE s.id_kelas_chandra = %s
    """, (kelas,))
    daftar_siswa = cursor.fetchall()
    cursor.execute("SELECT nama_kelas_chandra FROM tbl_kelas_chandra WHERE id_kelas_chandra = %s", (kelas,))
    kelas_data = cursor.fetchone()  

    if not kelas_data:
        flash("Kelas tidak ditemukan!", "error")
        return redirect(url_for('data_nilai_chandra'))

    kelas_nama = kelas_data['nama_kelas_chandra']


    pdf_folder = "rapor_siswa"  
    os.makedirs(pdf_folder, exist_ok=True)

    pdf = PDF(semester=semester, tahun=tahun)
    for siswa in daftar_siswa:
        pdf = PDF(semester=semester, tahun=tahun)  
        pdf.siswa = siswa
        pdf.add_page()
        pdf.set_font("Arial", size=10)
        
        
        cursor.execute("""
            SELECT 
                m.nama_mapel_chandra,
                m.jenis_mapel_chandra,
                ((n.nilai_tugas_chandra+n.nilai_uts_chandra+n.nilai_uas_chandra)/3) AS nilai_akhir,
                n.deskripsi_chandra
            FROM tbl_nilai_chandra n
            JOIN tbl_mapel_chandra m ON n.id_mapel_chandra = m.id_mapel_chandra
            WHERE n.NIS_CHANDRA = %s
            AND n.semester_chandra = %s
            AND n.tahun_ajaran_chandra = %s
            ORDER BY m.jenis_mapel_chandra, m.nama_mapel_chandra
        """, (siswa['NIS_CHANDRA'], semester, tahun))
        nilai = cursor.fetchall()
     
        cetak_nilai(pdf, "A. Mapel Umum", [n for n in nilai if n['jenis_mapel_chandra'] == 'UMUM'])
        cetak_nilai(pdf, "B. Mapel Kejuruan", [n for n in nilai if n['jenis_mapel_chandra'] == 'Kejuruan'])
        cetak_nilai(pdf, "C. Mapel Pilihan", [n for n in nilai if n['jenis_mapel_chandra'] == 'Pilihan'])
        cursor.execute("""
            SELECT sakit, izin, alfa
            FROM tbl_absensi_chandra
            WHERE NIS_CHANDRA = %s
        """, (siswa['NIS_CHANDRA'],))
        absensi = cursor.fetchone() or {'sakit': 0, 'izin': 0, 'alfa': 0}

        pdf.set_font("Arial", "B", 10)
        pdf.cell(0, 8, "D. Kehadiran", ln=1)
        pdf.cell(10, 8, "No", 1, 0, "C")
        pdf.cell(60, 8, "Jenis Kehadiran", 1, 0, "C")
        pdf.cell(30, 8, "Jumlah (Hari)", 1, 1, "C")

        pdf.set_font("Arial", size=10)
        pdf.cell(10, 8, "1", 1, 0, "C")
        pdf.cell(60, 8, "Sakit", 1)
        pdf.cell(30, 8, str(absensi['sakit']), 1, 1, "C")

        pdf.cell(10, 8, "2", 1, 0, "C")
        pdf.cell(60, 8, "Izin", 1)
        pdf.cell(30, 8, str(absensi['izin']), 1, 1, "C")

        pdf.cell(10, 8, "3", 1, 0, "C")
        pdf.cell(60, 8, "Tanpa Keterangan (Alfa)", 1)
        pdf.cell(30, 8, str(absensi['alfa']), 1, 1, "C")

        pdf.ln(12)
        pdf.cell(60, 8, "Mengetahui,", ln=0, align="C")
        pdf.cell(60, 8, "Orang Tua/Wali", ln=0, align="C")
        pdf.cell(0, 8, "Wali Kelas", ln=1, align="C")
        pdf.ln(18)
        pdf.cell(60, 8, "__________________", ln=0, align="C")
        pdf.cell(60, 8, "__________________", ln=0, align="C")
        pdf.cell(0, 8, "__________________", ln=1, align="C")

        filename = f"Rapor_{siswa['nama_chandra'].replace(' ', '_')}-{kelas_nama}.pdf"
        pdf.output(os.path.join(pdf_folder, filename))

    cursor.close()
    conn.close()

    flash(f'Rapor berhasil disimpan di folder "{pdf_folder}"', 'success')
    return redirect(url_for('data_nilai_chandra'))


@app.route('/proses_nilai', methods=['POST'])
def proses_nilai():
    ChandraNis = request.form['ChandraNis']
    ChandraMapel = request.form['ChandraMapel']
    ChandraTugas = float(request.form['ChandraTugas'])
    ChandraUTS   = float(request.form['ChandraUTS'])
    ChandraUAS   = float(request.form['ChandraUAS'])
    nilai = (ChandraTugas + ChandraUTS + ChandraUAS) / 3
    ChandraDeskripsi = deskripsi_otomatis(nilai)
    ChandraS = request.form['ChandraS']
    ChandraAjaran = request.form['ChandraAjaran']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 1 FROM tbl_nilai_chandra
        WHERE
            NIS_CHANDRA=%s
            AND id_mapel_chandra=%s
            AND semester_chandra=%s
            AND tahun_ajaran_chandra=%s
    """, (ChandraNis, ChandraMapel, ChandraS, ChandraAjaran))

    if cursor.fetchone():
        flash('Nilai mapel ini untuk semester & tahun ajaran tersebut sudah ada!', 'error')
        return redirect(url_for('data_nilai_chandra'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT id_nilai_chandra FROM tbl_nilai_chandra ORDER BY id_nilai_chandra DESC LIMIT 1"
    )
    IDNILAICHANDRA = cursor.fetchone()

    next_number = 1

    if IDNILAICHANDRA:
        IDAKHIRCHANDRA = IDNILAICHANDRA['id_nilai_chandra']
        if IDAKHIRCHANDRA[-2:].isdigit():
            next_number = int(IDAKHIRCHANDRA[-2:]) + 1

    new_code_chandra = f"N10{next_number:02d}"


    cursor.execute("""
        INSERT INTO tbl_nilai_chandra (
            id_nilai_chandra,
            NIS_CHANDRA,
            id_mapel_chandra,
            nilai_tugas_chandra,
            nilai_uts_chandra,
            nilai_uas_chandra,
            deskripsi_chandra,
            semester_chandra,
            tahun_ajaran_chandra
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        new_code_chandra,
        ChandraNis,
        ChandraMapel,
        ChandraTugas,
        ChandraUTS,
        ChandraUAS,
        ChandraDeskripsi,
        ChandraS,
        ChandraAjaran
    ))

    conn.commit()
    cursor.close()
    conn.close()


    flash(f'Data dengan ID Nilai {new_code_chandra}  berhasil disimpan!', 'success')
    return redirect(url_for('data_nilai_chandra'))


@app.route('/edit_nilai_chandra/<nis>/<mapel>/<semester>/<tahun>')
def edit_nilai_chandra(nis, mapel, semester, tahun):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT a.*, b.nama_mapel_chandra
        FROM tbl_nilai_chandra a
        JOIN tbl_mapel_chandra b ON a.id_mapel_chandra=b.id_mapel_chandra
        WHERE
            a.NIS_chandra=%s
            AND b.nama_mapel_chandra=%s
            AND a.semester_chandra=%s
            AND a.tahun_ajaran_chandra=%s
    """, (nis, mapel, semester, tahun))

    nilai_edit = cursor.fetchone()

    if not nilai_edit:
        flash('Data nilai tidak ditemukan!', 'error')
        return redirect(url_for('data_nilai_chandra'))

    cursor.execute("SELECT * FROM tbl_mapel_chandra")
    daftar_mapel_chandra = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'data_nilai_chandra.html',
        nilai_edit=nilai_edit,
        daftar_mapel_chandra=daftar_mapel_chandra
    )


@app.route('/update_nilai_chandra', methods=['POST'])
def update_nilai_chandra():
    ChandraNis    = request.form['ChandraNis']
    ChandraMapel  = request.form['ChandraMapel']
    MapelLamaChandra = request.form['MapelLamaChandra']

    ChandraTugas  = float(request.form['ChandraTugas'])
    ChandraUTS    = float(request.form['ChandraUTS'])
    ChandraUAS    = float(request.form['ChandraUAS'])

    nilai = (ChandraTugas + ChandraUTS + ChandraUAS) / 3
    ChandraDeskripsi = deskripsi_otomatis(nilai)

    ChandraS      = request.form['ChandraS']
    SemesterLamaChandra = request.form['SemesterLamaChandra']

    ChandraAjaran = request.form['ChandraAjaran']
    AjaranLamaChandra = request.form['AjaranLamaChandra']

    conn = get_db_connection()
    cursor = conn.cursor()


    if ChandraS != SemesterLamaChandra:
        cursor.execute("""
            SELECT 1 FROM tbl_nilai_chandra
            WHERE
                NIS_chandra=%s
                AND id_mapel_chandra=%s
                AND semester_chandra=%s
                AND tahun_ajaran_chandra=%s
        """, (ChandraNis, ChandraMapel, ChandraS, ChandraAjaran))

        if cursor.fetchone():
            cursor.close()
            conn.close()
            flash(
                'Gagal update! Nilai mapel ini sudah ada di semester tersebut.',
                'error'
            )
            return redirect(url_for('data_nilai_chandra'))

    cursor.execute("""
        UPDATE tbl_nilai_chandra
        SET
            id_mapel_chandra=%s,
            nilai_tugas_chandra=%s,
            nilai_uts_chandra=%s,
            nilai_uas_chandra=%s,
            deskripsi_chandra=%s,
            semester_chandra=%s,
            tahun_ajaran_chandra=%s
        WHERE
            NIS_CHANDRA=%s
            AND id_mapel_chandra=%s
            AND semester_chandra=%s
            AND tahun_ajaran_chandra=%s
    """, (
        ChandraMapel, ChandraTugas, ChandraUTS, ChandraUAS,
        ChandraDeskripsi, ChandraS, ChandraAjaran,
        ChandraNis, MapelLamaChandra, SemesterLamaChandra, AjaranLamaChandra
    ))

    conn.commit()
    cursor.close()
    conn.close()

    flash('Data nilai berhasil diperbarui!', 'success')
    return redirect(url_for('data_nilai_chandra'))

@app.route('/hapus_nilai/<nis>/<mapel>/<semester>/<tahun>')
def hapus_nilai_chandra(nis, mapel, semester, tahun):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE a FROM tbl_nilai_chandra a
        JOIN tbl_mapel_chandra b ON a.id_mapel_chandra=b.id_mapel_chandra
        WHERE
            a.NIS_CHANDRA=%s
            AND b.nama_mapel_chandra=%s
            AND a.semester_chandra=%s
            AND a.tahun_ajaran_chandra=%s
    """, (nis, mapel, semester, tahun))


    conn.commit()
    cursor.close()
    conn.close()

    flash('Data nilai berhasil dihapus!', 'success')
    return redirect(url_for('data_nilai_chandra'))

    
if __name__ == '__main__':
    app.run(debug=True)
