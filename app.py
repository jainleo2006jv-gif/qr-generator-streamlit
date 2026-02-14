import streamlit as st
import qrcode
from io import BytesIO

st.set_page_config(page_title="QR Generator", page_icon="🔗")

st.title("🔗 Link to QR Code Generator")
st.write("Paste a link below and generate a QR code.")

link = st.text_input("Paste your link here", placeholder="https://example.com")

if st.button("Generate QR"):
    if not link.strip():
        st.error("Don’t click generate with an empty link. Paste a real URL.")
    else:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(link)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        qr_bytes = buffer.getvalue()

        st.image(qr_bytes, caption="Your QR Code")
        st.download_button(
            "Download QR Code",
            data=qr_bytes,
            file_name="qr_code.png",
            mime="image/png"
        )
