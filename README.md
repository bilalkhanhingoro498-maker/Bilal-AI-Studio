# Bilal AI Studio — Phase 1 (Voice + Lip Sync UI)

This Streamlit prototype includes:
- Text-to-video / photo-to-video request builder
- Voiceover and multi-character dialogue fields
- English, Urdu, and mixed Urdu-English language selection
- Voice style and delivery options
- Optional recorded audio and voice reference uploads
- Optional talking-portrait image input for lip-sync requests
- Saved request history

## Important
This is a **UI/request builder**, not a working video/voice generation backend yet. It saves request JSON and uploaded files in `user_data/`. Streamlit Community Cloud storage is not durable, and its free resources are limited. Do not treat it as permanent storage.

## Run locally
```bash
python -m venv .venv
```
Windows PowerShell:
```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

## Free-first backend plan
- Evaluate the open-source Urdu TTS project for Urdu speech; validate the model and license before deployment.
- SadTalker is a candidate for animating a single portrait from audio.
- MuseTalk is a candidate for syncing audio to an existing video.
- Run inference on an available GPU runtime; free GPU sessions are limited and may disconnect.
- Connect Google Drive later for output storage.

Never upload API keys or private credentials to GitHub. Use only voices and likenesses you own or have permission to use.
