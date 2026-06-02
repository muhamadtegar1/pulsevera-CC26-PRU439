---
title: Pulsevera ML API
emoji: ❤️
colorFrom: red
colorTo: pink
sdk: docker
pinned: false
license: mit
app_port: 7860
---

# Pulsevera ML API

FastAPI inference endpoint untuk prediksi risiko penyakit jantung.

## Endpoints

| Method | Path | Deskripsi |
|---|---|---|
| GET | `/` | Info API |
| GET | `/health` | Status model + Gemini |
| GET | `/api/v1/metadata` | Metadata model + SHAP importance |
| POST | `/api/v1/predict` | Prediksi risiko (ML/DL) |

## Environment Variables

Set di Hugging Face Space Settings:

```
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.5-flash
GEMINI_ENABLED=true
```

## Model Files

Model files besar (pkl) perlu di-upload manual via HF Git LFS:

```bash
# Install git-lfs
git lfs install
git lfs track "models/*.pkl" "models/shap_explainer.pkl"
git add .gitattributes
git add models/
git commit -m "add model files via LFS"
git push
```

Model .keras (692KB) sudah di-track langsung.
