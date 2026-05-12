import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="AI Raqamli Tahlilchi", layout="wide")

st.title("📊 KOB uchun AI 'Raqamli Tahlilchi'")
st.markdown("O'z biznes ma'lumotlaringizni yuklang va AI tahlilini oling.")

# --- FAYL YUKLASH QISMI ---
st.sidebar.header("Ma'lumotlar manbasi")
uploaded_file = st.sidebar.file_uploader("Excel yoki CSV faylni tanlang", type=['csv', 'xlsx'])

if uploaded_file is not None:
    # Faylni o'qish
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # Ustunlar borligini tekshirish (Sana, Savdo, Xarajat)
        required_columns = ['Sana', 'Savdo', 'Xarajat']
        if all(col in df.columns for col in required_columns):
            df['Sana'] = pd.to_datetime(df['Sana'])
            
            # Asosiy ko'rsatkichlar
            df['Foyda'] = df['Savdo'] - df['Xarajat']
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Umumiy Savdo", f"{df['Savdo'].sum():,.0f} mln")
            with col2:
                st.metric("Umumiy Foyda", f"{df['Foyda'].sum():,.0f} mln")
            with col3:
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
