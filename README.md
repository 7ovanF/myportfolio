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

---

AI declaration in [AI-DECLARATION.md](AI-DECLARATION.md)