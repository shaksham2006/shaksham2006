# Animated GitHub Profile — shaksham2006

1. Create a **public repository named exactly `shaksham2006`**.
2. Copy these files into that repository.
3. Push to `main`.
4. Open **Actions → Update profile art → Run workflow** once.
5. The contribution heatmap will refresh daily.

## Local portrait regeneration

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate

pip install -r scripts/requirements.txt
python scripts/prep_photo.py assets/source-photo.png
python scripts/make_ascii_svg.py
```

Regenerate the portrait/card when your photo or profile details change.
