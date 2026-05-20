import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
from datetime import datetime

st.set_page_config(
    page_title="EcoMonitor Dashboard",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
    }
    .metric-card {
        background: #21262d;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #58a6ff;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #8b949e;
        margin-top: 0.3rem;
    }
    h1 { color: #58a6ff !important; }
    h2, h3 { color: #c9d1d9 !important; }
""", unsafe_allow_html=True)

CSV_FILE = 'misure.csv'

@st.cache_data(ttl=10)
def carica_dati():
    if not os.path.exists(CSV_FILE):
        return pd.DataFrame(columns=['studente', 'sensore', 'valore', 'luogo', 'data_ora'])
    df = pd.read_csv(CSV_FILE)
    df['valore'] = pd.to_numeric(df['valore'], errors='coerce')
    df['data_ora'] = pd.to_datetime(df['data_ora'], errors='coerce')
    
    # 🔥 MODIFICA SOLO QUI: CO2 → LUCE
    df['sensore'] = df['sensore'].replace('CO2', 'Luce')
    
    return df.dropna(subset=['valore'])

st.title("🌿 EcoMonitor Dashboard")
st.caption("Sistema di monitoraggio ambientale — Classe 4E ITIS Informatica")

df_originale = carica_dati()

with st.sidebar:
    st.image("https://img.shields.io/badge/EcoMonitor-v2.0-green", use_column_width=False)
    st.markdown("---")
    st.subheader("🔍 Filtri")

    sensori_disponibili = ['Tutti'] + sorted(df_originale['sensore'].unique().tolist()) if not df_originale.empty else ['Tutti']
    sensore_sel = st.selectbox("Sensore", sensori_disponibili)

    luoghi_disponibili = ['Tutti'] + sorted(df_originale['luogo'].unique().tolist()) if not df_originale.empty else ['Tutti']
    luogo_sel = st.selectbox("Luogo", luoghi_disponibili)

    studenti_disponibili = ['Tutti'] + sorted(df_originale['studente'].unique().tolist()) if not df_originale.empty else ['Tutti']
    studente_sel = st.selectbox("Studente", studenti_disponibili)

    st.markdown("---")
    if st.button("🔄 Aggiorna dati"):
        st.cache_data.clear()
        st.rerun()
    st.caption(f"Ultimo aggiornamento: {datetime.now().strftime('%H:%M:%S')}")

df = df_originale.copy()
if sensore_sel != 'Tutti':
    df = df[df['sensore'] == sensore_sel]
if luogo_sel != 'Tutti':
    df = df[df['luogo'] == luogo_sel]
if studente_sel != 'Tutti':
    df = df[df['studente'] == studente_sel]

st.markdown("### 📊 Riepilogo generale")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-value">{len(df)}</div>
        <div class="metric-label">Misure totali</div>
    </div>""", unsafe_allow_html=True)

with col2:
    media = df['valore'].mean() if not df.empty else 0
    st.markdown(f"""<div class="metric-card">
        <div class="metric-value">{media:.2f}</div>
        <div class="metric-label">Valore medio</div>
    </div>""", unsafe_allow_html=True)

with col3:
    n_studenti = df['studente'].nunique() if not df.empty else 0
    st.markdown(f"""<div class="metric-card">
        <div class="metric-value">{n_studenti}</div>
        <div class="metric-label">Studenti attivi</div>
    </div>""", unsafe_allow_html=True)

with col4:
    n_luoghi = df['luogo'].nunique() if not df.empty else 0
    st.markdown(f"""<div class="metric-card">
        <div class="metric-value">{n_luoghi}</div>
        <div class="metric-label">Luoghi monitorati</div>
    </div>""", unsafe_allow_html=True)

st.markdown("---")

if df.empty:
    st.warning("⚠️ Nessun dato trovato con i filtri selezionati.")
else:
    col_g1, col_g2 = st.columns(2)

    with col_g1:
        st.markdown("#### 📍 Misure per luogo")
        fig, ax = plt.subplots(figsize=(7, 4))
        fig.patch.set_facecolor('#21262d')
        ax.set_facecolor('#161b22')
        media_luogo = df.groupby('luogo')['valore'].mean().sort_values(ascending=False)
        colors = ['#58a6ff', '#3fb950', '#f78166', '#d2a8ff', '#ffa657']
        bars = ax.bar(media_luogo.index, media_luogo.values,
                      color=colors[:len(media_luogo)], edgecolor='none', width=0.6)
        ax.set_ylabel('Valore medio', color='#8b949e')
        ax.tick_params(colors='#8b949e')
        ax.spines[['top', 'right', 'left', 'bottom']].set_visible(False)
        for bar, val in zip(bars, media_luogo.values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    f'{val:.1f}', ha='center', va='bottom', color='#c9d1d9', fontsize=10)
        plt.xticks(rotation=20, ha='right')
        st.pyplot(fig)
        plt.close()

    with col_g2:
        st.markdown("#### 👤 Misure per studente")
        fig, ax = plt.subplots(figsize=(7, 4))
        fig.patch.set_facecolor('#21262d')
        ax.set_facecolor('#161b22')
        count_studente = df.groupby('studente').size().sort_values(ascending=False)
        colors_s = ['#d2a8ff', '#ffa657', '#79c0ff']
        ax.barh(count_studente.index, count_studente.values,
                color=colors_s[:len(count_studente)], edgecolor='none', height=0.5)
        ax.set_xlabel('Numero di misure', color='#8b949e')
        ax.tick_params(colors='#8b949e')
        ax.spines[['top', 'right', 'left', 'bottom']].set_visible(False)
        for i, (idx, val) in enumerate(count_studente.items()):
            ax.text(val + 0.1, i, str(val), va='center', color='#c9d1d9', fontsize=10)
        st.pyplot(fig)
        plt.close()

    st.markdown("---")

    col_g3, col_g4 = st.columns(2)

    with col_g3:
        st.markdown("#### 🔬 Media per sensore")
        fig, ax = plt.subplots(figsize=(7, 4))
        fig.patch.set_facecolor('#21262d')
        ax.set_facecolor('#161b22')
        media_sensore = df.groupby('sensore')['valore'].mean()
        wedge_colors = ['#58a6ff', '#3fb950', '#ffa657', '#f78166']
        wedges, texts, autotexts = ax.pie(
            media_sensore.values,
            labels=media_sensore.index,
            autopct='%1.1f%%',
            colors=wedge_colors[:len(media_sensore)],
            startangle=90,
            textprops={'color': '#c9d1d9'}
        )
        for autotext in autotexts:
            autotext.set_color('#0d1117')
            autotext.set_fontweight('bold')
        st.pyplot(fig)
        plt.close()

    with col_g4:
        st.markdown("#### 🏆 Classifica luoghi per valore")
        fig, ax = plt.subplots(figsize=(7, 4))
        fig.patch.set_facecolor('#21262d')
        ax.set_facecolor('#161b22')

        if sensore_sel == 'Tutti' and df['sensore'].nunique() > 1:
            for i, sensore in enumerate(df['sensore'].unique()):
                df_s = df[df['sensore'] == sensore]
                media_l = df_s.groupby('luogo')['valore'].mean().sort_values(ascending=False)
                ax.plot(media_l.index, media_l.values, marker='o',
                        label=sensore, color=colors[i], linewidth=2)
            ax.legend(facecolor='#21262d', edgecolor='#30363d', labelcolor='#c9d1d9')
        else:
            media_l = df.groupby('luogo')['valore'].mean().sort_values(ascending=False)
            ax.plot(media_l.index, media_l.values, marker='o',
                    color='#58a6ff', linewidth=2, markersize=8)
            for x, y in zip(range(len(media_l)), media_l.values):
                ax.text(x, y + 0.5, f'{y:.1f}', ha='center', color='#c9d1d9', fontsize=10)

        ax.set_ylabel('Valore medio', color='#8b949e')
        ax.tick_params(colors='#8b949e')
        ax.spines[['top', 'right', 'left', 'bottom']].set_visible(False)
        plt.xticks(rotation=20, ha='right')
        st.pyplot(fig)
        plt.close()

    st.markdown("---")
    st.markdown("### 📋 Statistiche per sensore")
    stats = df.groupby('sensore')['valore'].agg(['mean', 'min', 'max', 'count'])
    stats.columns = ['Media', 'Minimo', 'Massimo', 'Misure']
    stats = stats.round(3)
    st.dataframe(stats, use_container_width=True)

    st.markdown("---")
    st.markdown("### 📄 Tabella completa dei dati")
    df_display = df.copy()
    df_display['data_ora'] = df_display['data_ora'].dt.strftime('%Y-%m-%d %H:%M:%S')
    st.dataframe(df_display, use_container_width=True, height=300)

    csv_export = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Scarica dati filtrati (CSV)",
        data=csv_export,
        file_name="misure_filtrate.csv",
        mime="text/csv"
    )

st.markdown("---")
st.caption("EcoMonitor v2.0 — Gruppo: Awan Ali Atta, Singh Gurtjpreet, Cristiano Sofia — Classe 4E ITIS Informatica")
