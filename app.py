import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression

# 1. Sahifa sozlamalari
st.set_page_config(page_title="AI Business Intelligence", layout="wide", page_icon="📈")

st.title("📊 Professional AI Biznes Tahlilchi")

# Sidebar - Sozlamalar
with st.sidebar:
    st.header("📂 Ma'lumotlarni yuklash")
    uploaded_file = st.file_uploader("Walmart 'train.csv' faylini tanlang", type=['csv'])
    
    st.divider()
    # Valyuta yoki birlikni tanlash
    currency = st.selectbox("Birlikni tanlang:", ["USD", "UZS", "AUS"])

if uploaded_file is not None:
    # Ma'lumotni o'qish
    df = pd.read_csv(uploaded_file)
    df['Date'] = pd.to_datetime(df['Date'])

    # 2. FILTRLASH - Chalkashlikni yo'qotamiz
    st.sidebar.subheader("🎯 Filtrlash")
    
    # Do'konni tanlash
    store_ids = sorted(df['Store'].unique())
    selected_store = st.sidebar.selectbox("Do'kon raqamini tanlang:", store_ids)
    
    # Tanlangan do'kon bo'limlarini olish
    df_store = df[df['Store'] == selected_store]
    dept_ids = sorted(df_store['Dept'].unique())
    selected_dept = st.sidebar.selectbox(f"{selected_store}-do'kondagi bo'limni tanlang:", dept_ids)
    
    # Yakuniy toza ma'lumot
    df_final = df_store[df_store['Dept'] == selected_dept].sort_values('Date')

    # 3. ASOSIY MONITORING
    st.subheader(f"🏠 {selected_store}-do'kon, {selected_dept}-bo'lim hisoboti")
    
    c1, c2, c3 = st.columns(3)
    total_sales = df_final['Weekly_Sales'].sum()
    avg_sales = df_final['Weekly_Sales'].mean()
    max_sales = df_final['Weekly_Sales'].max()

    c1.metric("Umumiy Savdo", f"{total_sales:,.0f} {currency}")
    c2.metric("O'rtacha Haftalik Savdo", f"{avg_sales:,.0f} {currency}")
    c3.metric("Eng yuqori savdo", f"{max_sales:,.0f} {currency}")

    # 4. GRAFIK (Tiniq va tushunarli)
    st.divider()
    st.write("### 📈 Haftalik savdo dinamikasi")
    fig = px.area(df_final, x='Date', y='Weekly_Sales', 
                 labels={'Weekly_Sales': f'Savdo ({currency})', 'Date': 'Vaqt'},
                 color_discrete_sequence=['#00CC96'])
    st.plotly_chart(fig, use_container_width=True)

    # 5. AI BASHORATI
    st.divider()
    st.subheader("🤖 AI Bashorati")
    
    # Bashorat uchun model (Linear Regression)
    X = np.array(range(len(df_final))).reshape(-1, 1)
    y = df_final['Weekly_Sales'].values
    model = LinearRegression().fit(X, y)
    prediction = model.predict([[len(df_final)]])[0]

    st.success(f"Kelasi hafta uchun kutilayotgan savdo: **{prediction:,.2f} {currency}**")
    
    # AI Tavsiyasi
    if prediction > avg_sales:
        st.info(f"💡 **AI Tavsiyasi:** Savdo ko'tarilishi kutilmoqda. {currency}lik mahsulotlar zaxirasini tekshiring!")
    else:
        st.warning(f"⚠️ **AI Tavsiyasi:** Savdo pasayishi kutilmoqda. Marketing kampaniyalarini faollashtiring.")

else:
    st.info("Iltimos, Walmart faylini yuklang. Shunda tahlillarni boshlaymiz.")
