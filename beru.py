import streamlit as st
import yt_dlp
import os

# ---- UI Styling ----
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0d1b2a, #000000);
    color: white;
}
.title {
    font-size: 4rem;
    font-weight: 900;
    text-align: center;
    color: #00bfff;
    text-shadow:
        0 0 5px #00bfff,
        0 0 10px #00bfff,
        0 0 20px #00bfff,
        0 0 40px #00bfff,
        0 0 80px #00bfff;
    margin-top: 50px;
    margin-bottom: 20px;
}
.link-input {
    font-size: 1.2rem;
    padding: 12px;
    border-radius: 8px;
    border: 2px solid #50b7f5;
    width: 100%;
    max-width: 700px;
    margin: auto;
    display: block;
    background-color: #001529;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---- UI Elements ----
st.markdown('<div class="title">BERU</div>', unsafe_allow_html=True)
st.markdown("""
    <h3 style='text-align: center; color: #a3bffa; font-style: italic; margin-top: -20px;'>
        Are you the King of Humans?
    </h3>
""", unsafe_allow_html=True)

# Input fields
link = st.text_input("📎 Paste your YouTube link here 💅", key="ytlink", placeholder="https://youtube.com/...")
choice = st.radio("🎛️ Choose your domain:", ["Video", "Audio"], horizontal=True)
res = None
if choice == "Video":
    res = st.selectbox("📏 Choose resolution:", ["360p", "480p", "720p", "1080p", "best"])

# ---- Download function ----
def download_video(link, choice, res=None):
    folder = "Downloads/Videos" if choice == "Video" else "Downloads/Music"
    os.makedirs(folder, exist_ok=True)

    ydl_opts = {
        'outtmpl': os.path.join(folder, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'quiet': True,
    }

    if choice == "Audio":
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    else:
        if res != "best":
            height = res[:-1]  # Remove 'p' from '720p' etc
            ydl_opts['format'] = f"bestvideo[height={height}]+bestaudio/best"
        else:
            ydl_opts['format'] = "best"

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            filename = ydl.prepare_filename(info)
            return filename
    except Exception as e:
        return f"error::{str(e)}"

# ---- Trigger Download ----
if st.button("⬇️ Start Download"):
    if not link:
        st.warning("Are we downloading air today? 🫠")
    else:
        result = download_video(link, choice, res)
        if result.startswith("error::"):
            st.error(f"⚠️ Something went wrong: {result[7:]}")
        else:
            st.success(f"✅ Beru never fails. ARISE.\nFile saved to: {result}")
            st.balloons()

st.markdown("""
<style>
.footer {
    text-align: center;
    color: #888;
    font-size: 0.9rem;
    margin-top: 40px;
    padding: 10px 0;
    border-top: 1px solid #222;
}
</style>
<div class="footer">
© 2025 prodigy. All rights reserved. Do not steal. Seriously. 😎
</div>
""", unsafe_allow_html=True)
