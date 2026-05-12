import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression
from fpdf import FPDF

st.set_page_config(page_title="AI Raqamli Tahlilchi", layout="wide", page_icon="📈")

st.title("📊 KOB uchun AI 'Raqamli Tahlilchi'")

# Sidebar
with st.sidebar:
    st.header("📁 Ma'lumotlar")
    uploaded_file = st.file_uploader("Excel/CSV faylni tanlang", type=['csv', 'xlsx'])

if uploaded_file is not None:
    try:
        # Faylni o'qish
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        df['Sana'] = pd.to_datetime(df['Sana'])
        df['Foyda'] = df['Savdo'] - df['Xarajat']

        # Metrikalar
        c1, c2, c3 = st.columns(3)
        savdo_sum = df['Savdo'].sum()
        foyda_sum = df['Foyda'].sum()
        c1.metric("Umumiy Savdo", f"{savdo_sum} mln")
        c2.metric("Umumiy Foyda", f"{foyda_sum} mln")
        c3.metric("Rentabellik", f"{(foyda_sum/savdo_sum*100):.1f}%")

        # Grafik
        fig = px.line(df, x='Sana', y=['Savdo', 'Xarajat'], title="📈 Biznes Dinamikasi", markers=True)
        st.plotly_chart(fig, use_container_width=True)

        # AI Bashorat
        X = np.array(range(len(df))).reshape(-1, 1)
        y = df['Savdo'].values
        model = LinearRegression().fit(X, y)
        bashorat = model.predict([[len(df)]])[0]
        
        st.success(f"🤖 **AI Bashorati:** Kelasi oyda kutilayotgan savdo: **{bashorat:.1f} mln so'm**")

        # PDF Yaratish funksiyasi
        def create_pdf_file(df_report, pred):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, txt="AI Raqamli Tahlilchi Hisoboti", ln=True, align='C')
            pdf.ln(10)
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Umumiy Savdo: {df_report['Savdo'].sum()} mln so'm", ln=True)
            pdf.cell(200, 10, txt=f"Umumiy Foyda: {df_report['Foyda'].sum()} mln so'm", ln=True)
            pdf.cell(200, 10, txt=f"AI Bashorati (kelasi oy): {pred:.1f} mln so'm", ln=True)
            pdf.ln(10)
            pdf.cell(200, 10, txt="Oxirgi ko'rsatkichlar:", ln=True)
            pdf.set_font("Arial", size=10)
            for i in range(len(df_report)):
                txt_row = f"{df_report['Sana'].dt.date.iloc[i]} | Savdo: {df_report['Savdo'].iloc[i]} | Xarajat: {df_report['Xarajat'].iloc[i]}"
                pdf.cell(200, 10, txt=txt_row, ln=True)
            return pdf.output(dest='S').encode('latin-1')

        st.divider()
        pdf_bytes = create_pdf_file(df, bashorat)
        st.download_button(label="📥 PDF Hisobotni yuklab olish",
                           data=pdf_bytes,
                           file_name="biznes_hisobot.pdf",
                           mime="application/pdf")

    except Exception as e:
        st.error(f"Xatolik yuz berdi: {e}")
else:
    st.info("Iltimos, chap tarafdagi menyu orqali Excel faylingizni yuklang.")
