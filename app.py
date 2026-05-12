import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression

# 1. Sahifa sozlamalari
st.set_page_config(page_title="Business AI Analyst", layout="wide", page_icon="📊")

st.title("🚀 Professional Biznes Analitika")

# 2. Ma'lumotlarni yuklash
with st.sidebar:
    st.header("📂 Fayl boshqaruvi")
    uploaded_file = st.file_uploader("Faylni tanlang (CSV/Excel)", type=['csv', 'xlsx'])

if uploaded_file is not None:
    # Faylni o'qish (xatoliklarni oldini olish bilan)
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, encoding='utf-8')
        else:
            df = pd.read_excel(uploaded_file)
    except:
        uploaded_file.seek(0)
        df = pd.read_csv(uploaded_file, encoding='latin-1')

    # Ustunlarni avtomatik qidirish
    date_col = next((c for c in df.columns if any(x in c.lower() for x in ['date', 'sana', 'vaqt'])), None)
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    st.sidebar.divider()
    st.sidebar.subheader("⚙️ Sozlamalar")
    sales_col = st.sidebar.selectbox("Savdo (Tushum) ustunini tanlang:", numeric_cols)
    expense_col = st.sidebar.selectbox("Xarajat (Chiqim) ustunini tanlang (ixtiyoriy):", ["Mavjud emas"] + numeric_cols)

    if date_col:
        df[date_col] = pd.to_datetime(df[date_col])
        df = df.sort_values(date_col)

    # 3. Asosiy ko'rsatkichlar
    st.subheader("📌 Moliyaviy Holat")
    c1, c2, c3 = st.columns(3)
    
    total_sales = df[sales_col].sum()
    total_exp = df[expense_col].sum() if expense_col != "Mavjud emas" else 0
    
    c1.metric("Umumiy Savdo", f"{total_sales:,.0f}")
    c2.metric("Umumiy Xarajat", f"{total_exp:,.0f}")
    c3.metric("Sof Foyda", f"{(total_sales - total_exp):,.0f}")

    # 4. Oddiy va tiniq grafik
    st.divider()
    st.subheader("📈 Savdo va Xarajat Dinamikasi")
    
    plot_cols = [sales_col]
    if expense_col != "Mavjud emas": plot_cols.append(expense_col)
    
    if date_col:
        fig = px.line(df, x=date_col, y=plot_cols, title="Vaqt kesimidagi o'zgarishlar")
        fig.update_xaxes(rangeslider_visible=True) # Faqat masshtab uchun surgich qoldi
        st.plotly_chart(fig, use_container_width=True)

    # 5. AI Tavsiyalari
    st.divider()
    st.subheader("🤖 AI Strategik Maslahatlari")
    
    X = np.array(range(len(df))).reshape(-1, 1)
    y = df[sales_col].values
    model = LinearRegression().fit(X, y)
    pred = model.predict([[len(df)]])[0]
    avg_s = df[sales_col].mean()
    growth = ((pred - avg_s) / avg_s) * 100

    col_l, col_r = st.columns(2)
    with col_l:
        st.info(f"🔮 **Bashorat:** Kelasi davrda savdo taxminan **{pred:,.0f}** bo'lishi kutilmoqda.")
    
    with col_r:
        st.write("### 🎯 Nima qilish kerak?")
        if growth > 5:
            st.success(f"✅ **Savdo o'smoqda:** Tovar zaxiralarini oshiring va mijozlar oqimiga tayyor turing.")
        elif growth < -5:
            st.warning("⚠️ **Savdo pasaymoqda:** Narxlar strategiyasini qayta ko'rib chiqing yoki aksiyalar tashkil qiling.")
        else:
            st.write("ℹ️ **Stabil holat:** Katta o'zgarishlar kutilmayapti. Xizmat sifatini oshiring.")

else:
    st.info("Boshlash uchun biznes ma'lumotlarini yuklang.")
