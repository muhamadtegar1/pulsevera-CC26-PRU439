import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

C_INDIGO = "#4F46E5"
C_BLUE   = "#2563EB"
C_AMBER  = "#F59E0B"
C_MINT   = "#10B981"
C_CORAL  = "#EF4444"
C_DARK   = "#0F172A"
C_GRAY   = "#94A3B8"
C_BG     = "#FFFFFF"

def box(ax, cx, cy, w, h, color, title, subtitle="", title_size=10, sub_size=8):
    ax.add_patch(FancyBboxPatch((cx - w/2, cy - h/2), w, h,
                 boxstyle="round,pad=0.025", linewidth=1.4,
                 edgecolor=color, facecolor=color, zorder=3))
    if subtitle:
        ax.text(cx, cy + 0.12, title, ha="center", va="center",
                fontsize=title_size, color="white", weight="bold", zorder=4)
        ax.text(cx, cy - 0.14, subtitle, ha="center", va="center",
                fontsize=sub_size, color="white", alpha=0.92, zorder=4,
                multialignment="center")
    else:
        ax.text(cx, cy, title, ha="center", va="center",
                fontsize=title_size, color="white", weight="bold", zorder=4)

def arr(ax, cx, y0, y1):
    ax.annotate("", xy=(cx, y1 + 0.02), xytext=(cx, y0 - 0.02),
                arrowprops=dict(arrowstyle="-|>", color=C_GRAY,
                                lw=1.6, mutation_scale=15), zorder=2)


# ── Figure ────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(6, 9))
ax.set_xlim(0, 1)
ax.set_ylim(0, 9)
ax.axis("off")
fig.patch.set_facecolor(C_BG)

CX = 0.5
W  = 0.70
H  = 0.72

# Y positions (top → bottom)
YS = [8.2, 6.9, 5.6, 4.3, 3.0, 1.7]

# ── Title ─────────────────────────────────────────────────────────────────────
ax.text(CX, 8.75, "Pulsevera — User Flow",
        ha="center", fontsize=13, weight="bold", color=C_DARK)

# ── 6 Shapes ──────────────────────────────────────────────────────────────────
NODES = [
    (C_INDIGO, "Landing Page",
               "Hero · Statistik · Cara Kerja · FAQ"),
    (C_BLUE,   "Input Form  (5 Langkah)",
               "Profil · Antropometri · Gaya Hidup · Konsumsi · Kondisi Kesehatan"),
    (C_AMBER,  "ML Processing",
               "Deep Learning Inference · SHAP Attribution · Gemini AI  (~350 ms)"),
    (C_CORAL,  "Estimasi Risiko Serangan Jantung",
               "Probabilitas %  ·  Label: Rendah / Sedang / Tinggi"),
    (C_MINT,   "Skor Gaya Hidup & Rekomendasi",
               "Skor 0-5  ·  5 Kebiasaan  ·  Top 3 Faktor SHAP  ·  Saran Gemini AI"),
    (C_INDIGO, "Selesai",
               "Kembali ke Beranda  /  Cek Ulang"),
]

for i, (color, title, subtitle) in enumerate(NODES):
    box(ax, CX, YS[i], W, H, color, title, subtitle)
    if i < len(YS) - 1:
        arr(ax, CX, YS[i] - H/2, YS[i+1] + H/2)

# ── Loop "Cek Ulang" arrow ─────────────────────────────────────────────────
ax.annotate("", xy=(CX + W/2, YS[1] - 0.05),
            xytext=(CX + W/2, YS[5] - 0.05),
            arrowprops=dict(arrowstyle="-|>", color=C_BLUE, lw=1.3,
                            connectionstyle="arc3,rad=-0.5",
                            mutation_scale=12), zorder=2)
ax.text(0.93, (YS[1] + YS[5]) / 2, "Cek\nUlang",
        ha="center", va="center", fontsize=7, color=C_BLUE,
        multialignment="center")

# ── Disclaimer ────────────────────────────────────────────────────────────────
ax.text(CX, 0.95,
        "Alat edukasi — bukan pengganti diagnosis dokter",
        ha="center", fontsize=7.5, color=C_CORAL, style="italic")
ax.text(CX, 0.65,
        "CDC BRFSS 2022  ·  445.132 responden  ·  Accuracy 85.76%  ·  Recall 71.15%  ·  ROC-AUC 88.12%",
        ha="center", fontsize=6.8, color=C_GRAY)

# ── Legend ────────────────────────────────────────────────────────────────────
legend_items = [
    mpatches.Patch(facecolor=C_INDIGO, label="Navigasi"),
    mpatches.Patch(facecolor=C_BLUE,   label="Input Form"),
    mpatches.Patch(facecolor=C_AMBER,  label="ML Processing"),
    mpatches.Patch(facecolor=C_CORAL,  label="Risiko"),
    mpatches.Patch(facecolor=C_MINT,   label="Output & Rekomendasi"),
]
ax.legend(handles=legend_items, loc="lower center",
          bbox_to_anchor=(0.5, 0.01), ncol=5,
          fontsize=7, frameon=True, framealpha=0.9, edgecolor=C_GRAY)

plt.tight_layout()
plt.savefig("reports/userflow_pulsevera.png", dpi=150,
            bbox_inches="tight", facecolor=C_BG)
print("Saved: reports/userflow_pulsevera.png")
