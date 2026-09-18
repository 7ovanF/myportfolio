# Some Portfolio

Nama: Jovan Finesta

NPM: 2506599144

Kelas: PBP B

---

## Local run instructions
1. Clone the repository
```bash
git clone https://github.com/7ovanF/myportfolio && cd myportfolio
```
2. Enable venv and install dependencies
```bash
# Make venv
python -m venv env

# For POSIX shells
source env/bin/activate
# Powershell
env\bin\Activate.ps1 # honestly dont know
# csh
./env/bin/activate.csh
# fish
./env/bin/activate.fish
# yeah the point is activate venv

pip install -r requirements.txt
```
3. Run migrations
```bash
python manage.py migrate
```
4. Run server
```bash
python manage.py runserver
```
5. Access it through `localhost:8000` (default) in your web browser!

## Tugas 1

1. Ya, saya menggunakan beberapa elemen sesuai makna semantik (`<section>` digunakan seperti yang sudah digunakan pada template, `<header>` dan `<footer>` bawaan...). Elemen-elemen tersebut tidak membawa properti visual yang baru, namun membawa manfaat lain. Selain menambahkan arti semantik, juga digunakan oleh *assistive technology* untuk penyandang disabilitas dan memberikan informasi kepada search engine (sebagai bagian dari SEO). Referensi: https://www.jamesparker.dev/what-are-semantic-html-elements-and-why-are-they-important/.
2. Setelah mempelajari `grid` dan `flex`, web responsif tidak terlalu sulit (walau membutuhkan investasi waktu belajar). Misalnya, untuk memisah cards project sesuai ukuran layar, hanya perlu menggunakan media query untuk menyesuaikan kembali properti grid. Secara umum, untuk membuat tampilan versi mobile, saya perlu menyusun elemen-elemen menjadi lebih vertikal daripada horizontal seperti pada desktop.
3. Batasan belum terlalu terasa karena sebuah website portfolio memang tidak perlu memiliki konten dinamis. Namun, dapat terasa bahwa jika ditambahkan sistem database, proses pembangunan website bisa terbantu. Misalnya, saya menduplikasi bagian projects beberapa kali; jika data diiterasi dari database, struktur `div` tersebut tidak perlu diulang-ulang.

## Tugas 2

### Disclaimers
- Saya tanpa sengaja mengerjakan (hampir) keseluruhan Tugas 2 saat berniat mengerjakan Tutorial 2. Ini dikarenakan saya tidak memiliki menu Experiences sebelumnya, dan mengira bahwa bagian tersebut dimaksudkan untuk diadaptasi sesuai data yang ada. Untuk commit untuk Tugas 2 itu sendiri, saya akan tukar dengan commit yang berisi konten yang seharusnya untuk Tutorial 2. Mohon dimaklumi... 
- Saya mengimplementasikan *template inheritance* sebagai tambahan pada tugas ini.
- Sepertinya file upload via admin di-disable di environment deployment, maka di web PWS tidak akan muncul gambar apapun untuk sementara. 

### Jawaban Refleksi
1. Alur interaksi user:
    1. User mengirim HTTP request melalui URL yang didapatkan, entah PWS atau bukan.
    2. HTTP request di-route (details hidden) dan sampai pada server.
    3. Di server, dilakukan resolusi path dengan cara membaca entri-entri yang diregistrasi pada file `urls.py` project. File `urls.py` di project bisa meng-`include` file `urls.py` dari masing-masing app, atau bahkan langsung memuat sebuah path yang dihubungkan dengan sebuah view dalam app.
    4. Setelah meresolusi path yang tepat, method **view** yang terhubung pada path (diimport dari file `views.py`) tersebut akan dieksekusi, dan HTTP request akan di-pass.
    5. View melakukan generasi HTML dari **template** dan context yang disediakan — biasanya context mengandung data dari **model** (query melalui object-object di `models.py`) — dan mengembalikannya melalui sebuah HTTP response.
    6. HTTP response tersebut di-route kembali ke user dan HTML di-render oleh browser.

2. Pertama, tanpa sistem iterasi yang baik, banyak sekali struktur halaman HTML yang perlu diduplikasi, sehingga  mengubah struktur HTML menjadi lebih canggung. Kedua, sistem database mempermudah menambahkan data baru di, dalam kasus proyek ini, web portofolio seiring perkembangan karir karena sudah terdefinisi sebuah struktur yang terorganisasi.

3. `makemigrations` membuat kode Python yang menggunakan implementasi Django yang berfungsi untuk mengubah schema database dan menaruh kode tersebut di folder pada masing-masing app yang terkait. `migrate` dilakukan untuk mengeksekusi kode tersebut sehingga benar-benar diaplikasikan pada database; migrasi melalui `migrate` harus dilakukan dengan file-file migrasi yang dibuat oleh `makemigrations`.

    Semua perubahan pada schema database (melalui perubahan `models.py`) memerlukan migrasi ulang dengan `makemigrations` dan `migrate`. Contohnya, menambahkan model baru atau menambah/mengubah field pada model yang sudah ada.
    
## Tugas 3
#### Jelaskan mengapa kita menggunakan ModelForm pada Django alih-alih membuat form HTML secara manual. Selain itu, jelaskan pula mengapa kita diwajibkan menambahkan {% csrf_token %} pada form tersebut!
1. `ModelForm` sediaan Django sudah memberikan semuanya bagi user. Ia men-generate struktur HTML secara otomatis (yang dapat dimodifikasi dengan mendefinisikan ulang nested classnya `Meta`) dan juga meng-handle logika penerimaan dan pemrosesan POST request serta penyimpanan data itu sendiri.

    `csrf_token` menambahkan sebuah token yang digunakan untuk melakukan prevensi serangan CSRF, yaitu serangan di mana pihak jahat melakukan sebuah request ke server website melalui kredensial dari seorang user yang sudah terautentikasi. Dengan membandingkan token yang disimpan di server dengan yang dikirim bersama request client, server dapat memvalidasi bahwa request tersebut datang dari session asli, bukan diinstigasi oleh pihak lain. Django secara otomatis meng-include modul yang mewajibkan penggunaan token CSRF untuk form. 

#### Pada Tutorial 03, kita membahas format data JSON dan XML. Mengapa JSON lebih disukai dalam pengembangan aplikasi web modern dibandingkan XML?
2. JSON memiliki struktur yang sederhana, sehingga lebih mudah dibaca maupun disusun. JavaScript, sebagai salah satu penerima utama format JSON, dapat membaca format tersebut dengan lebih mudah. XML memiliki berbagai fitur yang lebih dibandingkan JSON, seperti spesifikasi struktur (schema) dan namespacing agar berbagai service bisa membaca informasi tertentu pada dokumen XML yang sama. Biasanya JSON cukup saja untuk aplikasi non-kritikal. Referensi: https://stackoverflow.com/questions/5615352/xml-and-json-advantages-and-disadvantages

#### Jelaskan alur yang terjadi saat kamu menggunakan fungsi view untuk mengembalikan data portofoliomu dalam bentuk JSON. Mengapa kita perlu melakukan proses serialization pada model Django sebelum datanya dikembalikan?
3. Alur fungsi view:
    1. Request client sampai, URL di-resolve, fungsi view terpanggil.
    2. Fungsi view membutuhkan konteks berupa data untuk dimasukkan ke template. View memanggil fungsi API yang me-return data.
    3. Fungsi API GET mengambil data dari database (`ModelName.objects.all()` dan sebagainya).
    4. Data tersebut di-serialize (yaitu dikonversi ke format yang bisa ditransmisi), yaitu ke bentuk JSON. Hasil serialisasi dikembalikan ke fungsi view.
    5. Fungsi view melakukan deserialization dari format JSON ke bentuk yang bisa dibaca Python.
    6. Fungsi view mengirim context ke template renderer dan mengirim hasil HTML ke client.
    
    Serialization diperlukan karena kedua sisi dalam request, yakni client dan server, belum tentu memiliki format yang sama dalam membaca data. Untuk mengirimkannya, server harus mengonversi ke bentuk yang universal dan mudah ditransmisi (misalnya JSON). Setelah diterima, data dapat di-deserialize oleh client ke bentuk yang dikenali olehnya tanpa memedulikan format awal yang dipakai server.

---

AI declaration in [AI-DECLARATION.md](AI-DECLARATION.md)