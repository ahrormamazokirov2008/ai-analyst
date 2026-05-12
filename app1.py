import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Universal AI Business Analyst", layout="wide")

st.title("📊 Universal Biznes Analitika Platformasi")

# 1. MA'LUMOT YUKLASH
with st.sidebar:
    st.header("📂 Ma'lumotlar")
    uploaded_file = st.file_uploader("Faylni yuklang (CSV/Excel)", type=['csv', 'xlsx'])

if uploaded_file:
    # Faylni o'qish
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    
    # Ustunlarni avtomatik qidirish (Sana, Savdo, Xarajat)
    date_col = next((c for c in df.columns if any(x in c.lower() for x in ['date', 'sana', 'time'])), None)
    # Savdo va Xarajat ustunlarini tanlash (Foydalanuvchi tanlashi uchun sidebar)
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    st.sidebar.divider()
    st.sidebar.subheader("⚙️ Sozlamalar")
    sales_col = st.sidebar.selectbox("Savdo (Tushum) ustunini tanlang:", numeric_cols)
    expense_col = st.sidebar.selectbox("Xarajat (Chiqim) ustunini tanlang (agar bo'lsa):", ["Mavjud emas"] + numeric_cols)

    if date_col:
        df[date_col] = pd.to_datetime(df[date_col])
        df = df.sort_values(date_col)

    # 2. MOLIYAVIY MONITORING
    st.subheader("📌 Moliyaviy Holat")
    m1, m2, m3 = st.columns(3)
    
    total_sales = df[sales_col].sum()
    total_exp = df[expense_col].sum() if expense_col != "Mavjud emas" else 0
    
    m1.metric("Umumiy Savdo", f"{total_sales:,.0f}")
    m2.metric("Umumiy Xarajat", f"{total_exp:,.0f}")
    m3.metric("Sof Foyda", f"{(total_sales - total_exp):,.0f}")

    # 3. GRAFIK
    st.divider()
    plot_cols = [sales_col]
    if expense_col != "Mavjud emas": plot_cols.append(expense_col)
    
    if date_col:
        fig = px.line(df, x=date_col, y=plot_cols, title="Biznesning o'zgarish dinamikasi")
        st.plotly_chart(fig, use_container_width=True)

    # 4. AI TAVSIYALARI (Tadbirkor tilida)
    st.divider()
    st.subheader("🤖 AI Strategik Maslahatlari")
    
    # Modelni o'qitish
    X = np.array(range(len(df))).reshape(-1, 1)
    model = LinearRegression().fit(X, df[sales_col].values)
    pred = model.predict([[len(df)]])[0]
    avg_s = df[sales_col].mean()
    growth = ((pred - avg_s) / avg_s) * 100

    c_left, c_right = st.columns(2)
    with c_left:
        st.info(f"🔮 **Bashorat:** Kelasi davrda savdo miqdori taxminan **{pred:,.0f}** bo'lishi kutilmoqda.")
    
    with c_right:
        st.write("### 🎯 Nima qilish kerak?")
        if growth > 5:
            st.success(f"✅ **Savdo o'smoqda:** Talab yuqori. Tavsiya: Mahsulotlar zaxirasini oshiring va mijozlar oqimiga tayyor turing.")
        elif growth < -5:
            st.warning("⚠️ **Savdo pasaymoqda:** Mijozlarni yo'qotish xavfi bor. Tavsiya: Narxlar strategiyasini qayta ko'rib chiqing yoki aksiyalar tashkil qiling.")
        else:
            st.write("ℹ️ **Stabil holat:** Katta o'zgarishlar kutilmayapti. Xizmat sifatini oshirishga e'tibor qarating.")

else:
    st.info("Boshlash uchun ma'lumotlar faylini yuklang.")
