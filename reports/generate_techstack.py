import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

C_BG     = "#F0F4FF"
C_WHITE  = "#FFFFFF"
C_INDIGO = "#4F46E5"
C_DARK   = "#0F172A"
C_CORAL  = "#EF4444"
C_GRAY   = "#94A3B8"
C_TEXT   = "#1E293B"
C_SUB    = "#64748B"

COLUMNS = [
    {
        "label": "FRONTEND",
        "color": C_INDIGO,
        "items": [
            ("React 18",          "UI library utama"),
            ("Three.js / R3F",    "Visualisasi 3D jantung"),
            ("Tailwind CSS",      "Styling utility-first"),
            ("Vite",              "Build tool & dev server"),
            ("Framer Motion",     "Animasi & page transition"),
            ("React Router DOM",  "Client-side routing"),
        ],
    },
    {
        "label": "BACKEND",
        "color": C_DARK,
        "items": [
            ("Node.js + Express",   "REST API server"),
            ("Axios",               "HTTP proxy ke ML API"),
            ("Helmet",              "Security middleware"),
            ("Morgan",              "HTTP request logging"),
            ("CORS",                "Cross-origin resource sharing"),
            ("Hugging Face Spaces", "Deployment via Docker"),
        ],
    },
    {
        "label": "ML / AI",
        "color": C_CORAL,
        "items": [
            ("Python + FastAPI",      "ML API serving"),
            ("TensorFlow / Keras",    "Deep learning model"),
            ("scikit-learn",          "Preprocessing & metrics"),
            ("SHAP",                  "Model explainability"),
            ("SMOTE (imb-learn)",     "Penanganan class imbalance"),
            ("Google Gemini AI",      "Rekomendasi personal"),
        ],
    },
]

# ── Figure ────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(11, 7))
ax.set_xlim(0, 11)
ax.set_ylim(0, 7)
ax.axis("off")
fig.patch.set_facecolor(C_BG)
ax.set_facecolor(C_BG)

# ── Title ─────────────────────────────────────────────────────────────────────
ax.text(0.3, 6.72, "Tech Stack",
        fontsize=22, weight="bold", color=C_TEXT, va="center")
ax.text(0.3, 6.35, "Teknologi yang digunakan untuk membangun Pulsevera",
        fontsize=10, color=C_SUB, va="center")

# ── Columns ───────────────────────────────────────────────────────────────────
COL_W    = 3.2
COL_GAP  = 0.2
X_STARTS = [0.3, 0.3 + COL_W + COL_GAP, 0.3 + 2 * (COL_W + COL_GAP)]
Y_TOP    = 6.0
HDR_H    = 0.42
ITEM_H   = 0.60
ITEM_PAD = 0.08

for col_idx, col in enumerate(COLUMNS):
    x0 = X_STARTS[col_idx]

    # Header bar
    ax.add_patch(FancyBboxPatch((x0, Y_TOP - HDR_H), COL_W, HDR_H,
                 boxstyle="round,pad=0.05",
                 facecolor=col["color"], edgecolor="none", zorder=3))
    ax.text(x0 + COL_W / 2, Y_TOP - HDR_H / 2, col["label"],
            ha="center", va="center", fontsize=10.5, weight="bold",
            color=C_WHITE, zorder=4)

    # Item cards
    for i, (title, subtitle) in enumerate(col["items"]):
        y_card = Y_TOP - HDR_H - ITEM_PAD - (i + 1) * (ITEM_H + ITEM_PAD) + ITEM_H
        y_top_card = y_card
        y_bot_card = y_card - ITEM_H

        ax.add_patch(FancyBboxPatch((x0, y_bot_card), COL_W, ITEM_H,
                     boxstyle="round,pad=0.04",
                     facecolor=C_WHITE, edgecolor="#E2E8F0",
                     linewidth=0.8, zorder=2))

        # Color accent bar on left
        ax.add_patch(FancyBboxPatch((x0, y_bot_card), 0.06, ITEM_H,
                     boxstyle="round,pad=0.0",
                     facecolor=col["color"], edgecolor="none",
                     alpha=0.85, zorder=3))

        ax.text(x0 + 0.16, y_bot_card + ITEM_H * 0.62, title,
                fontsize=9.5, weight="bold", color=C_TEXT,
                va="center", zorder=4)
        ax.text(x0 + 0.16, y_bot_card + ITEM_H * 0.28, subtitle,
                fontsize=8, color=C_SUB, va="center", zorder=4)

# ── Deployment footer ─────────────────────────────────────────────────────────
Y_DEP = 0.18
ax.add_patch(FancyBboxPatch((0.3, Y_DEP - 0.16), 10.4, 0.38,
             boxstyle="round,pad=0.04",
             facecolor="#EEF2FF", edgecolor="#C7D2FE",
             linewidth=0.8, zorder=2))

ax.text(0.5, Y_DEP + 0.06, "Deployment",
        fontsize=8.5, weight="bold", color=C_TEXT, va="center")

dep_items = [
    (C_INDIGO, "Frontend",  "Vercel (auto-deploy dari GitHub)"),
    (C_DARK,   "Backend",   "Hugging Face Spaces — Docker (Node.js 20)"),
    (C_CORAL,  "ML API",    "Hugging Face Spaces — Docker (Python 3.11 + TF 2.17)"),
]
dep_x = [1.8, 5.0, 8.0]
for (color, label, desc), dx in zip(dep_items, dep_x):
    ax.add_patch(mpatches.FancyBboxPatch((dx - 0.08, Y_DEP - 0.09), 0.12, 0.20,
                 boxstyle="round,pad=0.02",
                 facecolor=color, edgecolor="none", zorder=3))
    ax.text(dx + 0.12, Y_DEP + 0.03, label,
            fontsize=8.5, weight="bold", color=C_TEXT, va="center", zorder=4)
    ax.text(dx + 0.12, Y_DEP - 0.1, desc,
            fontsize=7.5, color=C_SUB, va="center", zorder=4)

plt.tight_layout(pad=0.5)
plt.savefig("reports/Tech stack.png", dpi=150,
            bbox_inches="tight", facecolor=C_BG)
print("Saved: reports/Tech stack.png")
