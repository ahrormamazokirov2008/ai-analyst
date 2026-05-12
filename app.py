import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="AI Business Architect", layout="wide", page_icon="🚀")

st.title("🚀 Big Data AI Analitika — Walmart Edition")

with st.sidebar:
    st.header("📁 Ma'lumotlar")
    uploaded_file = st.file_uploader("CSV faylni yuklang (Walmart train.csv)", type=['csv'])

if uploaded_file:
    # Ma'lumotni yuklash
    df = pd.read_csv(uploaded_file)
    
    # 1. SANANI AVTOMATIK TOPISH
    date_col = None
    for col in df.columns:
        if col.lower() in ['date', 'sana', 'timestamp', 'time']:
            date_col = col
            df[date_col] = pd.to_datetime(df[date_col])
            break
    
    if date_col:
        # 2. DO'KONLARNI FILTRLASH (Walmart ma'lumotlari uchun maxsus)
        if 'Store' in df.columns:
            st.sidebar.divider()
            stores = sorted(df['Store'].unique())
            selected_store = st.sidebar.selectbox("Do'konni tanlang:", stores)
            df = df[df['Store'] == selected_store]
            st.sidebar.info(f"{selected_store}-do'kon ma'lumotlari yuklandi.")

        # 3. TAHLIL USTUNINI TANLASH
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        target_col = st.sidebar.selectbox("Tahlil qilinadigan raqamli ustun:", numeric_cols, 
                                         index=numeric_cols.index('Weekly_Sales') if 'Weekly_Sales' in numeric_cols else 0)

        # ASOSIY MONITORING
        st.subheader(f"📊 {selected_store if 'Store' in df.columns else ''} Do'kon: {target_col} Dinamikasi")
        
        # Grafik
        fig = px.line(df, x=date_col, y=target_col, title=f"Vaqt bo'yicha {target_col} o'zgarishi")
        st.plotly_chart(fig, use_container_width=True)

        # 4. AI BASHORATI (Training)
        st.divider()
        st.subheader("🤖 AI Bashorat Modeli")
        
        df_clean = df.dropna(subset=[target_col])
        X = np.array(range(len(df_clean))).reshape(-1, 1)
        y = df_clean[target_col].values
        
        model = LinearRegression().fit(X, y)
        prediction = model.predict([[len(df_clean)]])[0]
        
        st.success(f"Kelasi davr uchun AI bashorati: **{prediction:,.2f}**")
        
        # Qo'shimcha statistika
        col1, col2 = st.columns(2)
        col1.metric("O'rtacha ko'rsatkich", f"{df_clean[target_col].mean():,.2f}")
        col2.metric("Eng yuqori natija", f"{df_clean[target_col].max():,.2f}")

    else:
        st.error("Xatolik: Faylda sana ustuni topilmadi. Ustun nomi 'Date' yoki 'Sana' ekanligini tekshiring.")
else:
    st.info("Walmart 'train.csv' faylini yuklang va Big Data tahlilini boshlang.")
def ai_prediction_module(df):
    st.subheader("🤖 AI Bashorati")
    X = np.array(range(len(df))).reshape(-1, 1)
    y = df['Savdo'].values
    model = LinearRegression().fit(X, y)
    bashorat = model.predict([[len(df)]])[0]
    st.success(f"Kelasi oy uchun AI bashorati: **{bashorat:,.1f} mln so'm**")

# --- ASOSIY ILOVA LOGIKASI ---
with st.sidebar:
    st.title("🚀 Business AI")
    uploaded_file = st.file_uploader("Excel/CSV yuklang", type=['xlsx', 'csv'])
    
    if uploaded_file:
        # Menyu tanlash (Bu yerda yangi funksiyalar qo'shilsa ham eskilariga zarar yetmaydi)
        menu = st.radio("Bo'limni tanlang:", 
                        ["Dashboard", "What-If Simulator", "AI Prediction", "Ombor Tahlili (Tez kunda)"])

if uploaded_file:
    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)
    df['Sana'] = pd.to_datetime(df['Sana'])
    df['Foyda'] = df['Savdo'] - df['Xarajat']

    if menu == "Dashboard":
        dashboard_module(df)
    elif menu == "What-If Simulator":
        what_if_module(df)
    elif menu == "AI Prediction":
        ai_prediction_module(df)
    elif menu == "Ombor Tahlili (Tez kunda)":
        st.warning("Bu bo'lim ustida ishlayapmiz. Keyingi yangilanishda qo'shiladi!")
else:
    st.info("Boshlash uchun ma'lumotlar faylini yuklang.")
