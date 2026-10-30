import streamlit as st
from pathlib import Path
from datetime import datetime
import json

APP_DIR = Path(__file__).parent
DATA_DIR = APP_DIR / "user_data"
UPLOAD_DIR = DATA_DIR / "uploads"
REQUEST_DIR = DATA_DIR / "generation_requests"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
REQUEST_DIR.mkdir(parents=True, exist_ok=True)

st.set_page_config(page_title="Bilal AI Studio", page_icon="🎬", layout="wide")

st.markdown("""
<style>
.block-container {padding-top: 2rem; max-width: 1120px;}
.hero {padding: 1.4rem; border-radius: 16px; background: linear-gradient(120deg,#172554,#312e81); color: white;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>🎬 Bilal AI Studio</h1><p>Personal AI video workspace · Video · Voice · Lip Sync</p></div>', unsafe_allow_html=True)
st.write("")

with st.sidebar:
    st.header("Video settings")
    video_mode = st.radio("Video creation", ["Text to Video", "Photo to Video"])
    duration = st.selectbox("Clip duration", [10], format_func=lambda x: f"{x} seconds")
    resolution = st.selectbox("Target resolution", ["480p", "720p"])
    st.divider()
    st.caption("Phase 1: interface and request builder")
    st.caption("Generation services are not connected yet.")

video_tab, voice_tab, history_tab = st.tabs(["🎥 Video", "🎙️ Voice & Lip Sync", "📁 Saved requests"])

with video_tab:
    st.subheader("Create your scene")
    prompt = st.text_area("Visual prompt", placeholder="Describe the scene, camera movement, lighting and character actions...", height=130)
    video_image = st.file_uploader("Starting image (required for Photo to Video)", type=["png", "jpg", "jpeg", "webp"], key="video_image")
    if video_mode == "Photo to Video" and video_image:
        st.image(video_image, caption="Starting image", use_container_width=True)
    negative_prompt = st.text_input("Negative prompt (optional)", placeholder="blurry, distorted face, flicker...")

with voice_tab:
    st.subheader("Voiceover and character dialogue")
    audio_mode = st.radio("Audio type", ["AI voiceover", "Multiple character dialogues", "Upload recorded audio"], horizontal=False)
    language = st.selectbox("Dialogue language", ["English", "Urdu", "Urdu + English"])
    voice_style = st.selectbox("Voice style", ["Male", "Female", "Childlike", "Choose per character"])
    voice_tone = st.selectbox("Speaking style", ["Natural", "Friendly", "Dramatic", "Emotional", "Calm"])
    voice_text = st.text_area("Voiceover text / dialogue script", placeholder="Enter the exact words you want spoken...", height=120)
    voice_reference = st.file_uploader("Optional voice sample (only use a voice you own or have permission to use)", type=["wav", "mp3", "m4a"], key="voice_reference")
    recorded_audio = st.file_uploader("Optional recorded dialogue/audio file", type=["wav", "mp3", "m4a"], key="recorded_audio")

    st.divider()
    st.subheader("Lip sync")
    enable_lipsync = st.checkbox("Enable lip sync for a speaking character", value=True)
    lipsync_image = st.file_uploader("Character portrait for talking-photo animation", type=["png", "jpg", "jpeg", "webp"], key="lipsync_image")
    st.caption("For a single portrait + speech audio, a talking-head engine such as SadTalker is a possible backend. It needs GPU resources for practical speed.")
    st.caption("For an existing video + audio lip-sync workflow, a separate video lip-sync engine such as MuseTalk may be used.")

    if lipsync_image:
        st.image(lipsync_image, caption="Lip-sync character portrait", width=260)

with st.expander("Free engine plan"):
    st.markdown("""
    - **Speech:** evaluate an open-source Urdu TTS model for Urdu and English voice generation.
    - **Talking photo:** SadTalker is a candidate for portrait + audio animation.
    - **Video lip sync:** MuseTalk is a candidate for an existing video + audio.
    - **Important:** the free Streamlit website hosts the controls only; it does not provide the GPU needed to render these models.
    """)

prepare = st.button("Prepare video + voice request", type="primary", use_container_width=True)

if prepare:
    errors = []
    if not prompt.strip():
        errors.append("Enter a visual prompt.")
    if video_mode == "Photo to Video" and video_image is None:
        errors.append("Upload a starting image for Photo to Video.")
    if audio_mode != "Upload recorded audio" and not voice_text.strip():
        errors.append("Enter the voiceover text or dialogue.")
    if audio_mode == "Upload recorded audio" and recorded_audio is None:
        errors.append("Upload an audio file.")
    if enable_lipsync and lipsync_image is None and video_mode != "Photo to Video":
        errors.append("Upload a character portrait for the lip-sync request, or turn lip sync off.")
    if errors:
        for err in errors:
            st.error(err)
    else:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        saved_files = {}

        for label, uploaded in [
            ("video_image", video_image),
            ("voice_reference", voice_reference),
            ("recorded_audio", recorded_audio),
            ("lipsync_image", lipsync_image),
        ]:
            if uploaded is not None:
                suffix = Path(uploaded.name).suffix.lower() or ".bin"
                filename = f"{stamp}_{label}{suffix}"
                (UPLOAD_DIR / filename).write_bytes(uploaded.getvalue())
                saved_files[label] = filename

        request_data = {
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "video_mode": video_mode,
            "duration_seconds": duration,
            "resolution": resolution,
            "visual_prompt": prompt.strip(),
            "negative_prompt": negative_prompt.strip(),
            "audio_mode": audio_mode,
            "language": language,
            "voice_style": voice_style,
            "voice_tone": voice_tone,
            "voice_text": voice_text.strip(),
            "enable_lipsync": enable_lipsync,
            "uploaded_files": saved_files,
            "status": "waiting_for_generation_backend"
        }
        request_file = REQUEST_DIR / f"request_{stamp}.json"
        request_file.write_text(json.dumps(request_data, indent=2, ensure_ascii=False), encoding="utf-8")
        st.success("Video + voice request saved in this app workspace.")
        st.warning("This version prepares the request only. It does not yet generate speech, animate lips, or render a video.")

st.divider()
st.subheader("Current system status")
c1, c2, c3 = st.columns(3)
c1.metric("Video duration", "10 seconds")
c2.metric("Audio features", "Voice + dialogue")
c3.metric("Lip sync", "Request option")
st.info("Next development step: connect a GPU-backed speech and lip-sync service. Free cloud GPU availability is limited and not guaranteed.")

st.subheader("Recent requests")
requests = sorted(REQUEST_DIR.glob("request_*.json"), reverse=True)
if not requests:
    st.caption("No requests saved yet.")
else:
    for file in requests[:10]:
        try:
            item = json.loads(file.read_text(encoding="utf-8"))
            with st.expander(f'{item["created_at"]} · {item["video_mode"]} · {item["audio_mode"]}'):
                st.write(item["visual_prompt"])
                st.write("Dialogue:", item["voice_text"] or "Audio upload")
                st.json(item)
        except Exception:
            st.caption(f"Could not read {file.name}")

st.divider()
st.caption("Bilal AI Studio · Personal prototype · Only upload voices/images you own or have permission to use.")
