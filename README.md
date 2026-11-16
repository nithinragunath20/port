# 📁 Nithin R — Portfolio Website Recreation

Pixel-perfect recreation of the award-winning Adobe Portfolio ("marta" theme) website based on [norakaszanyi.com](https://norakaszanyi.com/home) and `download.htm`.

Powered by a lightweight **Python Flask** backend with pure HTML5, CSS3, and Vanilla JavaScript on the frontend.

---

## 🚀 Features & Exact Visual Recreation

- **Exact Adobe Fonts Typography**:
  - `Adrianna Extended` (`cxxc`): Hero heading `NITHIN R`, uppercase subtitles `C S E  |  A I  &  M L`, project titles.
  - `Acumin Pro Wide` (`vcxq`): Fixed navigation items (`Works`, `Contact`, `Bio`), footer branding, and metadata.
  - All 13 original font weights and OTF files downloaded and served locally without external CDN lockouts.
- **Header & Navigation**:
  - Exact `125px` height fixed header with authentic circular monogram logo.
  - Strikethrough hover animation on navigation links (`Works`, `Contact`, `Bio`).
  - Smooth backdrop and color transitions on scroll past the masthead.
  - Fully responsive mobile drawer with 3-bar hamburger toggle.
- **Hero Video Masthead**:
  - Full-screen high-contrast looping MP4 video background.
  - Centered hero headline and spaced subtitle.
  - Animated chevron scroll-down arrow with smooth scroll trigger to `#works`.
- **Project Grid Gallery**:
  - Exact 202:158 card aspect ratio (`padding-bottom: 78.21782%`).
  - Dark hover overlay (`#0D0D0D` at 0.66 opacity) with centered uppercase title reveals.
  - Includes all 22 project items, cover images, and animated GIFs from the reference.
- **Dedicated Inner Pages**:
  - `/` or `/home`: Main portfolio gallery.
  - `/contact`: Contact details with AJAX message form.
  - `/bio` or `/cv`: Profile, education (BTech CSE-AIML at Jain University), experience (Lumbini Technologies), skills, and resume downloads.
  - `/project/<id>`: Individual project showcase view.
  - `/resume/download`: Direct download of Nithin's Resume PDF.
  - `/offer-letter/download`: Direct download of the Offer Letter PDF.

---

## 📂 Project Structure

```
portfolio/
├── app.py                      ← Flask application factory & runner
├── config.py                   ← Application configuration
├── extensions.py               ← Database & CSRF extensions
├── models.py                   ← Contact message and admin models
├── projects_data.json          ← Metadata for all 22 gallery projects
├── requirements.txt            ← Python dependencies
├── routes/
│   ├── main.py                 ← Routes for /, /contact, /bio, /project/<id>, and downloads
│   ├── contact.py              ← Contact form AJAX handler
│   └── admin.py                ← Lightweight message viewer
├── templates/
│   ├── index.html              ← Reconstructed homepage with video masthead & 22 cards
│   ├── contact.html            ← Contact page
│   ├── bio.html                ← Bio / CV page with Nithin R's profile & PDF links
│   └── project_detail.html     ← Individual project view
├── static/
│   ├── css/
│   │   └── portfolio.css       ← Exact recreation of Adobe Portfolio "marta" theme styles
│   ├── js/
│   │   └── portfolio.js        ← Navigation, scroll transitions, video autoplay, AJAX
│   ├── fonts/
│   │   ├── fonts.css           ← Local @font-face declarations
│   │   └── *.otf               ← 13 Adobe Fonts (Adrianna Extended & Acumin Pro Wide)
│   ├── images/
│   │   ├── hero_video.mp4      ← 1080p looping background video
│   │   ├── logo.png            ← Original circular logo mark
│   │   └── projects/           ← 22 project images & animated GIFs
│   └── resume/
│       ├── Nithin_Ragunath_Resume.pdf
│       └── Nithin_Ragunath_Offer_Letter.pdf
└── instance/
    └── portfolio.db            ← SQLite storage
```

---

## 💻 Running the Server

The server is currently running in the background at **`http://127.0.0.1:5000`**.

To run it manually:
```powershell
python app.py
```
Or with custom host and port:
```powershell
python -m flask --app app run --host 127.0.0.1 --port 5000
```
