# 🎵 Lana Music Bot

**Lana** adalah bot musik Discord modern dan kaya fitur, dibangun dengan Python menggunakan library `discord.py`. Bot ini dirancang untuk memberikan pengalaman mendengarkan musik yang mulus dan interaktif di server Discord Anda, sepenuhnya dikendalikan melalui slash command (`/`).

---

## ✨ Fitur Utama

- **Antarmuka Slash Command:** Mudah digunakan, modern, dan terintegrasi langsung dengan Discord.
- **Pemutaran Musik Berkualitas:** Putar lagu dari YouTube dengan kualitas audio terbaik.
- **Sistem Antrean (Queue):** Tambahkan beberapa lagu ke antrean dan biarkan bot memutarnya secara berurutan.
- **Kontrol Penuh:** Panel kontrol interaktif dengan tombol Play/Pause, Skip, dan Stop.
- **Pengaturan Server:** Panel `/settings` per-server untuk mengaktifkan/menonaktifkan fitur seperti Autoplay (khusus admin).
- **Struktur Profesional:** Kode terorganisir dengan baik menggunakan layout `src` dan Cogs untuk kemudahan pengembangan.

---

## 📜 Izin (Permissions) yang Dibutuhkan

Pastikan Lana memiliki izin berikut di server Anda, terutama di channel teks dan suara tempat ia digunakan:

- **Read Messages/View Channels:** Melihat perintah yang Anda ketik.
- **Send Messages:** Membalas perintah dan mengirim panel kontrol.
- **Embed Links:** Menampilkan panel pemutar musik dengan rapi.
- **Connect:** Bergabung ke voice channel.
- **Speak:** Memutar audio di voice channel.

---

## 📂 Struktur Proyek

```
LANA/
├── src/
│   └── bot_lana/
│       ├── cogs/
│       │   ├── general.py      # /ping
│       │   ├── help.py         # /help
│       │   └── music/
│       │       ├── player.py   # /play, /leave
│       │       ├── queue.py    # /queue, /skip, /nowplaying
│       │       └── settings.py # /settings
│       ├── core/
│       │   └── views.py        # Kelas UI untuk tombol
│       ├── data/
│       │   └── settings.json   # Penyimpanan pengaturan
│       └── bot.py              # Logika inti bot
│
├── .env                  # Token rahasia
├── main.py               # Titik masuk bot
├── pyproject.toml        # Konfigurasi proyek Python
└── requirements.txt      # Daftar dependensi
```

---

## 🚀 Cara Menjalankan Bot

### 1. Prasyarat

- Python 3.10 atau lebih baru
- FFmpeg terinstal di sistem Anda

#### Instalasi FFmpeg

- **Linux (Debian/Ubuntu/Kali):**
  ```
  sudo apt update && sudo apt install ffmpeg
  ```
- **macOS (Homebrew):**
  ```
  brew install ffmpeg
  ```
- **Windows (Chocolatey):**
  ```
  choco install ffmpeg
  ```
- **Alternatif:** Unduh dari situs resmi FFmpeg dan tambahkan ke PATH sistem Anda.

---

### 2. Download & Setup Awal

#### Dapatkan Kode Sumber

- **Opsi A: Menggunakan Git (Direkomendasikan)**
  ```
  git clone https://github.com/DeathKnight727/lana.git
  cd lana
  ```
- **Opsi B: Download ZIP**
  - Kunjungi repositori GitHub, klik tombol hijau **Code**, lalu pilih **Download ZIP**. Ekstrak file ZIP di komputer Anda.

#### Buat File `.env`

Buat file bernama `.env` di folder utama proyek dan isi dengan token bot Anda:

```
DISCORD_TOKEN="TOKEN_BOT_ANDA_DI_SINI"
```

---

### 3. Instalasi Dependensi

**Sangat disarankan menggunakan virtual environment (venv).**

#### Buat Virtual Environment

```
python3 -m venv venv
```

#### Buat Virtual Environment win

```
python -m venv venv
```

#### Aktifkan Virtual Environment

- **macOS/Linux:**
  ```
  source venv/bin/activate
  ```
- **Windows (Command Prompt):**
  ```
  .\venv\Scripts\activate
  ```
- **Windows (PowerShell):**
  ```
  .\venv\Scripts\Activate.ps1
  ```
  *(Jika ada error, jalankan: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process`)*

#### Instal Pustaka yang Dibutuhkan

```
pip install -r requirements.txt
```

#### Instal Proyek dalam Mode Editable

```
pip install -e .
```

---

### 4. Jalankan Bot

Setelah semua setup selesai, jalankan bot:

```
python3 main.py
```

Bot Anda sekarang akan online di Discord.

---

## 🎧 Contoh Perintah

- `/play query:Never Gonna Give You Up` — Memainkan/menambah lagu ke antrean.
- `/queue` — Menampilkan daftar lagu berikutnya.
- `/skip` — Melewati lagu yang sedang diputar.
- `/nowplaying` — Menampilkan detail lagu saat ini.
- `/leave` — Menghentikan musik & mengeluarkan bot dari channel.
- `/settings` — Panel pengaturan musik (admin).
- `/help` — Daftar semua perintah.

---

## ⚖️ Lisensi

Proyek ini dilisensikan di bawah Lisensi MIT. Lihat file LICENSE untuk detail lebih lanjut.

