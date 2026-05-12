import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression
from fpdf import FPDF

# --- SAHIFA SOZLAMALARI ---
st.set_page_config(page_title="AI Business Architect", layout="wide")

# --- MODULLAR (Funksiyalar) ---

def dashboard_module(df):
    st.subheader("📊 Asosiy Monitoring")
    c1, c2, c3 = st.columns(3)
    c1.metric("Umumiy Savdo", f"{df['Savdo'].sum():,.0f} mln")
    c2.metric("Umumiy Foyda", f"{df['Foyda'].sum():,.0f} mln")
    c3.metric("Rentabellik", f"{(df['Foyda'].sum()/df['Savdo'].sum()*100):.1f}%")
    
    fig = px.line(df, x='Sana', y=['Savdo', 'Xarajat'], title="Savdo dinamikasi", markers=True)
    st.plotly_chart(fig, use_container_width=True)

def what_if_module(df):
    st.subheader("🧪 Strategik Simulyator (What-If)")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        growth = st.slider("Savdo o'sishi (%)", 0, 100, 10)
        reduction = st.slider("Xarajatlarni qisqartirish (%)", 0, 50, 5)
    
    with col2:
        new_savdo = df['Savdo'].sum() * (1 + growth/100)
        new_xarajat = df['Xarajat'].sum() * (1 - reduction/100)
        new_foyda = new_savdo - new_xarajat
        st.success(f"Kutilayotgan yangi foyda: **{new_foyda:,.1f} mln**")
        st.info(f"Foyda o'zgarishi: **{new_foyda - df['Foyda'].sum():,.1f} mln**")

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
