# 🕵️ DeepSafe — DeepFake Face Detector

A multi-section web app (Home / About / How It Works / Detection / Login) that
classifies face images as **real** or **AI-generated / fake**, with confidence
scores and a Grad-CAM heatmap showing what the model focused on.

## Project structure
```
deepfake-detector/
├── app.py                   # Router: navbar + page switching
├── views/
│   ├── shared.py            # Global CSS, navbar, footer
│   ├── home.py               # Landing / hero page
│   ├── about.py
│   ├── how_it_works.py
│   ├── detection.py          # The actual analyzer (single + batch)
│   └── login.py               # UI placeholder — no real auth wired up
├── utils/
│   └── model_utils.py        # Model architecture, loading, Grad-CAM
├── model/
│   └── best_model.pth        # <- put your trained weights here (not committed)
├── requirements.txt
├── .env.example
└── .gitignore
```

> **Note on `views/` vs `pages/`:** the folder is deliberately named `views/`,
> not `pages/`. Streamlit auto-generates a sidebar navigation menu for any
> folder literally named `pages/` next to `app.py` — renaming avoids that and
> lets the custom top navbar be the only navigation the user sees.

## Setup (VS Code / local machine)

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows: venv\Scripts\activate
   # Mac/Linux: source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Put your trained weights at `model/best_model.pth` (download the file you saved from Kaggle at `/kaggle/working/deepfake_model/best_model.pth`).

4. Copy `.env.example` to `.env` and check the path:
   ```
   MODEL_PATH=model/best_model.pth
   ```

5. Run it:
   ```bash
   streamlit run app.py
   ```

The app opens at `http://localhost:8501`.

## Features
- Landing page with hero section, feature highlights, and CTA buttons
- About and How It Works sections explaining the project
- Single-image analysis with confidence gauges for both classes
- Batch upload — analyze many images at once, get a summary table
- Grad-CAM heatmap overlay so you can show *why* the model made a call (great for a demo)
- Downloadable text report per prediction
- Low-confidence warning banner (configurable threshold)
- Session history of recent predictions
- Login page UI (visual only — see note below)

## Using your own hero image
Drop any photo at `assets/hero_image.png` (or set `HERO_IMAGE_PATH` in `.env`
to point elsewhere — JPG works too). It's automatically:
- darkened and slightly desaturated (`brightness(0.6) contrast(1.15) saturate(0.85)`)
- covered with a navy gradient wash
- given a cyan/teal glow in the upper area

...so any image you drop in comes out matching the dark-navy, cyan-glow tone
of the rest of the site, regardless of its original lighting. If it still
looks off (too dark/too washed out) for your specific photo, tell me and I'll
tune the filter values.

## About the Login page
The Login section is a **visual placeholder only**. There's no backend
authentication wired up — clicking "Sign In" shows a message explaining this
rather than pretending to log you in. If you want real accounts later, the
cleanest options are Firebase Auth, Supabase Auth, or a small FastAPI backend
with JWT — happy to help wire one up when you're ready.

## Deploying later
- **Streamlit Community Cloud**: push this repo to GitHub, then connect it at share.streamlit.io. Because `model/*.pth` is gitignored, you'll need to either use **Git LFS** for the weights or host them externally (e.g. Hugging Face Hub, S3, Google Drive) and download them at app startup.
- **Hugging Face Spaces**: works well for PyTorch + Streamlit; weights can live directly in the Space repo.

## Notes
- The model architecture in `utils/model_utils.py` must exactly match the one used during training — if you retrain with a different `IMG_SIZE` or layer sizes, update it here too.
- This is a research/demo tool, not a forensic-grade detector — say so if you present it.
