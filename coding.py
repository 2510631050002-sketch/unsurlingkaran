
import streamlit as st
import streamlit.components.v1 as components
import math

# =====================================================
# 1. KONFIGURASI APLIKASI
# =====================================================

st.set_page_config(
    page_title="NEON CIRCLE | Media Pembelajaran",
    page_icon="⭕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================
# 2. CSS UTAMA
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;600;700;800&family=Poppins:wght@300;400;500;600;700&display=swap');

.stApp {
    background:
        radial-gradient(ellipse at 75% 40%, #122b43 0%, transparent 50%),
        linear-gradient(135deg, #070c18, #0b1425 55%, #080d19);
    color: #eaf6ff;
    font-family: 'Poppins', sans-serif;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1450px;
}

.neon-title {
    font-family: 'Orbitron', sans-serif;
    text-align: center;
    font-size: clamp(28px, 4vw, 43px);
    font-weight: 800;
    letter-spacing: 5px;
    color: #8af5ff;
    text-shadow:
        0 0 5px #00eaff,
        0 0 15px #00bfff,
        0 0 35px #008cff;
}

.neon-subtitle {
    text-align: center;
    color: #94b6d0;
    font-size: 13px;
    letter-spacing: 2px;
    margin-top: -5px;
}

.section-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 15px;
    color: #79eaff;
    letter-spacing: 2px;
    margin-bottom: 12px;
}

div.stButton > button {
    width: 100%;
    text-align: left;
    min-height: 43px;
    border-radius: 10px;
    border: 1px solid #24415c;
    background: rgba(15, 31, 51, 0.85);
    color: #d8edff;
    font-family: 'Poppins', sans-serif;
    font-size: 13px;
    font-weight: 500;
    transition: all 0.25s ease;
}

div.stButton > button:hover {
    background: rgba(0, 190, 230, 0.12);
    border-color: #00eaff;
    color: #70f5ff;
    box-shadow: 0 0 12px rgba(0, 234, 255, 0.3);
    transform: translateX(3px);
}

div.stButton > button:focus:not(:active) {
    border-color: #00eaff;
    color: #70f5ff;
}

div.stButton > button[kind="primary"] {
    background: linear-gradient(100deg, #103d59, #142b4b);
    border: 1px solid #00eaff;
    color: #8af5ff;
    box-shadow: 0 0 12px rgba(0, 234, 255, 0.25);
}

.panel {
    background: rgba(11, 25, 43, 0.83);
    border: 1px solid #23435e;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 0 22px rgba(0, 180, 255, 0.07);
}

.info-title {
    color: #70eaff;
    font-weight: 700;
    font-size: 17px;
}

.info-text {
    color: #b6cbe0;
    font-size: 13px;
    line-height: 1.8;
}

.small-note {
    color: #668ba9;
    font-size: 11px;
}

hr {
    border-color: #203a53;
}

#MainMenu, footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# 3. DATA UNSUR LINGKARAN
# =====================================================

UNSUR = {
    "Titik Pusat": {
        "kategori": "TITIK",
        "deskripsi": "Titik yang terletak tepat di tengah lingkaran. Titik pusat menjadi acuan untuk menentukan jarak ke seluruh titik pada keliling lingkaran.",
        "warna": "#ffe66d"
    },
    "Jari-jari": {
        "kategori": "GARIS",
        "deskripsi": "Jari-jari adalah garis yang menghubungkan titik pusat lingkaran dengan satu titik pada keliling lingkaran. Panjang semua jari-jari dalam satu lingkaran sama.",
        "warna": "#00eaff"
    },
    "Diameter": {
        "kategori": "GARIS",
        "deskripsi": "Diameter adalah garis lurus yang menghubungkan dua titik pada keliling lingkaran dan melewati titik pusat. Panjang diameter adalah dua kali jari-jari.",
        "warna": "#ff54d9"
    },
    "Keliling": {
        "kategori": "GARIS LENGKUNG",
        "deskripsi": "Keliling adalah panjang seluruh garis lengkung yang membatasi bagian luar lingkaran.",
        "warna": "#00eaff"
    },
    "Busur": {
        "kategori": "GARIS LENGKUNG",
        "deskripsi": "Busur adalah bagian dari garis lengkung keliling lingkaran yang menghubungkan dua titik pada lingkaran.",
        "warna": "#ffe66d"
    },
    "Tali Busur": {
        "kategori": "GARIS",
        "deskripsi": "Tali busur adalah garis lurus yang menghubungkan dua titik pada keliling lingkaran.",
        "warna": "#ff54d9"
    },
    "Juring": {
        "kategori": "DAERAH",
        "deskripsi": "Juring adalah daerah dalam lingkaran yang dibatasi oleh dua jari-jari dan satu busur.",
        "warna": "#00eaff"
    },
    "Tembereng": {
        "kategori": "DAERAH",
        "deskripsi": "Tembereng adalah daerah dalam lingkaran yang dibatasi oleh sebuah tali busur dan busur lingkaran.",
        "warna": "#ff54d9"
    },
    "Apotema": {
        "kategori": "GARIS",
        "deskripsi": "Apotema adalah garis terpendek dari titik pusat lingkaran menuju tali busur, dengan posisi tegak lurus terhadap tali busur.",
        "warna": "#8cffb0"
    },
    "Garis Singgung": {
        "kategori": "GARIS",
        "deskripsi": "Garis singgung adalah garis yang menyentuh lingkaran tepat pada satu titik. Garis ini tegak lurus terhadap jari-jari yang ditarik menuju titik singgung.",
        "warna": "#ffe66d"
    }
}


# =====================================================
# 4. FUNGSI GEOMETRI DAN LED
# =====================================================

CX, CY, R = 300, 300, 205

def titik_polar(sudut, radius=R):
    rad = math.radians(sudut)
    return (
        CX + radius * math.cos(rad),
        CY + radius * math.sin(rad)
    )


def format_num(n):
    return f"{n:.2f}"


def led_titik(x, y, warna, indeks=0, ukuran=3.5):
    delay = indeks * 0.035

    return f"""
    <g class="led" style="--delay:{delay:.3f}s">
        <circle cx="{x:.2f}" cy="{y:.2f}"
            r="{ukuran*3:.2f}"
            fill="{warna}" opacity="0.18"/>
        <circle cx="{x:.2f}" cy="{y:.2f}"
            r="{ukuran*1.7:.2f}"
            fill="{warna}" opacity="0.42"/>
        <circle cx="{x:.2f}" cy="{y:.2f}"
            r="{ukuran:.2f}"
            fill="{warna}" stroke="white"
            stroke-width="0.55"/>
    </g>
    """


def led_garis(x1, y1, x2, y2, warna, jumlah=35):
    hasil = ""
    for i in range(jumlah + 1):
        t = i / jumlah
        x = x1 + (x2 - x1) * t
        y = y1 + (y2 - y1) * t
        hasil += led_titik(x, y, warna, i)
    return hasil


def led_busur(sudut_awal, sudut_akhir, warna, jumlah=55):
    hasil = ""
    for i in range(jumlah + 1):
        t = i / jumlah
        sudut = sudut_awal + (sudut_akhir - sudut_awal) * t
        x, y = titik_polar(sudut)
        hasil += led_titik(x, y, warna, i, 3.1)
    return hasil


def titik_pada_lingkaran(x, y, label, warna):
    return f"""
    <circle cx="{x:.2f}" cy="{y:.2f}" r="8"
        fill="{warna}" opacity="0.2"/>
    <circle cx="{x:.2f}" cy="{y:.2f}" r="4"
        fill="white" stroke="{warna}" stroke-width="2"/>
    <text x="{x+11:.2f}" y="{y-11:.2f}"
        class="label">{label}</text>
    """


def teks(x, y, tulisan, warna="#ffffff", ukuran=15):
    return f"""
    <text x="{x}" y="{y}" fill="{warna}"
        font-size="{ukuran}" font-weight="600"
        class="label">{tulisan}</text>
    """


# =====================================================
# 5. MEMBUAT VISUALISASI SETIAP UNSUR
# =====================================================

def buat_visualisasi(pilihan):

    warna = UNSUR[pilihan]["warna"]
    gambar = ""

    # Titik acuan
    O = (CX, CY)

    # TITIK PUSAT
    if pilihan == "Titik Pusat":
        gambar += led_titik(CX, CY, warna, 1, 6)
        gambar += titik_pada_lingkaran(CX, CY, "O", warna)

    # JARI-JARI
    elif pilihan == "Jari-jari":
        A = titik_polar(-40)
        gambar += led_garis(CX, CY, *A, warna, 45)
        gambar += titik_pada_lingkaran(CX, CY, "O", warna)
        gambar += titik_pada_lingkaran(*A, "A", warna)
        gambar += teks(385, 210, "r", warna, 19)

    # DIAMETER
    elif pilihan == "Diameter":
        A = titik_polar(180)
        B = titik_polar(0)
        gambar += led_garis(*A, *B, warna, 65)
        gambar += titik_pada_lingkaran(*A, "A", warna)
        gambar += titik_pada_lingkaran(*B, "B", warna)
        gambar += titik_pada_lingkaran(CX, CY, "O", warna)
        gambar += teks(CX-8, CY-15, "d", warna, 19)

    # KELILING
    elif pilihan == "Keliling":
        gambar += led_busur(0, 360, warna, 125)

    # BUSUR
    elif pilihan == "Busur":
        gambar += led_busur(-140, -40, warna, 55)
        A = titik_polar(-140)
        B = titik_polar(-40)
        gambar += titik_pada_lingkaran(*A, "A", warna)
        gambar += titik_pada_lingkaran(*B, "B", warna)

    # TALI BUSUR
    elif pilihan == "Tali Busur":
        A = titik_polar(-140)
        B = titik_polar(-40)
        gambar += led_garis(*A, *B, warna, 50)
        gambar += titik_pada_lingkaran(*A, "A", warna)
        gambar += titik_pada_lingkaran(*B, "B", warna)

    # JURING
    elif pilihan == "Juring":
        A = titik_polar(-120)
        B = titik_polar(-30)

        # Bidang juring
        gambar += f"""
        <path d="M {CX} {CY} L {A[0]} {A[1]}
        A {R} {R} 0 0 1 {B[0]} {B[1]} Z"
        fill="{warna}" fill-opacity="0.16"
        stroke="none"/>
        """
        gambar += led_garis(CX, CY, *A, warna, 30)
        gambar += led_garis(CX, CY, *B, warna, 30)
        gambar += led_busur(-120, -30, warna, 55)
        gambar += titik_pada_lingkaran(CX, CY, "O", warna)

    # TEMBENG / TEMBERENG
    elif pilihan == "Tembereng":
        A = titik_polar(-140)
        B = titik_polar(-40)

        gambar += f"""
        <path d="M {A[0]} {A[1]}
        A {R} {R} 0 0 1 {B[0]} {B[1]} Z"
        fill="{warna}" fill-opacity="0.20"
        stroke="none"/>
        """
        gambar += led_busur(-140, -40, warna, 55)
        gambar += led_garis(*A, *B, warna, 45)
        gambar += titik_pada_lingkaran(*A, "A", warna)
        gambar += titik_pada_lingkaran(*B, "B", warna)

    # APOTEMA
    elif pilihan == "Apotema":
        A = titik_polar(-140)
        B = titik_polar(-40)
        M = (CX, CY - R * math.cos(math.radians(50)))

        # Tali busur horizontal
        gambar += led_garis(*A, *B, "#4c6881", 45)

        # Apotema
        gambar += led_garis(CX, CY, M[0], M[1], warna, 40)
        gambar += titik_pada_lingkaran(CX, CY, "O", warna)
        gambar += titik_pada_lingkaran(M[0], M[1], "M", warna)

        # Simbol siku-siku
        gambar += f"""
        <path d="M 300 249 L 310 249 L 310 259"
        fill="none" stroke="{warna}"
        stroke-width="2.5" class="softglow"/>
        """

    # GARIS SINGGUNG
    elif pilihan == "Garis Singgung":
        A = (CX + R, CY)

        # Garis singgung vertikal
        gambar += led_garis(
            CX + R, CY - 160,
            CX + R, CY + 160,
            warna, 55
        )

        # Jari-jari ke titik singgung
        gambar += led_garis(CX, CY, *A, "#00eaff", 35)

        gambar += titik_pada_lingkaran(CX, CY, "O", "#00eaff")
        gambar += titik_pada_lingkaran(*A, "T", warna)

        gambar += teks(510, 135, "Garis", warna, 13)
        gambar += teks(510, 153, "Singgung", warna, 13)

    return gambar


# =====================================================
# 6. SVG UTAMA
# =====================================================

def tampilkan_lingkaran(pilihan):

    visual = buat_visualisasi(pilihan)
    warna = UNSUR[pilihan]["warna"]

    svg = f"""
    <html>
    <head>
    <style>
        * {{ box-sizing: border-box; }}

        body {{
            margin: 0;
            background: transparent;
            overflow: hidden;
        }}

        .canvas {{
            width: 100%;
            max-width: 650px;
            margin: auto;
            background:
                radial-gradient(circle at center,
                    #142d49 0%, #0a172a 65%, #08111f 100%);
            border: 1px solid #284965;
            border-radius: 24px;
            padding: 12px;
            box-shadow:
                0 0 20px rgba(0,234,255,0.10),
                inset 0 0 25px rgba(0,234,255,0.04);
        }}

        svg {{
            display: block;
            width: 100%;
            height: auto;
        }}

        .led {{
            opacity: 0;
            animation: lampuNyala 0.45s ease forwards;
            animation-delay: var(--delay);
        }}

        @keyframes lampuNyala {{
            0% {{
                opacity: 0;
                transform: scale(0.2);
                transform-origin: center;
            }}
            65% {{
                opacity: 1;
                transform: scale(1.25);
            }}
            100% {{
                opacity: 1;
                transform: scale(1);
            }}
        }}

        .base-circle {{
            fill: none;
            stroke: #31506b;
            stroke-width: 2;
            opacity: 0.85;
        }}

        .outer-circle {{
            fill: none;
            stroke: #00d9ff;
            stroke-width: 1;
            opacity: 0.17;
        }}

        .label {{
            font-family: Arial, sans-serif;
            filter: drop-shadow(0 0 5px {warna});
        }}

        .softglow {{
            filter: drop-shadow(0 0 5px {warna});
        }}

        .center-dot {{
            fill: #b4d8f5;
        }}
    </style>
    </head>

    <body>
    <div class="canvas">
        <svg viewBox="0 0 600 600"
             xmlns="http://www.w3.org/2000/svg">

            <defs>
                <pattern id="grid"
                    width="30" height="30"
                    patternUnits="userSpaceOnUse">
                    <circle cx="1" cy="1" r="1"
                        fill="#31516e" opacity="0.30"/>
                </pattern>
            </defs>

            <rect width="600" height="600"
                fill="url(#grid)"/>

            <!-- Lingkaran dasar -->
            <circle cx="{CX}" cy="{CY}" r="{R}"
                class="base-circle"/>

            <circle cx="{CX}" cy="{CY}" r="{R+5}"
                class="outer-circle"/>

            <!-- Pusat -->
            <circle cx="{CX}" cy="{CY}" r="3"
                class="center-dot"/>

            <!-- Visualisasi unsur -->
            {visual}

        </svg>
    </div>
    </body>
    </html>
    """

    components.html(svg, height=650, scrolling=False)


# =====================================================
# 7. HEADER
# =====================================================

st.markdown("""
<div class="neon-title">NEON CIRCLE</div>
<div class="neon-subtitle">
    INTERACTIVE LEARNING • CIRCLE GEOMETRY
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# =====================================================
# 8. SESSION STATE
# =====================================================

if "unsur_aktif" not in st.session_state:
    st.session_state.unsur_aktif = "Jari-jari"


# =====================================================
# 9. TAMPILAN UTAMA
# =====================================================

kolom_kiri, kolom_kanan = st.columns(
    [0.85, 2.15],
    gap="large"
)


# =====================================================
# 10. PANEL KIRI - DAFTAR UNSUR
# =====================================================

with kolom_kiri:

    st.markdown(
        '<div class="section-title">✦ PILIH UNSUR</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="small-note">Klik salah satu unsur '
        'untuk menampilkan lampu LED pada lingkaran.</p>',
        unsafe_allow_html=True
    )

    for nama, data in UNSUR.items():

        aktif = nama == st.session_state.unsur_aktif

        if st.button(
            ("✦  " if aktif else "○  ") + nama,
            key=f"pilih_{nama}",
            type="primary" if aktif else "secondary",
            use_container_width=True
        ):
            st.session_state.unsur_aktif = nama
            st.rerun()


# =====================================================
# 11. PANEL KANAN - VISUALISASI
# =====================================================

with kolom_kanan:

    aktif = st.session_state.unsur_aktif
    data = UNSUR[aktif]

    st.markdown(
        f"""
        <div style="text-align:center; margin-bottom:5px;">
            <div style="
                color:{data['warna']};
                font-family:Orbitron, sans-serif;
                font-size:22px;
                font-weight:700;
                letter-spacing:2px;
                text-shadow:0 0 12px {data['warna']};
            ">{aktif.upper()}</div>

            <div style="
                color:#7598b9;
                font-size:11px;
                letter-spacing:2px;
            ">{data['kategori']}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    tampilkan_lingkaran(aktif)

    st.markdown(
        f"""
        <div class="panel">
            <div class="info-title">
                ✧ Mengenal {aktif}
            </div>
            <div class="info-text">
                {data['deskripsi']}
            </div>
            <hr>
            <div style="display:flex; align-items:center; gap:8px;">
                <div style="
                    width:10px;height:10px;
                    border-radius:50%;
                    background:{data['warna']};
                    box-shadow:0 0 10px {data['warna']};
                "></div>
                <span class="small-note">
                    Visualisasi LED aktif: {aktif}
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# 12. FOOTER
# =====================================================

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<hr>
<div style="
    text-align:center;
    color:#577894;
    font-size:11px;
    letter-spacing:2px;
">
    NEON CIRCLE • MEDIA PEMBELAJARAN MATEMATIKA
    <br>
    EXPLORE • OBSERVE • UNDERSTAND
</div>
""", unsafe_allow_html=True)
