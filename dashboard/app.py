"""
Pulsevera Dashboard - Predict, Prevent, Prevail
Streamlit dashboard untuk eksplorasi data risiko penyakit jantung.
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Pulsevera - Heart Disease Risk",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).parent.parent
DATA_PATH = BASE_DIR / "data" / "final" / "dataset_final.csv"
SAMPLE_PATH = Path(__file__).parent / "data" / "dataset_sample.csv"

RISK_COLOR = "#e74c3c"
SAFE_COLOR = "#2ecc71"

# ── Data loading ─────────────────────────────────────────────────
@st.cache_data
def load_data():
    if DATA_PATH.exists():
        return pd.read_csv(DATA_PATH)
    # Fallback ke sample 10% untuk Streamlit Cloud
    df = pd.read_csv(SAMPLE_PATH)
    st.info("ℹ️ Menampilkan sample 10% dari dataset (44.5K dari 445K baris). "
            "Data lengkap tersedia di lingkungan lokal.", icon="📊")
    return df

df = load_data()

# ── Sidebar ───────────────────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/color/96/heart-with-pulse.png", width=80)
st.sidebar.title("Pulsevera")
st.sidebar.caption("Predict · Prevent · Prevail")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigasi",
    ["Overview", "EDA Interaktif", "Faktor Risiko", "A/B Testing"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Filter Global**")
age_range = st.sidebar.slider(
    "Rentang Usia (Kode)",
    int(df['AgeCategory'].min()), int(df['AgeCategory'].max()),
    (int(df['AgeCategory'].min()), int(df['AgeCategory'].max()))
)

if 'Sex' in df.columns:
    sex_options = {0: "Perempuan", 1: "Laki-laki", -1: "Semua"}
    sex_choice = st.sidebar.selectbox("Jenis Kelamin", options=[-1, 0, 1],
                                       format_func=lambda x: sex_options[x])
else:
    sex_choice = -1

# Apply global filter
mask = (df['AgeCategory'] >= age_range[0]) & (df['AgeCategory'] <= age_range[1])
if sex_choice != -1 and 'Sex' in df.columns:
    mask &= (df['Sex'] == sex_choice)
df_filtered = df[mask].copy()

st.sidebar.markdown(f"**Data terfilter:** {len(df_filtered):,} baris")

# ═══════════════════════════════════════════════════════════════════
# PAGE 1: OVERVIEW
# ═══════════════════════════════════════════════════════════════════
if page == "Overview":
    st.title("❤️ Pulsevera - Dashboard Risiko Penyakit Jantung")
    st.markdown(
        "Dataset: **CDC BRFSS 2022** | "
        "Role: **Data Scientist** | "
        "Program: **Coding Camp 2026 powered by DBS Foundation**"
    )
    st.markdown("---")

    # KPI cards
    total = len(df_filtered)
    pos_cases = df_filtered['HadHeartAttack'].sum()
    pos_rate = pos_cases / total * 100
    avg_bmi = df_filtered['BMI'].mean() if 'BMI' in df_filtered.columns else 0
    avg_sleep = df_filtered['SleepHours'].mean() if 'SleepHours' in df_filtered.columns else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Data", f"{total:,}")
    c2.metric("Kasus Serangan Jantung", f"{pos_cases:,}", f"{pos_rate:.1f}%")
    c3.metric("Rata-rata BMI", f"{avg_bmi:.1f}")
    c4.metric("Rata-rata Jam Tidur", f"{avg_sleep:.1f} jam")

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Distribusi Target Variable")
        tc = df_filtered['HadHeartAttack'].value_counts()
        fig = px.pie(
            values=tc.values, names=['No (Tidak)', 'Yes (Ya)'],
            color_discrete_sequence=[SAFE_COLOR, RISK_COLOR],
            title="HadHeartAttack"
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Ringkasan Statistik Numerik")
        num_cols = [c for c in ['BMI', 'SleepHours', 'PhysicalHealthDays',
                                 'MentalHealthDays', 'LifestyleRiskScore'] if c in df_filtered.columns]
        st.dataframe(
            df_filtered[num_cols].describe().round(2),
            use_container_width=True
        )

    st.markdown("---")
    st.subheader("Distribusi Fitur Numerik")
    sel_col = st.selectbox("Pilih Kolom", options=num_cols)
    fig = px.histogram(df_filtered, x=sel_col, nbins=50,
                       color='HadHeartAttack',
                       color_discrete_map={0: SAFE_COLOR, 1: RISK_COLOR},
                       labels={'HadHeartAttack': 'Serangan Jantung'},
                       title=f"Distribusi {sel_col} berdasarkan Status Serangan Jantung",
                       barmode='overlay', opacity=0.7)
    st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════
# PAGE 2: EDA INTERAKTIF
# ═══════════════════════════════════════════════════════════════════
elif page == "EDA Interaktif":
    st.title("🔍 Exploratory Data Analysis Interaktif")
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["Univariate", "Bivariate", "Multivariate"])

    with tab1:
        st.subheader("Analisis Univariate")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Distribusi Numerik**")
            num_cols = [c for c in ['BMI', 'SleepHours', 'PhysicalHealthDays',
                                     'MentalHealthDays'] if c in df_filtered.columns]
            chosen_num = st.selectbox("Pilih fitur numerik", num_cols)
            fig = px.histogram(df_filtered, x=chosen_num, nbins=50,
                               color_discrete_sequence=[SAFE_COLOR],
                               title=f"Distribusi {chosen_num}")
            fig.add_vline(x=df_filtered[chosen_num].median(),
                          line_dash="dash", line_color="orange",
                          annotation_text=f"Median: {df_filtered[chosen_num].median():.1f}")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("**Distribusi Kategorik**")
            cat_mapping = {
                'GeneralHealth': {1: 'Poor', 2: 'Fair', 3: 'Good', 4: 'Very good', 5: 'Excellent'},
                'PhysicalActivities': {0: 'Tidak Aktif', 1: 'Aktif'},
                'AlcoholDrinkers': {0: 'Tidak', 1: 'Ya'},
                'Sex': {0: 'Perempuan', 1: 'Laki-laki'},
            }
            cat_cols = [c for c in cat_mapping if c in df_filtered.columns]
            chosen_cat = st.selectbox("Pilih fitur kategorik", cat_cols)
            cnt = df_filtered[chosen_cat].value_counts().reset_index()
            cnt.columns = [chosen_cat, 'count']
            if chosen_cat in cat_mapping:
                cnt[chosen_cat] = cnt[chosen_cat].map(cat_mapping[chosen_cat])
            fig = px.bar(cnt, x=chosen_cat, y='count',
                         color_discrete_sequence=[NEUTRAL_COLOR if 'NEUTRAL_COLOR' in dir() else '#3498db'],
                         title=f"Frekuensi {chosen_cat}")
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Analisis Bivariate")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Fitur Numerik vs Target**")
            num_col_biv = st.selectbox("Pilih fitur numerik", num_cols, key='biv_num')
            fig = px.box(df_filtered, x='HadHeartAttack', y=num_col_biv,
                         color='HadHeartAttack',
                         color_discrete_map={0: SAFE_COLOR, 1: RISK_COLOR},
                         labels={'HadHeartAttack': 'Serangan Jantung'},
                         title=f"{num_col_biv} vs HadHeartAttack")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("**Risiko per Kategori**")
            risk_by = df_filtered.groupby(chosen_cat if 'chosen_cat' in dir() else cat_cols[0])['HadHeartAttack'].mean() * 100
            risk_df = risk_by.reset_index()
            risk_df.columns = ['Kategori', '% Risiko']
            fig = px.bar(risk_df, x='Kategori', y='% Risiko',
                         color='% Risiko',
                         color_continuous_scale='RdYlGn_r',
                         title=f"Risiko HadHeartAttack per {cat_cols[0]}")
            st.plotly_chart(fig, use_container_width=True)

        # Heatmap korelasi
        st.markdown("**Heatmap Korelasi**")
        hm_cols = [c for c in ['BMI', 'SleepHours', 'PhysicalHealthDays', 'MentalHealthDays',
                                 'HadHeartAttack', 'GeneralHealth', 'AgeCategory', 'LifestyleRiskScore']
                   if c in df_filtered.columns]
        corr_mat = df_filtered[hm_cols].corr().round(3)
        fig = px.imshow(corr_mat, color_continuous_scale='RdYlGn',
                        zmin=-1, zmax=1,
                        title="Heatmap Korelasi Fitur Numerik",
                        text_auto=True)
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.subheader("Analisis Multivariate")

        if all(c in df_filtered.columns for c in ['AgeCategory', 'PhysicalActivities', 'HadHeartAttack']):
            st.markdown("**Usia × Aktivitas Fisik → Risiko Jantung**")
            pivot = df_filtered.pivot_table(
                values='HadHeartAttack',
                index='AgeCategory',
                columns='PhysicalActivities',
                aggfunc='mean'
            ) * 100
            pivot = pivot.reset_index()
            pivot = pivot.rename(columns={0: 'Tidak Aktif', 1: 'Aktif'})
            pivot_melt = pivot.melt(id_vars='AgeCategory', var_name='Aktivitas', value_name='Risiko %')
            fig = px.bar(pivot_melt, x='AgeCategory', y='Risiko %', color='Aktivitas',
                         barmode='group',
                         color_discrete_map={'Aktif': SAFE_COLOR, 'Tidak Aktif': RISK_COLOR},
                         title="Risiko Serangan Jantung: Usia × Aktivitas Fisik")
            st.plotly_chart(fig, use_container_width=True)

        if 'LifestyleRiskScore' in df_filtered.columns:
            st.markdown("**Lifestyle Risk Score → Risiko Jantung**")
            lrs_risk = df_filtered.groupby('LifestyleRiskScore')['HadHeartAttack'].agg(
                ['mean', 'count']).reset_index()
            lrs_risk.columns = ['Score', 'Risiko %', 'Jumlah']
            lrs_risk['Risiko %'] *= 100
            fig = px.bar(lrs_risk, x='Score', y='Risiko %',
                         color='Risiko %',
                         color_continuous_scale='RdYlGn_r',
                         text='Risiko %',
                         title="Lifestyle Risk Score vs % Risiko Serangan Jantung")
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════
# PAGE 3: FAKTOR RISIKO
# ═══════════════════════════════════════════════════════════════════
elif page == "Faktor Risiko":
    st.title("⚠️ Analisis Faktor Risiko")
    st.markdown("---")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Top 15 Fitur Berkorelasi dengan Risiko Jantung")
        corr = df_filtered.corrwith(df_filtered['HadHeartAttack']).drop('HadHeartAttack')
        corr = corr.dropna().sort_values(key=abs, ascending=False).head(15)
        corr_df = pd.DataFrame({'Fitur': corr.index, 'Korelasi': corr.values})
        corr_df['Warna'] = corr_df['Korelasi'].apply(
            lambda x: 'Positif (Meningkatkan Risiko)' if x > 0 else 'Negatif (Menurunkan Risiko)')
        fig = px.bar(corr_df.sort_values('Korelasi'), x='Korelasi', y='Fitur',
                     orientation='h', color='Warna',
                     color_discrete_map={
                         'Positif (Meningkatkan Risiko)': RISK_COLOR,
                         'Negatif (Menurunkan Risiko)': SAFE_COLOR
                     },
                     title="Korelasi Fitur dengan HadHeartAttack")
        fig.add_vline(x=0, line_color='black')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Ringkasan Faktor Risiko Gaya Hidup")
        lifestyle_factors = {
            'Tidak Aktif Fisik': (df_filtered['PhysicalActivities'] == 0).mean() * 100 if 'PhysicalActivities' in df_filtered.columns else 0,
            'Perokok Aktif': (df_filtered['IsActiveSmoker'] == 1).mean() * 100 if 'IsActiveSmoker' in df_filtered.columns else 0,
            'Obesitas (BMI>30)': (df_filtered['IsObese'] == 1).mean() * 100 if 'IsObese' in df_filtered.columns else 0,
            'Kurang Tidur (<6 jam)': (df_filtered['IsSleepDeprived'] == 1).mean() * 100 if 'IsSleepDeprived' in df_filtered.columns else 0,
            'Konsumsi Alkohol': (df_filtered['AlcoholDrinkers'] == 1).mean() * 100 if 'AlcoholDrinkers' in df_filtered.columns else 0,
        }
        lf_df = pd.DataFrame({'Faktor': list(lifestyle_factors.keys()),
                               '% Populasi': list(lifestyle_factors.values())})
        fig = px.bar(lf_df.sort_values('% Populasi'), x='% Populasi', y='Faktor',
                     orientation='h', color='% Populasi',
                     color_continuous_scale='Oranges',
                     title="Prevalensi Faktor Risiko Gaya Hidup")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("Risiko per Faktor Gaya Hidup")
    risk_summary = []
    for factor, col, val in [
        ('Tidak Aktif Fisik', 'PhysicalActivities', 0),
        ('Perokok Aktif', 'IsActiveSmoker', 1),
        ('Obesitas', 'IsObese', 1),
        ('Kurang Tidur', 'IsSleepDeprived', 1),
        ('Minum Alkohol', 'AlcoholDrinkers', 1),
    ]:
        if col in df_filtered.columns:
            with_factor = df_filtered[df_filtered[col] == val]['HadHeartAttack'].mean() * 100
            without_factor = df_filtered[df_filtered[col] != val]['HadHeartAttack'].mean() * 100
            risk_summary.append({
                'Faktor Risiko': factor,
                'Dengan Faktor (%)': round(with_factor, 2),
                'Tanpa Faktor (%)': round(without_factor, 2),
                'Selisih Risiko (%)': round(with_factor - without_factor, 2)
            })

    if risk_summary:
        rs_df = pd.DataFrame(risk_summary)
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Dengan Faktor', x=rs_df['Faktor Risiko'],
                             y=rs_df['Dengan Faktor (%)'], marker_color=RISK_COLOR))
        fig.add_trace(go.Bar(name='Tanpa Faktor', x=rs_df['Faktor Risiko'],
                             y=rs_df['Tanpa Faktor (%)'], marker_color=SAFE_COLOR))
        fig.update_layout(barmode='group',
                          title='Perbandingan Risiko: Ada vs Tidak Ada Faktor',
                          yaxis_title='% HadHeartAttack = Yes')
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(rs_df, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════
# PAGE 4: A/B TESTING
# ═══════════════════════════════════════════════════════════════════
elif page == "A/B Testing":
    from scipy import stats as scipy_stats

    st.title("🧪 A/B Testing - Uji Hipotesis Statistik")
    st.markdown("Validasi statistik untuk membuktikan signifikansi faktor risiko penyakit jantung.")
    st.markdown("---")

    alpha = st.slider("Significance Level (α)", 0.01, 0.10, 0.05, 0.01)

    tests = []

    # H1: Physical Activity
    if 'PhysicalActivities' in df_filtered.columns:
        active = df_filtered[df_filtered['PhysicalActivities'] == 1]['HadHeartAttack']
        inactive = df_filtered[df_filtered['PhysicalActivities'] == 0]['HadHeartAttack']
        ct = [[active.sum(), (active == 0).sum()],
              [inactive.sum(), (inactive == 0).sum()]]
        chi2, p1, _, _ = scipy_stats.chi2_contingency(ct)
        tests.append({
            'Hipotesis': 'H1: Aktivitas Fisik vs HadHeartAttack',
            'Uji': 'Chi-Square',
            'p-value': round(p1, 6),
            'Signifikan': 'Ya' if p1 < alpha else 'Tidak',
            'Grup A': f'Aktif: {active.mean()*100:.2f}%',
            'Grup B': f'Tidak Aktif: {inactive.mean()*100:.2f}%'
        })

    # H2: BMI
    if 'BMI' in df_filtered.columns:
        bmi_yes = df_filtered[df_filtered['HadHeartAttack'] == 1]['BMI'].dropna()
        bmi_no  = df_filtered[df_filtered['HadHeartAttack'] == 0]['BMI'].dropna()
        t2, p2 = scipy_stats.ttest_ind(bmi_yes, bmi_no)
        tests.append({
            'Hipotesis': 'H2: BMI vs HadHeartAttack',
            'Uji': 'T-Test',
            'p-value': round(p2, 6),
            'Signifikan': 'Ya' if p2 < alpha else 'Tidak',
            'Grup A': f'HadHeartAttack=Yes: {bmi_yes.mean():.2f}',
            'Grup B': f'HadHeartAttack=No: {bmi_no.mean():.2f}'
        })

    # H3: Smoker Status
    if 'IsActiveSmoker' in df_filtered.columns:
        smoker = df_filtered[df_filtered['IsActiveSmoker'] == 1]['HadHeartAttack']
        nonsmoker = df_filtered[df_filtered['IsActiveSmoker'] == 0]['HadHeartAttack']
        ct3 = [[smoker.sum(), (smoker == 0).sum()],
               [nonsmoker.sum(), (nonsmoker == 0).sum()]]
        chi3, p3, _, _ = scipy_stats.chi2_contingency(ct3)
        tests.append({
            'Hipotesis': 'H3: Status Merokok vs HadHeartAttack',
            'Uji': 'Chi-Square',
            'p-value': round(p3, 6),
            'Signifikan': 'Ya' if p3 < alpha else 'Tidak',
            'Grup A': f'Perokok Aktif: {smoker.mean()*100:.2f}%',
            'Grup B': f'Non-Perokok: {nonsmoker.mean()*100:.2f}%'
        })

    # H4: Sleep Hours
    if 'SleepHours' in df_filtered.columns:
        sleep_yes = df_filtered[df_filtered['HadHeartAttack'] == 1]['SleepHours'].dropna()
        sleep_no  = df_filtered[df_filtered['HadHeartAttack'] == 0]['SleepHours'].dropna()
        t4, p4 = scipy_stats.ttest_ind(sleep_yes, sleep_no)
        tests.append({
            'Hipotesis': 'H4: Jam Tidur vs HadHeartAttack',
            'Uji': 'T-Test',
            'p-value': round(p4, 6),
            'Signifikan': 'Ya' if p4 < alpha else 'Tidak',
            'Grup A': f'HadHeartAttack=Yes: {sleep_yes.mean():.2f} jam',
            'Grup B': f'HadHeartAttack=No: {sleep_no.mean():.2f} jam'
        })

    if tests:
        test_df = pd.DataFrame(tests)

        def color_sig(val):
            if val == 'Ya':
                return 'background-color: #fadbd8; color: #e74c3c; font-weight: bold'
            return 'background-color: #d5f5e3; color: #1e8449'

        st.dataframe(
            test_df.style.applymap(color_sig, subset=['Signifikan']),
            use_container_width=True
        )

        sig_count = sum(1 for t in tests if t['Signifikan'] == 'Ya')
        st.info(
            f"**{sig_count}/{len(tests)} hipotesis terbukti signifikan** pada α={alpha}. "
            "Faktor-faktor ini memiliki perbedaan statistik yang nyata antar kelompok."
        )

    st.markdown("---")
    st.subheader("Visualisasi Detail Per Hipotesis")
    if tests:
        chosen_h = st.selectbox("Pilih Hipotesis", [t['Hipotesis'] for t in tests])

        if 'H1' in chosen_h and 'PhysicalActivities' in df_filtered.columns:
            active = df_filtered[df_filtered['PhysicalActivities'] == 1]
            inactive = df_filtered[df_filtered['PhysicalActivities'] == 0]
            fig = go.Figure()
            fig.add_trace(go.Bar(name='Aktif', x=['% Serangan Jantung'],
                                 y=[active['HadHeartAttack'].mean() * 100],
                                 marker_color=SAFE_COLOR))
            fig.add_trace(go.Bar(name='Tidak Aktif', x=['% Serangan Jantung'],
                                 y=[inactive['HadHeartAttack'].mean() * 100],
                                 marker_color=RISK_COLOR))
            fig.update_layout(title='H1: Proporsi Serangan Jantung - Aktif vs Tidak Aktif',
                               yaxis_title='% HadHeartAttack = Yes', barmode='group')
            st.plotly_chart(fig, use_container_width=True)

        elif 'H2' in chosen_h and 'BMI' in df_filtered.columns:
            bmi_data = pd.DataFrame({
                'BMI': pd.concat([
                    df_filtered[df_filtered['HadHeartAttack'] == 0]['BMI'],
                    df_filtered[df_filtered['HadHeartAttack'] == 1]['BMI']
                ]),
                'Grup': ['No'] * (df_filtered['HadHeartAttack'] == 0).sum() +
                        ['Yes'] * (df_filtered['HadHeartAttack'] == 1).sum()
            })
            fig = px.box(bmi_data, x='Grup', y='BMI', color='Grup',
                         color_discrete_map={'No': SAFE_COLOR, 'Yes': RISK_COLOR},
                         title='H2: Distribusi BMI per Kelompok HadHeartAttack')
            st.plotly_chart(fig, use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────
st.markdown("---")
st.caption(
    "Pulsevera Dashboard | CC26-PRU439 | Coding Camp 2026 powered by DBS Foundation | "
    "Data: CDC BRFSS 2022"
)
