import streamlit as st
from pydub import AudioSegment
import io

st.title("🔥 Buto's Chop & Screw Studio")

uploaded_file = st.file_uploader("Upload your MP3", type="mp3")
speed_factor = st.slider("Slowdown (% speed)", 50, 100, 75) / 100
chop_interval = st.slider("Chop every X seconds", 1, 10, 3) * 1000
chop_length = st.slider("Chop length (ms)", 100, 800, 300)
song_length_min = st.slider("Final song length (minutes)", 3.0, 10.0, 3.5, step=0.5)
max_duration = int(song_length_min * 60 * 1000)

if uploaded_file:
    audio = AudioSegment.from_file(uploaded_file, format="mp3")

    slowed = audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate * speed_factor)
    }).set_frame_rate(audio.frame_rate)

    slowed = slowed[:max_duration]

    chopped = AudioSegment.empty()
    pos = 0
    while pos < len(slowed):
        next_chop = slowed[pos:pos + chop_interval]
        chopped += next_chop
        if pos + chop_length < len(slowed):
            stutter = slowed[pos:pos + chop_length]
            chopped += stutter + stutter
        pos += chop_interval

    out_file = io.BytesIO()
    chopped.export(out_file, format="mp3")
    audio_bytes = out_file.getvalue()

    st.audio(audio_bytes, format="audio/mp3")
    st.download_button("⬇️ Download Your Chopped & Screwed MP3", audio_bytes, file_name="chopped_screwed.mp3")
