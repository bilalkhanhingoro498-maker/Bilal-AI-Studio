import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(page_title="Bilal AI Studio", page_icon="🎬")
st.title("🎬 Bilal AI Studio")

prompt = st.text_area("Prompt", placeholder="Describe the scene, camera movement, lighting...", height=120)
photo = st.file_uploader("Reference photo (optional)", type=["png", "jpg", "jpeg", "webp"])
if photo:
    st.image(photo, width=200)

if st.button("Generate video", type="primary"):
    if not prompt.strip():
        st.error("Please write a prompt first.")
    else:
        try:
            client = InferenceClient(provider="fal-ai", api_key=st.secrets["HF_TOKEN"])
            with st.spinner("Generating video, please wait 1-3 minutes..."):
                if photo:
                    video = client.image_to_video(photo.getvalue(), prompt=prompt, model="Wan-AI/Wan2.2-I2V-A14B")
                else:
                    video = client.text_to_video(prompt, model="Wan-AI/Wan2.2-T2V-A14B")
            st.video(video)
            st.download_button("Download video", video, "video.mp4", "video/mp4")
        except Exception as e:
            st.error(f"Generation failed: {e}")
