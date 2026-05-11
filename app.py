import streamlit as st
import qrcode
from qrcode.image.styledpil import StyledPilImage
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="QR Generator", page_icon="🔗", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: transparent !important;
}
[data-testid="stApp"] {
    background: #020510 !important;
}

[data-testid="stAppViewContainer"]::before {
    content: '';s
    position: fixed;
    inset: 0;
    z-index: 0;
    background: linear-gradient(180deg, #020510 0%, #040d24 40%, #020510 100%);
}

[data-testid="stAppViewContainer"]::after {
    content: '';
    position: fixed;
    bottom: -10%;
    left: 50%;
    transform: translateX(-50%) perspective(600px) rotateX(70deg);
    width: 200vw;
    height: 140vh;
    background-image:
        linear-gradient(rgba(0,200,255,0.12) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,200,255,0.12) 1px, transparent 1px);
    background-size: 60px 60px;
    animation: gridMove 6s linear infinite;
    z-index: 0;
    pointer-events: none;
}

@keyframes gridMove {
    from { background-position: 0 0; }
    to   { background-position: 0 60px; }
}

.orb {
    position: fixed;
    border-radius: 50%;
    filter: blur(80px);
    opacity: 0.35;
    animation: drift 12s ease-in-out infinite alternate;
    z-index: 0;
    pointer-events: none;
}
.orb1 { width: 420px; height: 420px; top: -100px; left: -120px;
         background: radial-gradient(circle, #0066ff, #001a66); animation-duration: 14s; }
.orb2 { width: 320px; height: 320px; bottom: -80px; right: -80px;
         background: radial-gradient(circle, #00ccff, #003366); animation-duration: 10s; animation-delay: -4s; }
.orb3 { width: 200px; height: 200px; top: 40%; right: 10%;
         background: radial-gradient(circle, #7b2fff, #1a004d); animation-duration: 16s; animation-delay: -7s; }

@keyframes drift {
    from { transform: translate(0, 0) scale(1); }
    to   { transform: translate(30px, 40px) scale(1.08); }
}

.stars {
    position: fixed; inset: 0; z-index: 0; pointer-events: none;
    background-image:
        radial-gradient(1px 1px at 15% 22%, rgba(255,255,255,0.9) 0%, transparent 100%),
        radial-gradient(1px 1px at 72% 8%,  rgba(255,255,255,0.7) 0%, transparent 100%),
        radial-gradient(1px 1px at 88% 55%, rgba(255,255,255,0.8) 0%, transparent 100%),
        radial-gradient(1px 1px at 33% 80%, rgba(255,255,255,0.6) 0%, transparent 100%),
        radial-gradient(1px 1px at 56% 38%, rgba(255,255,255,0.9) 0%, transparent 100%),
        radial-gradient(1px 1px at 5%  60%, rgba(255,255,255,0.5) 0%, transparent 100%),
        radial-gradient(1px 1px at 92% 75%, rgba(255,255,255,0.7) 0%, transparent 100%),
        radial-gradient(2px 2px at 44% 12%, rgba(0,200,255,0.9)  0%, transparent 100%),
        radial-gradient(2px 2px at 78% 88%, rgba(0,200,255,0.7)  0%, transparent 100%);
}

[data-testid="stMainBlockContainer"] {
    position: relative;
    z-index: 10;
    max-width: 600px !important;
    margin: 60px auto !important;
    padding: 44px 48px 52px !important;
    background: linear-gradient(135deg,
        rgba(4,20,60,0.82) 0%,
        rgba(2,10,30,0.90) 100%) !important;
    border: 1px solid rgba(0,200,255,0.22) !important;
    border-radius: 24px !important;
    box-shadow:
        0 0 0 1px rgba(0,200,255,0.08),
        0 8px 32px rgba(0,0,0,0.6),
        0 0 80px rgba(0,100,255,0.12),
        inset 0 1px 0 rgba(255,255,255,0.06) !important;
    backdrop-filter: blur(24px) !important;
}

h1 {
    font-family: 'Orbitron', monospace !important;
    font-weight: 900 !important;
    font-size: 2rem !important;
    letter-spacing: 0.04em !important;
    background: linear-gradient(135deg, #00ccff 0%, #ffffff 50%, #7b2fff 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    margin-bottom: 4px !important;
    text-shadow: none !important;
}

h3 {
    font-family: 'Orbitron', monospace !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.10em !important;
    color: rgba(0,200,255,0.70) !important;
    text-transform: uppercase !important;
    margin-top: 28px !important;
    margin-bottom: 12px !important;
    padding-bottom: 8px !important;
    border-bottom: 1px solid rgba(0,200,255,0.15) !important;
}

p, label, .stMarkdown p {
    font-family: 'Rajdhani', sans-serif !important;
    color: rgba(180,220,255,0.80) !important;
    font-size: 1.05rem !important;
    letter-spacing: 0.02em !important;
}

/* Slider label */
[data-testid="stSlider"] label {
    font-family: 'Rajdhani', sans-serif !important;
    color: rgba(180,220,255,0.80) !important;
}

/* Color picker label */
[data-testid="stColorPicker"] label {
    font-family: 'Rajdhani', sans-serif !important;
    color: rgba(180,220,255,0.80) !important;
}

/* Select box */
[data-testid="stSelectbox"] label {
    font-family: 'Rajdhani', sans-serif !important;
    color: rgba(180,220,255,0.80) !important;
}
[data-testid="stSelectbox"] > div > div {
    background: rgba(0,10,40,0.70) !important;
    border: 1px solid rgba(0,200,255,0.30) !important;
    border-radius: 12px !important;
    color: #e0f4ff !important;
}

/* File uploader */
[data-testid="stFileUploader"] label {
    font-family: 'Rajdhani', sans-serif !important;
    color: rgba(180,220,255,0.80) !important;
}
[data-testid="stFileUploadDropzone"] {
    background: rgba(0,10,40,0.60) !important;
    border: 1px dashed rgba(0,200,255,0.35) !important;
    border-radius: 12px !important;
}

.stTextInput > div > div > input {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1rem !important;
    background: rgba(0,10,40,0.70) !important;
    border: 1px solid rgba(0,200,255,0.30) !important;
    border-radius: 12px !important;
    color: #e0f4ff !important;
    padding: 14px 18px !important;
    box-shadow: 0 0 20px rgba(0,150,255,0.08), inset 0 1px 0 rgba(255,255,255,0.04) !important;
    transition: border-color 0.25s, box-shadow 0.25s !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(0,200,255,0.75) !important;
    box-shadow: 0 0 30px rgba(0,200,255,0.20), inset 0 1px 0 rgba(255,255,255,0.06) !important;
    outline: none !important;
}
.stTextInput > div > div > input::placeholder { color: rgba(100,160,220,0.45) !important; }

.stButton > button {
    font-family: 'Orbitron', monospace !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    width: 100% !important;
    padding: 16px !important;
    border-radius: 12px !important;
    border: 1px solid rgba(0,200,255,0.55) !important;
    background: linear-gradient(135deg, rgba(0,80,200,0.60) 0%, rgba(0,30,100,0.80) 100%) !important;
    color: #00e5ff !important;
    cursor: pointer !important;
    position: relative !important;
    overflow: hidden !important;
    transition: all 0.3s !important;
    box-shadow: 0 0 30px rgba(0,150,255,0.15), inset 0 1px 0 rgba(255,255,255,0.08) !important;
}
.stButton > button:hover {
    border-color: rgba(0,230,255,0.90) !important;
    color: #ffffff !important;
    box-shadow: 0 0 50px rgba(0,200,255,0.35), 0 4px 20px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.12) !important;
    transform: translateY(-2px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

.stDownloadButton > button {
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.06em !important;
    width: 100% !important;
    padding: 13px !important;
    border-radius: 12px !important;
    border: 1px solid rgba(123,47,255,0.55) !important;
    background: linear-gradient(135deg, rgba(60,0,160,0.50) 0%, rgba(20,0,80,0.75) 100%) !important;
    color: #c084fc !important;
    transition: all 0.3s !important;
    box-shadow: 0 0 25px rgba(120,50,255,0.12) !important;
    margin-top: 8px !important;
}
.stDownloadButton > button:hover {
    border-color: rgba(160,80,255,0.85) !important;
    color: #ffffff !important;
    box-shadow: 0 0 40px rgba(150,50,255,0.30) !important;
    transform: translateY(-2px) !important;
}

[data-testid="stImage"] img {
    border-radius: 16px !important;
    border: 1px solid rgba(0,200,255,0.20) !important;
    box-shadow: 0 0 40px rgba(0,150,255,0.20), 0 8px 32px rgba(0,0,0,0.5) !important;
    display: block !important;
    margin: 16px auto 0 !important;
}

[data-testid="stAlert"] {
    font-family: 'Rajdhani', sans-serif !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,80,80,0.30) !important;
    background: rgba(80,0,0,0.40) !important;
}

#MainMenu, footer, header { visibility: hidden !important; }
[data-testid="stToolbar"] { display: none !important; }
</style>

<div class="orb orb1"></div>
<div class="orb orb2"></div>
<div class="orb orb3"></div>
<div class="stars"></div>
""", unsafe_allow_html=True)

# ── Helper ──────────────────────────────────────────────────────────────────
def hex_to_rgb(hex_color: str) -> tuple:
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def generate_qr(link, fg_color, bg_color, box_size, ec_level, logo_file, output_format):
    ec_map = {"L": qrcode.constants.ERROR_CORRECT_L,
              "M": qrcode.constants.ERROR_CORRECT_M,
              "Q": qrcode.constants.ERROR_CORRECT_Q,
              "H": qrcode.constants.ERROR_CORRECT_H}

    qr = qrcode.QRCode(
        version=1,
        error_correction=ec_map[ec_level],
        box_size=box_size,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fg_color, back_color=bg_color).convert("RGBA")

    # ── Embed logo ──
    if logo_file is not None:
        logo = Image.open(logo_file).convert("RGBA")
        qr_w, qr_h = img.size
        logo_max = int(min(qr_w, qr_h) * 0.22)
        logo.thumbnail((logo_max, logo_max), Image.LANCZOS)
        logo_w, logo_h = logo.size

        # White rounded background behind logo
        pad = 10
        bg = Image.new("RGBA", (logo_w + pad*2, logo_h + pad*2), (255, 255, 255, 255))
        bg_x = (qr_w - bg.width) // 2
        bg_y = (qr_h - bg.height) // 2
        img.paste(bg, (bg_x, bg_y))
        img.paste(logo, (bg_x + pad, bg_y + pad), logo)

    # ── Export ──
    buf = BytesIO()
    if output_format == "JPEG":
        img_rgb = img.convert("RGB")
        img_rgb.save(buf, format="JPEG", quality=95)
        mime = "image/jpeg"
        ext = "jpg"
    else:
        img.save(buf, format="PNG")
        mime = "image/png"
        ext = "png"

    return buf.getvalue(), mime, ext, img

# ── UI ───────────────────────────────────────────────────────────────────────
st.title("🔗 QR Code Generator")
st.write("Paste a link below, customise, and generate a QR code instantly.")

link = st.text_input("Paste your link here", placeholder="https://example.com")

# ── Section: Colors ──
st.markdown("### 🎨 Colors")
col1, col2 = st.columns(2)
with col1:
    fg_color = st.color_picker("QR Color (foreground)", value="#000000")
with col2:
    bg_color = st.color_picker("Background Color", value="#FFFFFF")

# ── Section: Size & Error Correction ──
st.markdown("### ⚙️ Settings")
col3, col4 = st.columns(2)
with col3:
    box_size = st.slider("QR Size", min_value=5, max_value=20, value=10,
                         help="Controls the pixel size of each QR module")
with col4:
    ec_level = st.selectbox(
        "Error Correction",
        options=["L", "M", "Q", "H"],
        index=3,
        help="H = highest redundancy (required for logo). L = smallest file size."
    )

# ── Section: Logo ──
st.markdown("### 🖼️ Logo Overlay (optional)")
logo_file = st.file_uploader(
    "Upload a logo to embed in the center",
    type=["png", "jpg", "jpeg", "webp"],
    help="Works best with error correction set to H"
)
if logo_file and ec_level != "H":
    st.warning("⚠️ For best results with a logo, set Error Correction to **H**.")

# ── Section: Output Format ──
st.markdown("### 💾 Output Format")
output_format = st.selectbox("Download as", options=["PNG", "JPEG"], index=0)

# ── Generate ──
st.markdown("###")
if st.button("⬡ Generate QR Code"):
    if not link.strip():
        st.error("Please paste a valid URL before generating.")
    else:
        with st.spinner("Generating…"):
            qr_bytes, mime, ext, img_preview = generate_qr(
                link.strip(), fg_color, bg_color,
                box_size, ec_level, logo_file, output_format
            )

        st.image(qr_bytes, caption="Your QR Code", use_container_width=False, width=280)

        col_dl1, col_dl2 = st.columns(2)
        with col_dl1:
            st.download_button(
                f"↓ Download as {output_format}",
                data=qr_bytes,
                file_name=f"qr_code.{ext}",
                mime=mime
            )
        with col_dl2:
            # Offer the alternate format too
            alt_format = "JPEG" if output_format == "PNG" else "PNG"
            alt_bytes, alt_mime, alt_ext, _ = generate_qr(
                link.strip(), fg_color, bg_color,
                box_size, ec_level, logo_file, alt_format
            )
            st.download_button(
                f"↓ Download as {alt_format}",
                data=alt_bytes,
                file_name=f"qr_code.{alt_ext}",
                mime=alt_mime
            )
