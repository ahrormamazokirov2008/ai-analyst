import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression

# 1. Sahifa sozlamalari
st.set_page_config(page_title="AI Business Intelligence", layout="wide")

st.title("📊 Professional AI Biznes Tahlilchi")

# Sidebar - Fayl yuklash
with st.sidebar:
    st.header("📂 Ma'lumotlarni yuklash")
    uploaded_file = st.file_uploader("Walmart 'train.csv' faylini tanlang", type=['csv'])
    
    # Valyuta tanlash (Siz so'ragandek)
    currency = st.selectbox("Valyutani tanlang:", ["$", "so'm", "ta"])

if uploaded_file:
    # Ma'lumotni o'qish (Faqat kerakli ustunlarni o'qiymiz, tezroq ishlashi uchun)
    df = pd.read_csv(uploaded_file)
    df['Date'] = pd.to_datetime(df['Date'])

    # 2. FILTRLASH - Chalkashlikni yo'qotamiz
    st.sidebar.divider()
    st.sidebar.subheader("🎯 Filtrlash")
    
    # Do'konni tanlash
    store_id = st.sidebar.selectbox("Do'kon raqamini tanlang:", sorted(df['Store'].unique()))
    
    # Bo'limni tanlash
    df_store = df[df['Store'] == store_id]
    dept_id = st.sidebar.selectbox(f"{store_id}-do'kondagi bo'limni tanlang:", sorted(df_store['Dept'].unique()))
    
    # Yakuniy toza ma'lumot
    df_final = df_store[df_store['Dept'] == dept_id].sort_values('Date')

    # 3. ASOSIY MONITORING (Raqamlar va birliklar bilan)
    st.subheader(f"🏠 {store_id}-do'kon, {dept_id}-bo'lim bo'yicha hisobot")
    
    c1, c2, c3 = st.columns(3)
    total_sales = df_final['Weekly_Sales'].sum()
    avg_sales = df_final['Weekly_Sales'].mean()
    max_sales = df_final['Weekly_Sales'].max()

    # Raqamlarni chiroyli formatda chiqarish (1,234.56 $)
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
    
    X = np.array(range(len(df_final))).reshape(-1, 1)
    y = df_final['Weekly_Sales'].values
    model = LinearRegression().fit(X, y)
    prediction = model.predict([[len(df_final)]])[0]

    st.success(f"Kelasi hafta uchun kutilayotgan savdo miqdori: **{prediction:,.2f} {currency}**")
    
    # AI Tavsiyasi
    if prediction > avg_sales:
        st.info(f"💡 AI Tavsiyasi: Kelasi haftada savdo o'rtacha ko'rsatkichdan yuqori bo'lishi kutilmoqda. Skladni **{currency}**lik mahsulotlar bilan to'ldiring!")
    else:
        st.warning(f"⚠️ AI Tavsiyasi: Savdo pasayishi kutilmoqda. Marketingga e'tibor bering.")

else:
    st.info("Iltimos, Walmart faylini yuklang. Shunda tahlillarni boshlaymiz.")        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
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
