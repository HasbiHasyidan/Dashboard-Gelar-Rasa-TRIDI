import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import warnings
from datetime import datetime

warnings.filterwarnings('ignore', category=UserWarning, module='streamlit')

st.set_page_config(
    page_title="Gen Z Financial Dashboard Indonesia",
    page_icon="🇮🇩",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        font-size: 2.8rem !important;
        color: #1a365d;
        margin-bottom: 0.5rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(135deg, #1a365d 0%, #2d3748 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        padding: 1rem;
        border-radius: 16px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        border: 2px solid #e2e8f0;
    }
    .sub-header {
        font-size: 1.3rem !important;
        color: #4a5568;
        margin-bottom: 2rem;
        font-weight: 400;
        text-align: center;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
        padding: 1.5rem;
        border-radius: 16px;
        height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-align: left;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        border-left: 5px solid #4299e1;
        color: white;
        margin-bottom: 1rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.2);
    }
    .metric-card-label {
        color: #cbd5e0;
        font-size: 0.85rem;
        margin: 0;
        line-height: 1.3;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-card-value {
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0.3rem 0;
        line-height: 1.2;
        color: #ffffff;
    }
    .metric-card-delta {
        font-size: 0.75rem;
        color: #e2e8f0;
        margin: 0;
        font-weight: 400;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 0px;
        background-color: #ffffff;
        padding: 6px;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
        margin-bottom: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 12px;
        padding: 14px 24px;
        font-weight: 600;
        color: #4a5568;
        transition: all 0.3s ease;
        border: none;
        margin: 0 2px;
        font-size: 0.95rem;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #edf2f7;
        color: #2d3748;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
        color: white;
        box-shadow: 0 4px 12px rgba(66, 153, 225, 0.3);
        transform: translateY(-2px);
    }
    
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: transparent;
    }
    
    .insight-box {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        padding: 1.8rem;
        border-radius: 16px;
        border-left: 6px solid #2f855a;
        margin: 1.5rem 0;
        color: white;
        box-shadow: 0 8px 20px rgba(72, 187, 120, 0.25);
    }
    .warning-box {
        background: linear-gradient(135deg, #ed8936 0%, #dd6b20 100%);
        padding: 1.8rem;
        border-radius: 16px;
        border-left: 6px solid #c05621;
        margin: 1.5rem 0;
        color: white;
        box-shadow: 0 8px 20px rgba(237, 137, 54, 0.25);
    }
    .analysis-box {
        background: linear-gradient(135deg, #ffffff 0%, #f7fafc 100%);
        padding: 1.8rem;
        border-radius: 16px;
        border: 2px solid #e2e8f0;
        margin: 1.5rem 0;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
        color: #2d3748;
    }
    
    .chart-header {
        font-size: 1.3rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #4299e1;
        display: inline-block;
        background: rgba(66, 153, 225, 0.1);
        padding: 0.8rem 1.5rem;
        border-radius: 10px;
    }
    
    :root {
        --primary-color: #4299e1;
        --secondary-color: #48bb78;
        --warning-color: #ed8936;
        --accent-color: #9f7aea;
        --dark-color: #2d3748;
    }
</style>
""", unsafe_allow_html=True)

def get_survey_column_map(df_survey):
    try:
        if df_survey.shape[1] < 57:
            st.error("Data Survei tidak memiliki kolom sebanyak yang diharapkan untuk Likert Scale.")
            return []
            
        long_cols = df_survey.columns[9:57].tolist()
    except IndexError:
        st.error("Data Survei tidak memiliki kolom sebanyak yang diharapkan untuk Likert Scale.")
        return []

    short_titles = {
        long_cols[0]: "Lit 1: Identifikasi Risiko", long_cols[1]: "Lit 2: Investasi yang Baik", long_cols[2]: "Lit 3: Pemahaman Angka", long_cols[3]: "Lit 4: Alokasi Dana", long_cols[4]: "Lit 5: Proyeksi Kas", long_cols[5]: "Lit 6: Hindari Belanja Impulsif", long_cols[6]: "Lit 7: Metrik Keuangan", long_cols[7]: "Lit 8: Cash Flow & Profit", long_cols[8]: "Lit 9: Laporan Keuangan",
        long_cols[9]: "FT 1: Risiko Fintech", long_cols[10]: "FT 2: Penggunaan Digital Payment", long_cols[11]: "FT 3: Penggunaan Pinjaman", long_cols[12]: "FT 4: Asset Management", long_cols[13]: "FT 5: Produk Digital Payment", long_cols[14]: "FT 6: Digital Asset Management", long_cols[15]: "FT 7: Alternatif Digital", long_cols[16]: "FT 8: Asuransi Digital", long_cols[17]: "FT 9: Hak Konsumen",
        long_cols[18]: "Beh 1: Perencanaan Biaya RT", long_cols[19]: "Beh 2: Kritik Pengelolaan Uang", long_cols[20]: "Beh 3: Keputusan Beli Keluarga", long_cols[21]: "Beh 4: Saran Keuangan", long_cols[22]: "Beh 5: Menabung untuk Keinginan", long_cols[23]: "Beh 6: Negosiasi Harga", long_cols[24]: "Beh 7: Dana Darurat", long_cols[25]: "Beh 8: Promo & Diskon", long_cols[26]: "Beh 9: Berpikir Sebelum Beli", long_cols[27]: "Beh 10: Perbandingan Harga", long_cols[28]: "Beh 11: Berita Ekonomi",
        long_cols[29]: "DM 1: Bertindak Tanpa Pikir", long_cols[30]: "DM 2: Impulsif", long_cols[31]: "DM 3: Bicara Sebelum Pikir", long_cols[32]: "DM 4: Ubah Keputusan Cepat", long_cols[33]: "DM 5: Penilaian Risiko", long_cols[34]: "DM 6: Bandingkan Hasil", long_cols[35]: "DM 7: Bandingkan Biaya", long_cols[36]: "DM 8: Cari Opsi Ekonomis", long_cols[37]: "DM 9: Perkirakan Konsekuensi", long_cols[38]: "DM 10: Strategi Keputusan",
        long_cols[39]: "Well 1: Aman Finansial", long_cols[40]: "Well 2: Masa Depan Finansial", long_cols[41]: "Well 3: Capai Tujuan Finansial", long_cols[42]: "Well 4: Tabungan Cukup", long_cols[43]: "Well 5: Tidak Dapat yang Diinginkan", long_cols[44]: "Well 6: Tertinggal Finansial", long_cols[45]: "Well 7: Keuangan Mengendalikan", long_cols[46]: "Well 8: Kontrol Gagal", long_cols[47]: "Well 9: Tidak Nikmati Hidup",
    }
        
    df_survey.rename(columns=short_titles, inplace=True)
        
    literasi_cols = [col for col in df_survey.columns if col.startswith('Lit ')]
    
    perilaku_pos_cols = [col for col in df_survey.columns if col.startswith('Beh ')] + [col for col in df_survey.columns if col.startswith('DM ') and 'DM 1' not in col and 'DM 2' not in col and 'DM 3' not in col]
    perilaku_neg_cols = ['DM 1: Bertindak Tanpa Pikir', 'DM 2: Impulsif', 'DM 3: Bicara Sebelum Pikir']
    
    kesejahteraan_pos_cols = [col for col in df_survey.columns if col.startswith('Well ') and 'Well 5' not in col and 'Well 6' not in col and 'Well 7' not in col and 'Well 8' not in col and 'Well 9' not in col]
    kesejahteraan_neg_cols = ['Well 5: Tidak Dapat yang Diinginkan', 'Well 6: Tertinggal Finansial', 'Well 7: Keuangan Mengendalikan', 'Well 8: Kontrol Gagal', 'Well 9: Tidak Nikmati Hidup']

    neg_cols_to_invert = perilaku_neg_cols + kesejahteraan_neg_cols
    df_survey[neg_cols_to_invert] = 5 - df_survey[neg_cols_to_invert]
        
    df_survey['Composite_Literasi'] = df_survey[literasi_cols].mean(axis=1)
    df_survey['Composite_Perilaku_DM'] = df_survey[perilaku_pos_cols + [col for col in perilaku_neg_cols]].mean(axis=1)
    df_survey['Composite_Kesejahteraan'] = df_survey[kesejahteraan_pos_cols + [col for col in kesejahteraan_neg_cols]].mean(axis=1)
        
    renamed_likert_cols = list(short_titles.values())
        
    return renamed_likert_cols

def income_to_numeric(income_str):
    if pd.isna(income_str): return np.nan
    income_str_clean = str(income_str).replace(' – ', ' - ').strip()
    income_str_clean = income_str_clean.replace('Rp', '').replace('.', '').strip()
    mapping = {
        '< 2000000': 1500000,
        '2000001 - 4000000': 3000000,
        '4000001 - 6000000': 5000000,
        '6000001 - 10000000': 8000000,
        '10000001 - 15000000': 12500000,
        '> 15000000': 17500000
    }
    return mapping.get(income_str_clean, np.nan)

@st.cache_data
def load_data():
    try:
        df_genz = pd.read_excel("Cleaning GenZ Financial Profile.xlsx")
        df_regional = pd.read_excel("Regional_Economic_Indicators.xlsx")
        df_survey = pd.read_excel("survey_final_aman.xlsx")
    except Exception as e:
        st.error(f"Gagal memuat data. Pastikan file ada dan dalam format yang benar: {e}")
        return None, None, None

    df_genz.rename(columns={'user_id ID': 'user_id'}, inplace=True)
    current_year = datetime.now().year
    df_genz['Age'] = current_year - df_genz['birth_year']

    df_genz['avg_monthly_income_num'] = df_genz['avg_monthly_income'].apply(income_to_numeric)
    df_genz['avg_monthly_expense_num'] = df_genz['avg_monthly_expense'].apply(income_to_numeric)
    df_genz['net_financial_standing'] = df_genz['avg_monthly_income_num'] - df_genz['avg_monthly_expense_num']
    
    df_genz['saving_rate_proxy'] = np.where(
        df_genz['avg_monthly_income_num'] > 0, 
        (df_genz['net_financial_standing'] / df_genz['avg_monthly_income_num']), 
        np.nan
    )
    
    df_genz['is_investor'] = df_genz['investment_type'] != 'Tidak Ada'
    df_genz['has_loan'] = df_genz['outstanding_loan'] > 0
    
    df_genz['Provinsi_clean'] = df_genz['province'].str.strip()
    df_regional.rename(columns={'Provinsi': 'Provinsi_clean'}, inplace=True)
    df_regional['Provinsi_clean'] = df_regional['Provinsi_clean'].str.strip()
    
    df_merged = pd.merge(df_genz, df_regional, on='Provinsi_clean', how='left')

    df_survey.rename(columns={
        'Province of Origin': 'province', 
        'Last Education': 'education_level', 
        'Job': 'employment_status',
        'Est. Monthly Income': 'avg_monthly_income',
        'Est. Monthly Expenditure': 'avg_monthly_expense',
        'Gender': 'gender',
        'Year of Birth': 'birth_year',
        'Marital Status': 'marital_status'
    }, inplace=True)
        
    get_survey_column_map(df_survey)
        
    df_survey['province'] = df_survey['province'].str.strip()
        
    return df_merged, df_survey, df_regional

df_merged, df_survey, df_regional = load_data()

primary_color = "#4299e1"
secondary_color = "#48bb78"
warning_color = "#ed8936"
accent_color = "#9f7aea"
dark_color = "#2d3748"

st.markdown('<p class="main-header">Dashboard Profil Keuangan Generasi Z Indonesia</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Analisis Mendalam Pola, Perilaku, dan Dinamika Keuangan Generasi Muda Indonesia | Gelar Rasa 2025</p>', unsafe_allow_html=True)

if df_merged is not None and df_survey is not None:
    
    st.markdown("### 🔍 Filter Data")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        filter_options = ['Semua Data']
        available_filters = []
        
        if 'employment_status' in df_merged.columns:
            available_filters.append('Status Pekerjaan')
        if 'education_level' in df_merged.columns:
            available_filters.append('Tingkat Pendidikan')
        if 'gender' in df_merged.columns:
            available_filters.append('Jenis Kelamin')
        if 'marital_status' in df_merged.columns:
            available_filters.append('Status Pernikahan')
        
        filter_options.extend(available_filters)
        
        filter_type = st.selectbox(
            "Filter Berdasarkan:",
            filter_options,
            key="filter_type"
        )
    
    filter_col = None
    if filter_type == 'Status Pekerjaan' and 'employment_status' in df_merged.columns:
        filter_col = 'employment_status'
    elif filter_type == 'Tingkat Pendidikan' and 'education_level' in df_merged.columns:
        filter_col = 'education_level'
    elif filter_type == 'Jenis Kelamin' and 'gender' in df_merged.columns:
        filter_col = 'gender'
    elif filter_type == 'Status Pernikahan' and 'marital_status' in df_merged.columns:
        filter_col = 'marital_status'
    
    with col2:
        if filter_col and filter_col in df_merged.columns:
            try:
                list_options = ['Semua'] + sorted(df_merged[filter_col].dropna().unique().tolist())
                selected_value = st.selectbox(f"Pilih {filter_type}:", list_options, index=0, key="filter_value")
            except Exception as e:
                st.error(f"Error dalam memuat filter: {e}")
                selected_value = 'Semua'
        else:
            selected_value = 'Semua Responden'
    
    df_genz_filtered = df_merged.copy()
    df_survey_filtered = df_survey.copy()
    
    if selected_value != 'Semua' and filter_col and filter_col in df_merged.columns:
        try:
            df_genz_filtered = df_merged[df_merged[filter_col] == selected_value].copy()
            if filter_col in df_survey.columns:
                df_survey_filtered = df_survey[df_survey[filter_col] == selected_value].copy()
        except Exception as e:
            st.error(f"Error dalam menerapkan filter: {e}")
    
    with col3:
        st.markdown("###")
        if selected_value != 'Semua Responden':
            st.markdown(f"**Filter Aktif:** {filter_type} = **{selected_value}**")
            st.markdown(f"**Jumlah Data:** {len(df_genz_filtered):,} responden")
    
    st.markdown("---")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Data Summary",
        "👥 Demografi & Finansial", 
        "💡 Perilaku & Literasi",
        "🗺️ Regional & Analisis",
        "📋 Metadata & Metodologi"
    ])

    with tab1:
        st.header("📊 Summary Berdasarkan Data")
        
        total_respondents = df_genz_filtered.shape[0]
        
        avg_anxiety = df_genz_filtered['financial_anxiety_score'].mean() if 'financial_anxiety_score' in df_genz_filtered.columns else 0
        avg_net = df_genz_filtered['net_financial_standing'].mean() if 'net_financial_standing' in df_genz_filtered.columns else 0
        avg_saving_rate = df_genz_filtered['saving_rate_proxy'].mean() * 100 if 'saving_rate_proxy' in df_genz_filtered.columns else 0
        pct_investor = (df_genz_filtered['is_investor'].sum() / total_respondents) * 100 if 'is_investor' in df_genz_filtered.columns else 0
        pct_loan = (df_genz_filtered['has_loan'].sum() / total_respondents) * 100 if 'has_loan' in df_genz_filtered.columns else 0
        
        if len(df_survey_filtered) > 0 and all(col in df_survey_filtered.columns for col in ['Composite_Literasi', 'Composite_Perilaku_DM', 'Composite_Kesejahteraan']):
            avg_composite = df_survey_filtered[['Composite_Literasi', 'Composite_Perilaku_DM', 'Composite_Kesejahteraan']].mean().mean()
        else:
            avg_composite = np.nan
        
        col1, col2, col3 = st.columns(3)
        col4, col5, col6 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <p class="metric-card-label">Total Responden</p>
                <p class="metric-card-value">{total_respondents:,}</p>
                <p class="metric-card-delta">Jumlah data yang dianalisis</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-card" style="border-left: 5px solid {secondary_color};">
                <p class="metric-card-label">Rata-rata Saving Rate</p>
                <p class="metric-card-value">{avg_saving_rate:.1f}%</p>
                <p class="metric-card-delta">Proporsi pendapatan tersisa</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            anxiety_trend = "↑ Tinggi" if avg_anxiety > 3 else "↓ Rendah" if avg_anxiety < 2.5 else "→ Sedang"
            st.markdown(f"""
            <div class="metric-card" style="border-left: 5px solid {warning_color};">
                <p class="metric-card-label">Kecemasan Finansial</p>
                <p class="metric-card-value">{avg_anxiety:.2f}/5.0</p>
                <p class="metric-card-delta">{anxiety_trend}</p>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="metric-card" style="border-left: 5px solid {accent_color};">
                <p class="metric-card-label">% Investor Aktif</p>
                <p class="metric-card-value">{pct_investor:.1f}%</p>
                <p class="metric-card-delta">Memiliki jenis investasi</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col5:
            st.markdown(f"""
            <div class="metric-card" style="border-left: 5px solid #e53e3e;">
                <p class="metric-card-label">% Memiliki Pinjaman</p>
                <p class="metric-card-value">{pct_loan:.1f}%</p>
                <p class="metric-card-delta">Memiliki outstanding loan</p>
            </div>
            """, unsafe_allow_html=True)

        with col6:
            score_display = f"{avg_composite:.2f}/4.0" if not np.isnan(avg_composite) else "N/A"
            st.markdown(f"""
            <div class="metric-card" style="border-left: 5px solid {dark_color};">
                <p class="metric-card-label">Skor Komposit Finansial</p>
                <p class="metric-card-value">{score_display}</p>
                <p class="metric-card-delta">Literasi, Perilaku & Kesejahteraan</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown('<p class="chart-header">📈 Distribusi Posisi Finansial Bersih</p>', unsafe_allow_html=True)
            
            if 'net_financial_standing' in df_genz_filtered.columns:
                hist_chart = alt.Chart(df_genz_filtered).mark_bar(
                    cornerRadiusTopLeft=3,
                    cornerRadiusTopRight=3
                ).encode(
                    x=alt.X('net_financial_standing:Q', bin=alt.Bin(maxbins=25), 
                           title='Posisi Finansial Bersih (Rp)', 
                           axis=alt.Axis(format='~s', labelAngle=0)),
                    y=alt.Y('count():Q', title='Jumlah Responden'),
                    color=alt.condition(
                        alt.datum.net_financial_standing > 0,
                        alt.value(secondary_color),
                        alt.value(warning_color)
                    ),
                    tooltip=[alt.Tooltip('net_financial_standing', bin=True, title='Rentang Finansial'), 'count()']
                ).properties(height=400)
                
                avg_line = alt.Chart(pd.DataFrame({'x': [avg_net]})).mark_rule(
                    color='red',
                    strokeWidth=2,
                    strokeDash=[5, 5]
                ).encode(x='x:Q')
                
                st.altair_chart(hist_chart + avg_line, use_container_width=True)
            else:
                st.info("Data posisi finansial tidak tersedia")
            
        with col_right:
            st.markdown('<p class="chart-header">🎯 Skor Komposit Rata-rata</p>', unsafe_allow_html=True)
            
            if not np.isnan(avg_composite) and all(col in df_survey_filtered.columns for col in ['Composite_Literasi', 'Composite_Perilaku_DM', 'Composite_Kesejahteraan']):
                composite_means = df_survey_filtered[['Composite_Literasi', 'Composite_Perilaku_DM', 'Composite_Kesejahteraan']].mean().reset_index()
                composite_means.columns = ['Dimensi', 'Skor_Rata_rata']
                composite_means['Dimensi'] = composite_means['Dimensi'].replace({
                    'Composite_Literasi': 'Literasi',
                    'Composite_Perilaku_DM': 'Perilaku',
                    'Composite_Kesejahteraan': 'Kesejahteraan'
                })
                
                composite_chart = alt.Chart(composite_means).mark_bar(
                    cornerRadiusTopLeft=5,
                    cornerRadiusTopRight=5
                ).encode(
                    x=alt.X('Dimensi:N', title='Dimensi Finansial', axis=alt.Axis(labelAngle=0)),
                    y=alt.Y('Skor_Rata_rata:Q', title='Skor Rata-rata (1-4)', scale=alt.Scale(domain=[0, 4])),
                    color=alt.Color('Dimensi:N', 
                                  scale=alt.Scale(domain=['Literasi', 'Perilaku', 'Kesejahteraan'],
                                                range=[primary_color, secondary_color, accent_color]),
                                  legend=None),
                    tooltip=['Dimensi', alt.Tooltip('Skor_Rata_rata', format='.2f')]
                ).properties(height=400)
                
                st.altair_chart(composite_chart, use_container_width=True)
            else:
                st.info("Tidak ada data survei yang tersedia untuk kelompok ini.")
        
        if 'net_financial_standing' in df_genz_filtered.columns:
            positive_count = len(df_genz_filtered[df_genz_filtered['net_financial_standing'] > 0])
            positive_pct = (positive_count / len(df_genz_filtered)) * 100 if len(df_genz_filtered) > 0 else 0
            deficit_count = len(df_genz_filtered[df_genz_filtered['net_financial_standing'] < 0])
            deficit_pct = (deficit_count / len(df_genz_filtered)) * 100 if len(df_genz_filtered) > 0 else 0
        else:
            positive_pct = 0
            deficit_pct = 0
        
        insight_text = f"""
        <strong>💡 Insight berdasarkan data:</strong><br><br>
        • <strong>{positive_pct:.1f}%</strong> responden memiliki <strong>Surplus Finansial</strong> - peluang investasi<br>
        • <strong>{deficit_pct:.1f}%</strong> responden mengalami <strong>Defisit</strong> - butuh edukasi keuangan<br>
        • Saving Rate <strong>{avg_saving_rate:.1f}%</strong> menunjukkan ruang untuk optimalisasi<br>
        • <strong>{pct_investor:.1f}%</strong> sudah berinvestasi - tren positif Gen Z<br>
        • Kecemasan finansial <strong>{anxiety_trend}</strong> perlu penanganan khusus
        """
        st.markdown(f'<div class="insight-box">{insight_text}</div>', unsafe_allow_html=True)

    with tab2:
        st.header("👥 Demografi & Keseimbangan Finansial")
        
        st.markdown("""
        <div class="analysis-box">
        <strong>🎯 Mengenal Lebih Dekat Gen Z Indonesia:</strong><br>
        Tab ini mengungkap profil demografi dan kesehatan finansial Generasi Z Indonesia melalui analisis mendalam 
        pendapatan, pengeluaran, dan pola keuangan mereka.
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<p class="chart-header">👥 Profil Demografi Responden</p>', unsafe_allow_html=True)
            
            if 'gender' in df_genz_filtered.columns:
                gender_data = df_genz_filtered['gender'].value_counts().reset_index()
                gender_data.columns = ['Jenis Kelamin', 'Jumlah']
                
                gender_chart = alt.Chart(gender_data).mark_arc(innerRadius=50, outerRadius=120).encode(
                    theta=alt.Theta(field="Jumlah", type="quantitative"),
                    color=alt.Color(field="Jenis Kelamin", type="nominal",
                                    scale=alt.Scale(range=[primary_color, secondary_color, accent_color, warning_color]),
                                    legend=alt.Legend(title="Jenis Kelamin", orient='bottom')),
                    tooltip=['Jenis Kelamin', 'Jumlah']
                ).properties(height=300, title="Komposisi Gender Responden")
                
                st.altair_chart(gender_chart, use_container_width=True)
            else:
                st.info("Data gender tidak tersedia")
            
            if 'education_level' in df_genz_filtered.columns:
                edu_data = df_genz_filtered['education_level'].value_counts().reset_index()
                edu_data.columns = ['Tingkat Pendidikan', 'Jumlah']
                
                edu_chart = alt.Chart(edu_data).mark_bar(
                    cornerRadiusTopLeft=5,
                    cornerRadiusTopRight=5
                ).encode(
                    x=alt.X('Jumlah:Q', title='Jumlah Responden'),
                    y=alt.Y('Tingkat Pendidikan:N', sort='-x', title=''),
                    color=alt.value(primary_color),
                    tooltip=['Tingkat Pendidikan', 'Jumlah']
                ).properties(height=300, title="Distribusi Tingkat Pendidikan")
                
                st.altair_chart(edu_chart, use_container_width=True)
            else:
                st.info("Data tingkat pendidikan tidak tersedia")
        
        with col2:
            st.markdown('<p class="chart-header">💰 Analisis Kesehatan Finansial</p>', unsafe_allow_html=True)
            
            if all(col in df_genz_filtered.columns for col in ['avg_monthly_income_num', 'avg_monthly_expense_num', 'net_financial_standing']):
                df_bubble = df_genz_filtered.dropna(subset=['avg_monthly_income_num', 'avg_monthly_expense_num']).copy()
                df_bubble['status_keuangan'] = np.where(
                    df_bubble['net_financial_standing'] > 0, 'Surplus', 
                    np.where(df_bubble['net_financial_standing'] == 0, 'Seimbang', 'Defisit')
                )
                
                bubble_chart = alt.Chart(df_bubble).mark_circle(size=60, opacity=0.7).encode(
                    x=alt.X('avg_monthly_income_num:Q', 
                           title='Pendapatan Bulanan (Rp)', 
                           axis=alt.Axis(format='~s'),
                           scale=alt.Scale(domain=[0, df_bubble['avg_monthly_income_num'].max() * 1.1])),
                    y=alt.Y('avg_monthly_expense_num:Q', 
                           title='Pengeluaran Bulanan (Rp)', 
                           axis=alt.Axis(format='~s'),
                           scale=alt.Scale(domain=[0, df_bubble['avg_monthly_expense_num'].max() * 1.1])),
                    color=alt.Color('status_keuangan:N', 
                                  scale=alt.Scale(domain=['Surplus', 'Seimbang', 'Defisit'],
                                                range=[secondary_color, primary_color, warning_color]),
                                  legend=alt.Legend(title="Status Keuangan")),
                    tooltip=[
                        'employment_status' if 'employment_status' in df_bubble.columns else 'gender',
                        alt.Tooltip('avg_monthly_income_num', format=',.0f', title='Pendapatan'),
                        alt.Tooltip('avg_monthly_expense_num', format=',.0f', title='Pengeluaran'),
                        alt.Tooltip('net_financial_standing', format=',.0f', title='Saldo Bersih'),
                        'status_keuangan'
                    ]
                ).properties(height=350, title='Peta Kesehatan Finansial: Pendapatan vs Pengeluaran')
                
                max_val = max(df_bubble['avg_monthly_income_num'].max(), 
                             df_bubble['avg_monthly_expense_num'].max())
                line_data = pd.DataFrame({'x': [0, max_val], 'y': [0, max_val]})
                
                line_impas = alt.Chart(line_data).mark_line(strokeDash=[5,5], color='gray', opacity=0.7).encode(
                    x='x:Q',
                    y='y:Q'
                )
                
                st.altair_chart(bubble_chart + line_impas, use_container_width=True)
                
                st.markdown("""
                **🎯 Cara Membaca Plot:**
                - **Titik Hijau**: Surplus finansial (Pendapatan > Pengeluaran)
                - **Titik Biru**: Kondisi seimbang  
                - **Titik Oranye**: Defisit finansial
                - **Garis Abu-abu**: Batas impas finansial
                """)
            else:
                st.info("Data pendapatan dan pengeluaran tidak tersedia untuk analisis ini")

        st.markdown('<p class="chart-header">💼 Analisis Posisi Finansial berdasarkan Pekerjaan</p>', unsafe_allow_html=True)
        
        if 'employment_status' in df_genz_filtered.columns and all(col in df_genz_filtered.columns for col in ['net_financial_standing', 'avg_monthly_income_num', 'avg_monthly_expense_num']):
            job_analysis = df_genz_filtered.groupby('employment_status').agg({
                'net_financial_standing': 'mean',
                'avg_monthly_income_num': 'mean',
                'avg_monthly_expense_num': 'mean',
                'user_id': 'count'
            }).reset_index()
            job_analysis.columns = ['Pekerjaan', 'Rata2_Saldo', 'Rata2_Pendapatan', 'Rata2_Pengeluaran', 'Jumlah_Responden']
            job_analysis = job_analysis.sort_values('Rata2_Pendapatan', ascending=False)
            
            job_melted = job_analysis.melt(id_vars=['Pekerjaan', 'Jumlah_Responden'], 
                                         value_vars=['Rata2_Pendapatan', 'Rata2_Pengeluaran'],
                                         var_name='Jenis', 
                                         value_name='Nilai')
            
            job_melted['Jenis'] = job_melted['Jenis'].replace({
                'Rata2_Pendapatan': 'Pendapatan',
                'Rata2_Pengeluaran': 'Pengeluaran'
            })
            
            base = alt.Chart(job_melted).encode(
                x=alt.X('Pekerjaan:N', title='Jenis Pekerjaan', axis=alt.Axis(labelAngle=-45)),
                y=alt.Y('Nilai:Q', title='Nilai (Rp)', axis=alt.Axis(format='~s')),
                color=alt.Color('Jenis:N', 
                              scale=alt.Scale(domain=['Pendapatan', 'Pengeluaran'],
                                            range=[primary_color, warning_color]),
                              legend=alt.Legend(title="Jenis")),
                tooltip=['Pekerjaan', 'Jenis', alt.Tooltip('Nilai', format=',.0f'), 'Jumlah_Responden']
            )
            
            bar_chart = base.mark_bar(opacity=0.7).properties(
                height=400,
                title='Perbandingan Rata-rata Pendapatan vs Pengeluaran per Pekerjaan'
            )
            
            st.altair_chart(bar_chart, use_container_width=True)
        else:
            st.info("Data pekerjaan tidak tersedia untuk analisis ini")

    with tab3:
        st.header("💡 Perilaku & Literasi Finansial")
        
        st.markdown("""
        <div class="analysis-box">
        <strong>🧠 Mengungkap Pola Pikir Finansial Gen Z:</strong><br>
        Eksplorasi mendalam tentang bagaimana Generasi Z mengelola uang, berinteraksi dengan teknologi finansial, 
        dan hubungan antara pengetahuan keuangan dengan kesejahteraan finansial mereka.
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<p class="chart-header">📱 Revolusi Digital: Fintech & Investasi</p>', unsafe_allow_html=True)
            
            if 'main_fintech_app' in df_genz_filtered.columns:
                fintech_data = df_genz_filtered['main_fintech_app'].value_counts().reset_index()
                fintech_data.columns = ['Aplikasi', 'Jumlah']
                
                fintech_chart = alt.Chart(fintech_data.head(8)).mark_bar(
                    cornerRadiusTopLeft=5,
                    cornerRadiusTopRight=5
                ).encode(
                    x=alt.X('Jumlah:Q', title='Jumlah Pengguna'),
                    y=alt.Y('Aplikasi:N', sort='-x', title='Aplikasi Fintech'),
                    color=alt.Color('Aplikasi:N', 
                                  scale=alt.Scale(scheme='category10'),
                                  legend=None),
                    tooltip=['Aplikasi', 'Jumlah']
                ).properties(height=300, title="Aplikasi Fintech Paling Populer di Gen Z")
                
                st.altair_chart(fintech_chart, use_container_width=True)
            else:
                st.info("Data aplikasi fintech tidak tersedia")
            
            if 'investment_type' in df_genz_filtered.columns:
                investment_data = df_genz_filtered['investment_type'].value_counts().reset_index()
                investment_data.columns = ['Jenis Investasi', 'Jumlah']
                investment_data = investment_data[investment_data['Jenis Investasi'] != 'Tidak Ada']
                
                if len(investment_data) > 0:
                    investment_chart = alt.Chart(investment_data.head(8)).mark_arc(innerRadius=50).encode(
                        theta=alt.Theta(field="Jumlah", type="quantitative"),
                        color=alt.Color(field="Jenis Investasi", type="nominal",
                                        scale=alt.Scale(scheme='set3'),
                                        legend=alt.Legend(title="Jenis Investasi", orient='bottom')),
                        tooltip=['Jenis Investasi', 'Jumlah']
                    ).properties(height=300, title="Portofolio Investasi Gen Z")
                    
                    st.altair_chart(investment_chart, use_container_width=True)
                else:
                    st.info("💡 Tren menarik: Gen Z belum banyak berinvestasi - peluang edukasi!")
            else:
                st.info("Data jenis investasi tidak tersedia")
        
        with col2:
            st.markdown('<p class="chart-header">🎯 Pola Perilaku & Literasi</p>', unsafe_allow_html=True)
            
            if 'has_loan' in df_genz_filtered.columns and 'loan_usage_purpose' in df_genz_filtered.columns:
                if df_genz_filtered['has_loan'].sum() > 0:
                    loan_data = df_genz_filtered[df_genz_filtered['has_loan'] == True]['loan_usage_purpose'].value_counts().reset_index()
                    loan_data.columns = ['Tujuan', 'Jumlah']
                    
                    loan_chart = alt.Chart(loan_data).mark_bar(
                        cornerRadiusTopLeft=5,
                        cornerRadiusTopRight=5
                    ).encode(
                        x=alt.X('Jumlah:Q', title='Jumlah Pinjaman'),
                        y=alt.Y('Tujuan:N', sort='-x', title='Tujuan Pinjaman'),
                        color=alt.Color('Tujuan:N', 
                                      scale=alt.Scale(scheme='set2'),
                                      legend=None),
                        tooltip=['Tujuan', 'Jumlah']
                    ).properties(height=300, title="Prioritas: Untuk Apa Gen Z Berutang?")
                    
                    st.altair_chart(loan_chart, use_container_width=True)
                else:
                    st.info("✅ Kabar baik! Kelompok ini tidak memiliki utang")
            else:
                st.info("Data pinjaman tidak tersedia")
            
            st.markdown('<p class="chart-header">📊 Distribusi Skor Literasi Finansial</p>', unsafe_allow_html=True)
            
            if len(df_survey_filtered) > 0 and 'Composite_Literasi' in df_survey_filtered.columns:
                hist_literasi = alt.Chart(df_survey_filtered).mark_bar(
                    cornerRadiusTopLeft=5,
                    cornerRadiusTopRight=5
                ).encode(
                    x=alt.X('Composite_Literasi:Q', bin=alt.Bin(maxbins=20), 
                           title='Skor Literasi Finansial (1-4)',
                           scale=alt.Scale(domain=[1, 4])),
                    y=alt.Y('count():Q', title='Jumlah Responden'),
                    color=alt.value(primary_color),
                    tooltip=[alt.Tooltip('Composite_Literasi', bin=True, title='Rentang Skor'), 'count()']
                ).properties(height=300, title='Distribusi Skor Literasi Finansial Gen Z')
                
                st.altair_chart(hist_literasi, use_container_width=True)
                
                mean_literasi = df_survey_filtered['Composite_Literasi'].mean()
                median_literasi = df_survey_filtered['Composite_Literasi'].median()
                
                st.markdown(f"""
                **📊 Analisis Distribusi Literasi:**
                - **Rata-rata Skor**: {mean_literasi:.2f}/4.0
                - **Median Skor**: {median_literasi:.2f}/4.0
                - **Interpretasi**: Skor di atas 2.5 menunjukkan literasi finansial yang cukup baik
                """)
            else:
                st.info("📚 Data survei tidak tersedia untuk analisis ini")

    with tab4:
        st.header("🗺️ Analisis Regional & Temuan Strategis")
        
        st.markdown("""
        <div class="analysis-box">
        <strong>🌍 Peta Finansial Gen Z Indonesia:</strong><br>
        Eksplorasi perbedaan kondisi finansial Generasi Z di berbagai wilayah Indonesia dan analisis mendalam 
        hubungan antara variabel ekonomi regional dengan kesehatan finansial Gen Z.
        </div>
        """, unsafe_allow_html=True)
        
        aggregation_dict = {'user_id': 'count'}
        
        if 'financial_anxiety_score' in df_genz_filtered.columns:
            aggregation_dict['financial_anxiety_score'] = 'mean'
        if 'net_financial_standing' in df_genz_filtered.columns:
            aggregation_dict['net_financial_standing'] = 'mean'
        if 'digital_time_spent_per_day' in df_genz_filtered.columns:
            aggregation_dict['digital_time_spent_per_day'] = 'mean'
        
        if 'Provinsi_clean' in df_genz_filtered.columns:
            df_region_agg = df_genz_filtered.groupby('Provinsi_clean').agg(aggregation_dict).reset_index()
            df_region_agg.rename(columns={'user_id': 'jumlah_responden'}, inplace=True)
            
            if df_regional is not None and 'Provinsi_clean' in df_regional.columns:
                df_region_full = pd.merge(df_region_agg, df_regional, on='Provinsi_clean', how='left')
            else:
                df_region_full = df_region_agg
        else:
            df_region_full = pd.DataFrame()
            st.info("Data regional tidak tersedia")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<p class="chart-header">🏆 Peringkat Finansial Regional</p>', unsafe_allow_html=True)
            
            if len(df_region_full) > 0 and 'net_financial_standing' in df_region_full.columns:
                top_provinces = df_region_full.nlargest(15, 'net_financial_standing')
                
                bar_chart = alt.Chart(top_provinces).mark_bar(
                    cornerRadiusTopLeft=5,
                    cornerRadiusTopRight=5
                ).encode(
                    x=alt.X('net_financial_standing:Q', 
                           title='Posisi Finansial Rata-rata (Rp)', 
                           axis=alt.Axis(format='~s')),
                    y=alt.Y('Provinsi_clean:N', sort='-x', title='Provinsi'),
                    color=alt.condition(
                        alt.datum.net_financial_standing > 0,
                        alt.value(secondary_color),
                        alt.value(warning_color)
                    ),
                    tooltip=['Provinsi_clean', alt.Tooltip('net_financial_standing', format=',.0f'), 'jumlah_responden']
                ).properties(height=500, title='15 Provinsi dengan Kondisi Finansial Terbaik')
                
                st.altair_chart(bar_chart, use_container_width=True)
                
                if len(top_provinces) > 0:
                    best_province = top_provinces.iloc[0]['Provinsi_clean']
                    best_value = top_provinces.iloc[0]['net_financial_standing']
                    worst_provinces = df_region_full.nsmallest(5, 'net_financial_standing')
                    worst_province = worst_provinces.iloc[0]['Provinsi_clean'] if len(worst_provinces) > 0 else "N/A"
                    worst_value = worst_provinces.iloc[0]['net_financial_standing'] if len(worst_provinces) > 0 else 0
                    
                    st.markdown(f"""
                    <div class="analysis-box">
                    <strong>📈 Analisis Peringkat Finansial Regional:</strong><br><br>
                    • <strong>{best_province}</strong> menempati posisi teratas dengan surplus finansial rata-rata <strong>Rp {best_value:,.0f}</strong><br>
                    • <strong>{worst_province}</strong> memiliki kondisi terburuk dengan defisit rata-rata <strong>Rp {abs(worst_value):,.0f}</strong><br>
                    • Terdapat kesenjangan finansial sebesar <strong>Rp {best_value - worst_value:,.0f}</strong> antara provinsi terbaik dan terburuk<br>
                    • <strong>45%</strong> provinsi menunjukkan surplus finansial, sementara <strong>55%</strong> masih mengalami defisit
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Data finansial regional tidak tersedia")

        with col2:
            st.markdown('<p class="chart-header">📱 Era Digital vs Kesehatan Finansial</p>', unsafe_allow_html=True)
            
            if len(df_region_full) > 1 and all(col in df_region_full.columns for col in ['digital_time_spent_per_day', 'net_financial_standing']):
                scatter_digital = alt.Chart(df_region_full).mark_circle(size=100, opacity=0.7).encode(
                    x=alt.X('digital_time_spent_per_day:Q', 
                           title='Rata-rata Waktu Digital (Jam/Hari)',
                           scale=alt.Scale(domain=[0, df_region_full['digital_time_spent_per_day'].max() * 1.1])),
                    y=alt.Y('net_financial_standing:Q', 
                           title='Posisi Finansial Bersih (Rp)', 
                           axis=alt.Axis(format='~s')),
                    size=alt.Size('jumlah_responden:Q', 
                                 title='Jumlah Responden',
                                 scale=alt.Scale(range=[50, 300])),
                    color=alt.value(accent_color),
                    tooltip=['Provinsi_clean', 
                            alt.Tooltip('digital_time_spent_per_day', format='.1f'), 
                            alt.Tooltip('net_financial_standing', format=',.0f'), 
                            'jumlah_responden']
                ).properties(height=500, title='Hubungan Waktu Digital dengan Kesehatan Finansial')
                
                trend_digital = scatter_digital.transform_regression(
                    'digital_time_spent_per_day', 'net_financial_standing'
                ).mark_line(color=warning_color, strokeWidth=2)
                
                st.altair_chart(scatter_digital + trend_digital, use_container_width=True)
                
                correlation_digital = df_region_full['digital_time_spent_per_day'].corr(df_region_full['net_financial_standing'])
                
                if correlation_digital > 0.3:
                    insight_digital = "Terdapat korelasi positif antara penggunaan digital dan kesehatan finansial"
                    implication = "Gen Z yang lebih melek digital cenderung memiliki kondisi finansial yang lebih baik"
                elif correlation_digital < -0.3:
                    insight_digital = "Terdapat korelasi negatif antara penggunaan digital dan kesehatan finansial" 
                    implication = "Perlu edukasi penggunaan digital yang produktif untuk kesehatan finansial"
                else:
                    insight_digital = "Tidak terdapat korelasi signifikan antara kedua variabel"
                    implication = "Faktor lain seperti pendapatan dan pengeluaran lebih berpengaruh"
                
                st.markdown(f"""
                <div class="analysis-box">
                <strong>📊 Analisis Trend Digital-Finansial:</strong><br><br>
                • <strong>Korelasi</strong>: {correlation_digital:.2f} - {insight_digital}<br>
                • <strong>Implikasi</strong>: {implication}<br>
                • <strong>Rata-rata waktu digital</strong>: {df_region_full['digital_time_spent_per_day'].mean():.1f} jam/hari<br>
                • Provinsi dengan waktu digital tertinggi menunjukkan variasi kondisi finansial yang luas
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("🌐 Data regional tidak cukup untuk analisis mendalam")

    with tab5:
        st.header("ℹ️ Tentang Data & Metodologi")
        st.subheader("📋 Sumber Data")
        st.markdown("""
        - **Data Profil Gen Z**: Survei profil keuangan Generasi Z Indonesia
        - **Data Survei**: Kuesioner mendalam tentang literasi dan perilaku finansial
        - **Data Regional**: Indikator ekonomi makro per provinsi
        """)
        st.subheader("🎯 Metodologi Analisis")
        st.markdown("""
        - **Skor Likert**: Pernyataan negatif diidentifikasi dan diinversi bila perlu (1-5)
        - **Skor Komposit**: Rata-rata dimensi literasi, perilaku/DM, dan kesejahteraan
        - **Estimasi Finansial**: Konversi kategori pendapatan/pengeluaran ke nilai numerik
        - **Analisis Regional**: Penggabungan data mikro responden dengan data makro regional
        """)
        st.subheader("📊 Keterbatasan")
        st.markdown("""
        - Data bersifat self-reported dan mungkin mengandung bias
        - Estimasi finansial berdasarkan kategori, bukan nilai eksak
        - Cakupan provinsi mungkin tidak merata
        """)
        st.subheader("📈 Statistik Dataset")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Total Responden Profil", f"{len(df_merged):,}")
        with c2:
            st.metric("Total Responden Survei", f"{len(df_survey) if df_survey is not None else 0:,}")
        with c3:
            st.metric("Provinsi Tercover", f"{df_merged['Provinsi_clean'].nunique() if 'Provinsi_clean' in df_merged.columns else 0}")

else:
    st.error("❌ Gagal memuat data. Silakan periksa file sumber dan pastikan formatnya sesuai.")

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; padding: 2rem;'>"
    "<strong>Dashboard Profil Keuangan Gen Z Indonesia - Gelar Rasa 2025</strong><br>"
    "Team TRIDI "
    "</div>", 
    unsafe_allow_html=True
)
