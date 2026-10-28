# Sub-Record Studio Website (Official Portal)

Website resmi untuk **Sub-Record Studio** (Yogyakarta) — studio rekaman, produksi musik, aransemen, video klip cover song, serta talent management & entertainment.

---

## 🚀 Fitur Utama & Pembaruan Sistem (2026)

### 1. Auto-Fetch & Sinkronisasi YouTube Otomatis (Zero Coding Manual)
- **Otomatis Tanpa Sentuh Kode:** Terintegrasi dengan GitHub Actions (`.github/workflows/sync-youtube.yml`) yang berjalan otomatis setiap 6 jam untuk memeriksa video baru dari channel YouTube [@subrecordstudio](https://www.youtube.com/@subrecordstudio).
- **1-Click Local Sync:** Tersedia file `sync-youtube.bat` (atau jalankan `python scripts/sync-youtube.py`). Cukup double-click untuk menarik dan mengkategorikan video YouTube terbaru secara lokal seketika.
- **Kategorisasi Otomatis:** Sistem secara otomatis mendeteksi dan mengelompokkan video ke dalam:
  - *Original Song & Single*
  - *Live Sessions & Wedding Performances*
  - *Cover Songs*
  - *Audio Production & Mixing Tips*
- **Inline Video Modal Popup:** Pengunjung dapat menonton video langsung di dalam website tanpa perlu meninggalkan halaman (zero bounce rate).

### 2. Halaman Pricelist Interaktif & Responsif (`pricelist.html`)
- Menggantikan gambar statis dengan kartu harga interaktif (responsive HTML/CSS):
  - **Cover Song Package:** Promo spesial 400k (Free aransemen akustik, 4 jam rekaman, mixing-mastering, shooting & editing video klip).
  - **All-In Recording Package:** Akustik (750k), Full Band (1.500k).
  - **Mixing & Mastering:** Akustik (500k), Full Band (mulai 1.000k tergantung kompleksitas).
  - **Music Composing & Aransemen:** Akustik (350k), Full Band (1.000k), Orkestra (1.500k), Full Song Production (5.000k).
  - **Live Entertainment:** Reguler kafe (300k), Akustik (800k), Live Band (2.000k), Brass Band (3.500k), Session Player (350k).
- **Filter Tabs:** Pengunjung dapat memfilter paket: *Semua Layanan*, *Recording*, *Paket Cover*, *Composing*, dan *Entertainment*.
- **Direct WhatsApp Booking:** Setiap paket memiliki tombol booking WhatsApp langsung dengan template pesan konsultasi otomatis.

### 3. Halaman Talent & Artis Lengkap
- Basis data terstruktur di `data/artists.json`.
- Profil lengkap talent:
  - **Cindy Leivana** (`cindy-leivana.html`): Frontwoman *Cindy and The Fairies*, Juara 2 FLS2N Nasional, Finalis La Academia Junior 2 SCTV.
  - **KEZHIKI** (`kezhiki.html`): Singer-songwriter hits *"Sunflowers"* & *"It's You"*.
  - **Marrez** (`marrez.html`): Solois pop balada single perdana *"Bersamanya"*.
  - **Anton Yoga** (`anton-yoga.html`): Vocal Director & Arranger (OST *"Langit Senja"*).
- **Pemisahan Diskografi yang Jelas:**
  - *Karya Bersama Sub-Record Studio* (Single resmi yang direkam/diproduksi di SRS).
  - *Diskografi Lengkap di Spotify* (Embed player Spotify untuk lagu-lagu awal/mandiri talent).
- **Talent Booking CTA:** Tombol khusus untuk mengundang atau booking talent ke acara pernikahan, gathering, atau kafe.

---

## 📁 Struktur File & Direktori

```
subrecordstudio/
├── .github/
│   └── workflows/
│       └── sync-youtube.yml         # GitHub Actions cron auto-sync YouTube
├── data/
│   ├── youtube-portfolio.json       # Basis data video portofolio hasil sync
│   └── artists.json                 # Basis data profil & rilisan talent artis
├── scripts/
│   └── sync-youtube.py              # Script sinkronisasi & kategorisasi YouTube
├── js/
│   ├── youtube-portfolio.js         # Engine dynamic render & video modal player
│   └── active.js                    # Inisialisasi plugin template
├── css/
│   └── pricelist.css                # Stylesheet lengkap komponen pricelist
├── img/
│   └── bg-img/                      # Aset gambar & artwork
├── index.html                       # Beranda (Hero slider, Top 6 portofolio, Pricelist teaser, Talent)
├── latest-releases.html             # Portofolio lengkap dengan filter kategori
├── pricelist.html                   # Daftar harga & paket layanan interaktif
├── artist.html                      # Daftar seluruh talent artis
├── cindy-leivana.html               # Profil & diskografi Cindy Leivana
├── kezhiki.html                     # Profil & diskografi KEZHIKI
├── marrez.html                      # Profil & diskografi Marrez
├── anton-yoga.html                  # Profil & kredensial Anton Yoga
├── blog.html                        # Tentang Sub-Record Studio (About Us)
├── contact.html                     # Kontak, WhatsApp, dan Google Maps studio
├── style.css                        # Stylesheet utama website
└── sync-youtube.bat                 # Eksekusi 1-click update YouTube lokal di Windows
```

---

## 🛠️ Panduan untuk Web Developer

### 1. Cara Sinkronisasi YouTube Secara Lokal
Jika ada video baru di YouTube dan ingin segera muncul di website lokal:
1. Double-click file `sync-youtube.bat` di folder project, **atau**
2. Buka terminal lalu jalankan:
   ```powershell
   python scripts/sync-youtube.py
   ```
3. Refresh browser di `index.html` atau `latest-releases.html`.

### 2. Cara Otomatisasi via GitHub (CI/CD)
1. Push repository ke GitHub:
   ```bash
   git add .
   git commit -m "feat: setup automated youtube sync & revamped pricelist"
   git push origin main
   ```
2. Workflow GitHub Actions di `.github/workflows/sync-youtube.yml` akan berjalan otomatis setiap 6 jam (atau dapat dijalankan manual lewat tab **Actions** > **Sync YouTube Portfolio** > **Run workflow**).
3. Jika ada video baru, GitHub Action akan otomatis meng-commit data terbaru ke branch repository Anda!

### 3. Cara Mengubah Harga atau Menambah Talent
- **Ubah Harga:** Buka `pricelist.html` atau edit nilai pada elemen `.srs-price-amount`.
- **Edit Talent:** Buka `data/artists.json` dan file HTML artis terkait (`artist.html`, `cindy-leivana.html`, dst).

---

© 2026 Sub-Record Studio Yogyakarta • *Quality is our priority!*
