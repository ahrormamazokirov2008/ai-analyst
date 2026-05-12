import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression
from fpdf import FPDF

# 1. Sahifa sozlamalari
st.set_page_config(page_title="AI Raqamli Tahlilchi", layout="wide", page_icon="📈")

st.title("📊 KOB uchun AI 'Raqamli Tahlilchi'")
st.markdown("Biznesingizni raqamlar va AI orqali professional tahlil qiling.")

# 2. Sidebar - Fayl yuklash
with st.sidebar:
    st.header("📁 Ma'lumotlar")
    uploaded_file = st.file_uploader("Excel/CSV faylni tanlang", type=['csv', 'xlsx'])
    st.info("Faylda 'Sana', 'Savdo', 'Xarajat' ustunlari bo'lishi shart.")

# 3. Asosiy mantiq
if uploaded_file is not None:
    try:
        # Faylni o'qish
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        # Ma'lumotlarni tayyorlash
        df['Sana'] = pd.to_datetime(df['Sana'])
        df = df.sort_values('Sana')
        df['Foyda'] = df['Savdo'] - df['Xarajat']

        # --- METRIKALAR ---
        c1, c2, c3 = st.columns(3)
        savdo_sum = df['Savdo'].sum()
        foyda_sum = df['Foyda'].sum()
        rentabellik = (foyda_sum / savdo_sum * 100) if savdo_sum != 0 else 0
        
        c1.metric("Umumiy Savdo", f"{savdo_sum:,.0f} mln")
        c2.metric("Umumiy Foyda", f"{foyda_sum:,.0f} mln")
        c3.metric("Rentabellik", f"{rentabellik:.1f}%")

        # --- GRAFIK ---
        st.subheader("📈 Savdo va Xarajatlar dinamikasi")
        fig = px.line(df, x='Sana', y=['Savdo', 'Xarajat'], markers=True, 
                     color_discrete_map={"Savdo": "#00CC96", "Xarajat": "#EF553B"})
        st.plotly_chart(fig, use_container_width=True)

        # --- AI BASHORAT ---
        X = np.array(range(len(df))).reshape(-1, 1)
        y = df['Savdo'].values
        model = LinearRegression().fit(X, y)
        bashorat = model.predict([[len(df)]])[0]
        
        st.success(f"🤖 **AI Bashorati:** Kelasi oyda kutilayotgan savdo: **{bashorat:,.1f} mln so'm**")

        # --- CHUQUR BIZNES TAHLIL ---
        st.divider()
        st.subheader("🧐 Biznesning " + "Sog'lig'i" + " Tahlili")
        
        # O'sish sur'ati
        if len(df) > 1:
            osish = ((df['Savdo'].iloc[-1] - df['Savdo'].iloc[-2]) / df['Savdo'].iloc[-2]) * 100
            st.write(f"📈 **O'sish sur'ati:** Oxirgi oyda savdo hajmi **{osish:.1f}%** ga o'zgardi.")
        
        # Xarajat ulushi
        xarajat_ulushi = (df['Xarajat'].iloc[-1] / df['Savdo'].iloc[-1]) * 100
        st.write(f"💸 **Xarajat ulushi:** Hozirda har 100 so'm daromadning **{xarajat_ulushi:.1f}** so'mi xarajatlarga ketyapti.")

        # AI Tavsiyasi
        st.subheader("💡 AI Strategik Tavsiyalari")
        if xarajat_ulushi > 80:
            st.warning("⚠️ **Xulosa:** Xarajatlaringiz daromadga nisbatan juda yuqori. Operatsion samaradorlikni oshirish va keraksiz xarajatlarni qisqartirish tavsiya etiladi.")
        elif osish < 0:
            st.info("ℹ️ **Xulosa:** Savdo hajmida pasayish kuzatildi. Marketing strategiyasini qayta ko'rib chiqish yoki mijozlar bilan ishlashni kuchaytirish lozim.")
        else:
            st.success("✅ **Xulosa:** Biznesingiz stabil rivojlanmoqda. Hozirgi yo'nalishni saqlab qoling va kengayish haqida o'ylang.")

        # --- PDF YARATISH ---
        def create_pdf(df_rep, pred):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, txt="AI Raqamli Tahlilchi Hisoboti", ln=True, align='C')
            pdf.ln(10)
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Umumiy Savdo: {df_rep['Savdo'].sum():,.1f} mln", ln=True)
            pdf.cell(200, 10, txt=f"Umumiy Foyda: {df_rep['Foyda'].sum():,.1f} mln", ln=True)
            pdf.cell(200, 10, txt=f"Kelasi oy uchun AI bashorati: {pred:,.1f} mln", ln=True)
            pdf.ln(10)
            pdf.cell(200, 10, txt="Oxirgi ko'rsatkichlar jadvali:", ln=True)
            pdf.set_font("Arial", size=10)
            for i in range(len(df_rep)):
                row = f"{df_rep['Sana'].dt.date.iloc[i]} | Savdo: {df_rep['Savdo'].iloc[i]} | Xarajat: {df_rep['Xarajat'].iloc[i]}"
                pdf.cell(200, 10, txt=row, ln=True)
            return pdf.output(dest='S').encode('latin-1')

        pdf_bytes = create_pdf(df, bashorat)
        st.download_button(label="📥 PDF Hisobotni yuklab olish",
                           data=pdf_bytes,
                           file_name="biznes_tahlil_hisoboti.pdf",
                           mime="application/pdf")

    except Exception as e:
        st.error(f"Xatolik yuz berdi: {e}")
else:
    st.info("Iltimos, chap tarafdagi menyu orqali Excel faylingizni yuklang.")
