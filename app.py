import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression
from fpdf import FPDF
import base64

st.set_page_config(page_title="AI Raqamli Tahlilchi", layout="wide", page_icon="📈")

st.title("📊 KOB uchun AI 'Raqamli Tahlilchi'")

# Sidebar
with st.sidebar:
    st.header("📁 Ma'lumotlar")
    uploaded_file = st.file_uploader("Excel/CSV faylni tanlang", type=['csv', 'xlsx'])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
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

        # --- PDF YARATISH QISMI ---
        def create_pdf(df, bashorat):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, txt="AI Raqamli Tahlilchi Hisoboti", ln=True, align='C')
            
            pdf.set_font("Arial", size=12)
            pdf.ln(10)
            pdf.cell(200, 10, txt=f"Umumiy Savdo: {df['Savdo'].sum()} mln so'm", ln=True)
            pdf.cell(200, 10, txt=f"Umumiy Foyda: {df['Foyda'].sum()} mln so'm", ln=True)
            pdf.cell(200, 10, txt=f"Kelasi oy uchun AI bashorati: {bashorat:.1f} mln so'm", ln=True)
            
            pdf.ln(10)
            pdf.cell(200, 10, txt="Oxirgi ko'rsatkichlar jadvali:", ln=True)
            pdf.set_font("Arial", size=10)
            for i in range(len(df)):
                row = f"{df['Sana'].dt.date.iloc[i]} | Savdo: {df['Savdo'].iloc[i]} | Xarajat: {df['Xarajat'].iloc[i]}"
                pdf.cell(200, 10, txt=row, ln=True)
            
            return pdf.output(dest='S').encode('latin-1')

        st.divider()
        pdf_data = create_pdf(df, bashorat)
        st.download_button(label="📥 PDF Hisobotni yuklab olish",
                           data=pdf_data,
                           file_name="biznes_hisobot.pdf",
                           mime="application/pdf")

    except Exception as e:
        st.error(f"Xatolik: {e}")
else:
    st.warning("Iltimos, fayl yuklang.")            with col3:
                rentabellik = (df['Foyda'].sum() / df['Savdo'].sum()) * 100
                st.metric("Rentabellik", f"{rentabellik:.1f}%")

            # Grafik
            st.subheader("📈 Savdo va Xarajatlar dinamikasi")
            fig = px.line(df, x='Sana', y=['Savdo', 'Xarajat'], markers=True)
            st.plotly_chart(fig, use_container_width=True)

            # AI Bashorati
            X = np.array(range(len(df))).reshape(-1, 1)
            y = df['Savdo'].values
            model = LinearRegression().fit(X, y)
            bashorat = model.predict([[len(df)]])[0]

            st.success(f"🤖 AI Bashorati: Kelasi oyda kutilayotgan savdo: {bashorat:,.1f} mln so'm")
            
            if df['Xarajat'].iloc[-1] > df['Savdo'].iloc[-1] * 0.7:
                st.warning("⚠️ AI Tavsiyasi: Oxirgi oyda xarajatlar juda yuqori bo'lgan. Tejamkorlik choralarini ko'ring.")
        else:
            st.error(f"Faylda quyidagi ustunlar bo'lishi shart: {required_columns}")
    except Exception as e:
        st.error(f"Xatolik yuz berdi: {e}")
else:
    st.info("Iltimos, chap tarafdagi menyu orqali ma'lumotlarni yuklang. Namuna sifatida 'Sana', 'Savdo', 'Xarajat' ustunlari bo'lishi kerak.")
