"""NEON CIRCLE - Media pembelajaran interaktif unsur-unsur lingkaran.

Jalankan dengan:  streamlit run neon_circle.py
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable

import streamlit as st
import streamlit.components.v1 as components

# =====================================================
# 1. KONFIGURASI
# =====================================================

st.set_page_config(
    page_title="NEON CIRCLE | Media Pembelajaran",
    page_icon="⭕",
    layout="wide",
    initial_sidebar_state="collapsed",
)

CX, CY, R = 300, 300, 205      # pusat & jari-jari kanvas SVG
DURASI_LED = 1.6               # total detik animasi nyala LED per unsur
Point = tuple[float, float]

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;800&family=Poppins:wght@300;400;500;600;700&display=swap');

.stApp {
    background:
        radial-gradient(ellipse at 75% 40%, #122b43 0%, transparent 50%),
        linear-gradient(135deg, #070c18, #0b1425 55%, #080d19);
    color: #eaf6ff;
    font-family: 'Poppins', sans-serif;
}
header[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 1450px; }
#MainMenu, footer { visibility: hidden; }

.neon-title {
    font-family: 'Orbitron', sans-serif; text-align: center;
    font-size: clamp(28px, 4vw, 43px); font-weight: 800; letter-spacing: 5px;
    color: #8af5ff;
    text-shadow: 0 0 5px #00eaff, 0 0 15px #00bfff, 0 0 35px #008cff;
}
.neon-subtitle {
    text-align: center; color: #94b6d0; font-size: 13px;
    letter-spacing: 2px; margin-top: -5px;
}
.section-title {
    font-family: 'Orbitron', sans-serif; font-size: 15px; color: #79eaff;
    letter-spacing: 2px; margin-bottom: 12px;
}

div.stButton > button {
    width: 100%; text-align: left; min-height: 43px; border-radius: 10px;
    border: 1px solid #24415c; background: rgba(15, 31, 51, 0.85);
    color: #d8edff; font-size: 13px; font-weight: 500;
    transition: all 0.25s ease;
}
div.stButton > button:hover {
    background: rgba(0, 190, 230, 0.12); border-color: #00eaff; color: #70f5ff;
    box-shadow: 0 0 12px rgba(0, 234, 255, 0.3); transform: translateX(3px);
}
div.stButton > button:focus-visible { outline: 2px solid #00eaff; outline-offset: 2px; }
div.stButton > button[kind="primary"] {
    background: linear-gradient(100deg, #103d59, #142b4b);
    border: 1px solid #00eaff; color: #8af5ff;
    box-shadow: 0 0 12px rgba(0, 234, 255, 0.25);
}

.panel {
    background: rgba(11, 25, 43, 0.83); border: 1px solid #23435e;
    border-radius: 16px; padding: 20px; margin-top: 14px;
    box-shadow: 0 0 22px rgba(0, 180, 255, 0.07);
}
.info-title { color: #70eaff; font-weight: 700; font-size: 17px; }
.info-text  { color: #b6cbe0; font-size: 13px; line-height: 1.8; }
.rumus {
    display: inline-block; margin-top: 6px; padding: 4px 12px;
    border: 1px dashed #2f5877; border-radius: 8px;
    color: #8af5ff; font-family: 'Orbitron', sans-serif; font-size: 12px;
}
.small-note { color: #668ba9; font-size: 11px; }
hr { border-color: #203a53; }
</style>
"""

# =====================================================
# 2. DATA UNSUR
# =====================================================


@dataclass(frozen=True)
class Unsur:
    kategori: str
    deskripsi: str
    warna: str
    rumus: str = ""


UNSUR: dict[str, Unsur] = {
    "Titik Pusat": Unsur(
        "TITIK",
        "Titik yang terletak tepat di tengah lingkaran. Titik pusat menjadi acuan "
        "untuk menentukan jarak ke seluruh titik pada keliling lingkaran.",
        "#ffe66d",
    ),
    "Jari-jari": Unsur(
        "GARIS",
        "Jari-jari adalah garis yang menghubungkan titik pusat lingkaran dengan satu "
        "titik pada keliling lingkaran. Panjang semua jari-jari dalam satu lingkaran sama.",
        "#00eaff",
        "r = ½ × d",
    ),
    "Diameter": Unsur(
        "GARIS",
        "Diameter adalah tali busur terpanjang: garis lurus yang menghubungkan dua titik "
        "pada keliling lingkaran dan melewati titik pusat. Panjangnya dua kali jari-jari.",
        "#ff54d9",
        "d = 2 × r",
    ),
    "Keliling": Unsur(
        "GARIS LENGKUNG",
        "Keliling adalah panjang seluruh garis lengkung yang membatasi bagian luar lingkaran.",
        "#00eaff",
        "K = 2πr = πd",
    ),
    "Busur": Unsur(
        "GARIS LENGKUNG",
        "Busur adalah bagian dari garis lengkung keliling lingkaran yang menghubungkan "
        "dua titik pada lingkaran.",
        "#ffe66d",
        "panjang busur = (θ/360°) × 2πr",
    ),
    "Tali Busur": Unsur(
        "GARIS",
        "Tali busur adalah garis lurus yang menghubungkan dua titik pada keliling lingkaran.",
        "#ff54d9",
    ),
    "Juring": Unsur(
        "DAERAH",
        "Juring adalah daerah dalam lingkaran yang dibatasi oleh dua jari-jari dan satu busur.",
        "#00eaff",
        "luas juring = (θ/360°) × πr²",
    ),
    "Tembereng": Unsur(
        "DAERAH",
        "Tembereng adalah daerah dalam lingkaran yang dibatasi oleh sebuah tali busur "
        "dan busur lingkaran.",
        "#ff54d9",
    ),
    "Apotema": Unsur(
        "GARIS",
        "Apotema adalah garis terpendek dari titik pusat lingkaran menuju tali busur, "
        "dengan posisi tegak lurus terhadap tali busur.",
        "#8cffb0",
        "a = √(r² − (½·tali busur)²)",
    ),
    "Garis Singgung": Unsur(
        "GARIS",
        "Garis singgung adalah garis yang menyentuh lingkaran tepat pada satu titik. "
        "Garis ini tegak lurus terhadap jari-jari yang ditarik menuju titik singgung.",
        "#ffe66d",
    ),
}

# =====================================================
# 3. PRIMITIF GEOMETRI & LED
# =====================================================


def polar(sudut: float, radius: float = R) -> Point:
    """Titik pada lingkaran untuk sudut tertentu (derajat, searah jarum jam di SVG)."""
    rad = math.radians(sudut)
    return CX + radius * math.cos(rad), CY + radius * math.sin(rad)


def led_titik(x: float, y: float, warna: str, delay: float = 0.0, ukuran: float = 3.5) -> str:
    return (
        f'<g class="led" style="--delay:{delay:.3f}s">'
        f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{ukuran * 3:.2f}" fill="{warna}" opacity="0.18"/>'
        f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{ukuran * 1.7:.2f}" fill="{warna}" opacity="0.42"/>'
        f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{ukuran:.2f}" fill="{warna}" '
        f'stroke="white" stroke-width="0.55"/></g>'
    )


def led_garis(p1: Point, p2: Point, warna: str, jumlah: int = 35) -> str:
    out = []
    for i in range(jumlah + 1):
        t = i / jumlah
        out.append(
            led_titik(
                p1[0] + (p2[0] - p1[0]) * t,
                p1[1] + (p2[1] - p1[1]) * t,
                warna,
                t * DURASI_LED,
            )
        )
    return "".join(out)


def led_busur(awal: float, akhir: float, warna: str, jumlah: int = 55, tutup: bool = False) -> str:
    """LED sepanjang busur. `tutup=True` untuk lingkaran penuh (tanpa titik ganda)."""
    n = jumlah if tutup else jumlah + 1
    out = []
    for i in range(n):
        t = i / jumlah
        x, y = polar(awal + (akhir - awal) * t)
        out.append(led_titik(x, y, warna, t * DURASI_LED, 3.1))
    return "".join(out)


def penanda(p: Point, label: str, warna: str) -> str:
    x, y = p
    return (
        f'<circle cx="{x:.2f}" cy="{y:.2f}" r="8" fill="{warna}" opacity="0.2"/>'
        f'<circle cx="{x:.2f}" cy="{y:.2f}" r="4" fill="white" stroke="{warna}" stroke-width="2"/>'
        f'<text x="{x + 11:.2f}" y="{y - 11:.2f}" class="label" fill="#ffffff" '
        f'font-size="15" font-weight="600">{label}</text>'
    )


def teks(x: float, y: float, isi: str, warna: str = "#fff", ukuran: int = 15,
         anchor: str = "start") -> str:
    return (
        f'<text x="{x:.2f}" y="{y:.2f}" fill="{warna}" font-size="{ukuran}" '
        f'font-weight="600" text-anchor="{anchor}" class="label">{isi}</text>'
    )


def siku_siku(sudut: Point, arah1: Point, arah2: Point, warna: str, s: float = 12) -> str:
    """Simbol siku-siku di `sudut`; arah1/arah2 adalah vektor satuan kedua sisi."""
    x, y = sudut
    a = (x + arah1[0] * s, y + arah1[1] * s)
    b = (x + (arah1[0] + arah2[0]) * s, y + (arah1[1] + arah2[1]) * s)
    c = (x + arah2[0] * s, y + arah2[1] * s)
    return (
        f'<path d="M {a[0]:.2f} {a[1]:.2f} L {b[0]:.2f} {b[1]:.2f} L {c[0]:.2f} {c[1]:.2f}" '
        f'fill="none" stroke="{warna}" stroke-width="2.5" class="softglow"/>'
    )


def bidang(path_d: str, warna: str, opacity: float) -> str:
    return f'<path d="{path_d}" fill="{warna}" fill-opacity="{opacity}" stroke="none"/>'


# =====================================================
# 4. RENDERER PER UNSUR
# =====================================================

O: Point = (CX, CY)


def r_titik_pusat(w: str) -> str:
    return led_titik(*O, w, 0, 6) + penanda(O, "O", w)


def r_jari_jari(w: str) -> str:
    a = polar(-40)
    mid = ((CX + a[0]) / 2, (CY + a[1]) / 2)
    return (
        led_garis(O, a, w, 45) + penanda(O, "O", w) + penanda(a, "A", w)
        + teks(mid[0] + 12, mid[1] + 18, "r", w, 19)
    )


def r_diameter(w: str) -> str:
    a, b = polar(180), polar(0)
    return (
        led_garis(a, b, w, 65)
        + penanda(a, "A", w) + penanda(b, "B", w) + penanda(O, "O", w)
        + teks(CX, CY + 30, "d", w, 19, "middle")
    )


def r_keliling(w: str) -> str:
    return led_busur(0, 360, w, 125, tutup=True)


def r_busur(w: str) -> str:
    a, b = polar(-140), polar(-40)
    return led_busur(-140, -40, w) + penanda(a, "A", w) + penanda(b, "B", w)


def r_tali_busur(w: str) -> str:
    a, b = polar(-140), polar(-40)
    return led_garis(a, b, w, 50) + penanda(a, "A", w) + penanda(b, "B", w)


def r_juring(w: str) -> str:
    a, b = polar(-120), polar(-30)
    area = bidang(f"M {CX} {CY} L {a[0]:.2f} {a[1]:.2f} "
                  f"A {R} {R} 0 0 1 {b[0]:.2f} {b[1]:.2f} Z", w, 0.16)
    lx, ly = polar(-75, R * 0.55)
    return (
        area + led_garis(O, a, w, 30) + led_garis(O, b, w, 30)
        + led_busur(-120, -30, w) + penanda(O, "O", w)
        + teks(lx, ly, "Juring", w, 14, "middle")
    )


def r_tembereng(w: str) -> str:
    a, b = polar(-140), polar(-40)
    area = bidang(f"M {a[0]:.2f} {a[1]:.2f} A {R} {R} 0 0 1 {b[0]:.2f} {b[1]:.2f} Z", w, 0.20)
    y_tengah = (a[1] + (CY - R)) / 2
    return (
        area + led_busur(-140, -40, w) + led_garis(a, b, w, 45)
        + penanda(a, "A", w) + penanda(b, "B", w)
        + teks(CX, y_tengah + 5, "Tembereng", w, 13, "middle")
    )


def r_apotema(w: str) -> str:
    a, b = polar(-140), polar(-40)
    m = (CX, a[1])  # titik tengah tali busur (proyeksi O ke tali busur)
    return (
        led_garis(a, b, "#4c6881", 45)
        + led_garis(O, m, w, 40)
        + penanda(O, "O", w) + penanda(m, "M", w)
        + siku_siku(m, (0, 1), (1, 0), w)
    )


def r_garis_singgung(w: str) -> str:
    t = (CX + R, CY)
    return (
        led_garis((t[0], CY - 160), (t[0], CY + 160), w, 55)
        + led_garis(O, t, "#00eaff", 35)
        + penanda(O, "O", "#00eaff") + penanda(t, "T", w)
        + siku_siku(t, (-1, 0), (0, -1), w)
        + teks(t[0] - 10, CY - 172, "Garis Singgung", w, 13, "end")
    )


RENDERER: dict[str, Callable[[str], str]] = {
    "Titik Pusat": r_titik_pusat,
    "Jari-jari": r_jari_jari,
    "Diameter": r_diameter,
    "Keliling": r_keliling,
    "Busur": r_busur,
    "Tali Busur": r_tali_busur,
    "Juring": r_juring,
    "Tembereng": r_tembereng,
    "Apotema": r_apotema,
    "Garis Singgung": r_garis_singgung,
}

# =====================================================
# 5. SVG UTAMA (di-cache per unsur)
# =====================================================


@st.cache_data(show_spinner=False)
def bangun_html(pilihan: str) -> str:
    warna = UNSUR[pilihan].warna
    visual = RENDERER[pilihan](warna)
    return f"""
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; background: transparent; overflow: hidden; }}
  .canvas {{
    width: 100%; max-width: 650px; margin: auto; padding: 12px;
    background: radial-gradient(circle at center, #142d49 0%, #0a172a 65%, #08111f 100%);
    border: 1px solid #284965; border-radius: 24px;
    box-shadow: 0 0 20px rgba(0,234,255,.10), inset 0 0 25px rgba(0,234,255,.04);
  }}
  svg {{ display: block; width: 100%; height: auto; }}
  .led {{
    opacity: 0; transform-box: fill-box; transform-origin: center;
    animation: nyala .45s ease forwards; animation-delay: var(--delay);
  }}
  @keyframes nyala {{
    0%   {{ opacity: 0; transform: scale(.2); }}
    65%  {{ opacity: 1; transform: scale(1.25); }}
    100% {{ opacity: 1; transform: scale(1); }}
  }}
  @media (prefers-reduced-motion: reduce) {{
    .led {{ animation: none; opacity: 1; }}
  }}
  .base-circle  {{ fill: none; stroke: #31506b; stroke-width: 2; opacity: .85; }}
  .outer-circle {{ fill: none; stroke: #00d9ff; stroke-width: 1; opacity: .17; }}
  .center-dot   {{ fill: #b4d8f5; }}
  .label     {{ font-family: Arial, sans-serif; filter: drop-shadow(0 0 5px {warna}); }}
  .softglow  {{ filter: drop-shadow(0 0 5px {warna}); }}
</style>
</head>
<body>
  <div class="canvas">
    <svg viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg"
         role="img" aria-label="Ilustrasi unsur lingkaran: {pilihan}">
      <title>{pilihan}</title>
      <defs>
        <pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse">
          <circle cx="1" cy="1" r="1" fill="#31516e" opacity=".30"/>
        </pattern>
      </defs>
      <rect width="600" height="600" fill="url(#grid)"/>
      <circle cx="{CX}" cy="{CY}" r="{R}" class="base-circle"/>
      <circle cx="{CX}" cy="{CY}" r="{R + 5}" class="outer-circle"/>
      <circle cx="{CX}" cy="{CY}" r="3" class="center-dot"/>
      {visual}
    </svg>
  </div>
</body>
</html>
"""


# =====================================================
# 6. STATE & CALLBACK
# =====================================================


def pilih_unsur(nama: str) -> None:
    st.session_state.unsur_aktif = nama


st.session_state.setdefault("unsur_aktif", "Jari-jari")

# =====================================================
# 7. UI
# =====================================================

st.markdown(CSS, unsafe_allow_html=True)
st.markdown(
    '<div class="neon-title">NEON CIRCLE</div>'
    '<div class="neon-subtitle">INTERACTIVE LEARNING • CIRCLE GEOMETRY</div><br>',
    unsafe_allow_html=True,
)

kiri, kanan = st.columns([0.85, 2.15], gap="large")

with kiri:
    st.markdown('<div class="section-title">✦ PILIH UNSUR</div>', unsafe_allow_html=True)
    st.markdown(
        '<p class="small-note">Klik salah satu unsur untuk menampilkan lampu LED pada lingkaran.</p>',
        unsafe_allow_html=True,
    )
    for nama in UNSUR:
        aktif = nama == st.session_state.unsur_aktif
        st.button(
            ("✦  " if aktif else "○  ") + nama,
            key=f"pilih_{nama}",
            type="primary" if aktif else "secondary",
            use_container_width=True,
            on_click=pilih_unsur,
            args=(nama,),
        )

with kanan:
    nama_aktif = st.session_state.unsur_aktif
    data = UNSUR[nama_aktif]

    st.markdown(
        f"""
        <div style="text-align:center; margin-bottom:5px;">
          <div style="color:{data.warna}; font-family:Orbitron,sans-serif; font-size:22px;
                      font-weight:700; letter-spacing:2px; text-shadow:0 0 12px {data.warna};">
            {nama_aktif.upper()}</div>
          <div style="color:#7598b9; font-size:11px; letter-spacing:2px;">{data.kategori}</div>
        </div>""",
        unsafe_allow_html=True,
    )

    components.html(bangun_html(nama_aktif), height=650, scrolling=False)

    rumus_html = f'<div class="rumus">{data.rumus}</div>' if data.rumus else ""
    st.markdown(
        f"""
        <div class="panel">
          <div class="info-title">✧ Mengenal {nama_aktif}</div>
          <div class="info-text">{data.deskripsi}</div>
          {rumus_html}
          <hr>
          <div style="display:flex; align-items:center; gap:8px;">
            <div style="width:10px; height:10px; border-radius:50%; background:{data.warna};
                        box-shadow:0 0 10px {data.warna};"></div>
            <span class="small-note">Visualisasi LED aktif: {nama_aktif}</span>
          </div>
        </div>""",
        unsafe_allow_html=True,
    )

    with st.expander("🧮 Coba hitung: masukkan jari-jari"):
        r_in = st.number_input("Jari-jari (r)", min_value=0.1, value=7.0, step=0.5)
        c1, c2, c3 = st.columns(3)
        c1.metric("Diameter", f"{2 * r_in:.2f}")
        c2.metric("Keliling", f"{2 * math.pi * r_in:.2f}")
        c3.metric("Luas", f"{math.pi * r_in ** 2:.2f}")

st.markdown(
    """
    <br><hr>
    <div style="text-align:center; color:#577894; font-size:11px; letter-spacing:2px;">
      NEON CIRCLE • MEDIA PEMBELAJARAN MATEMATIKA<br>EXPLORE • OBSERVE • UNDERSTAND
    </div>""",
    unsafe_allow_html=True,
)
