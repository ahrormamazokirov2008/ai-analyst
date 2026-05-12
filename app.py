import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression

# 1. SAHIFA SOZLAMALARI
st.set_page_config(page_title="Universal AI Analyst Pro", layout="wide", page_icon="📈")

st.title("📊 Universal AI Biznes Analitika")

# 2. MA'LUMOT YUKLASH (Aqliy o'qish tizimi bilan)
with st.sidebar:
    st.header("📂 Ma'lumotlar")
    uploaded_file = st.file_uploader("Faylni yuklang (CSV/Excel)", type=['csv', 'xlsx'])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, encoding='utf-8')
        else:
            df = pd.read_excel(uploaded_file)
    except UnicodeDecodeError:
        uploaded_file.seek(0)
        df = pd.read_csv(uploaded_file, encoding='latin-1')

    # Ustunlarni avtomatik aniqlash
    date_col = next((c for c in df.columns if any(x in c.lower() for x in ['date', 'sana', 'vaqt', 'time'])), None)
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    st.sidebar.divider()
    st.sidebar.subheader("⚙️ Tahlil sozlamalari")
    sales_col = st.sidebar.selectbox("Savdo (Tushum) ustunini tanlang:", numeric_cols)
    expense_col = st.sidebar.selectbox("Xarajat (Chiqim) ustunini tanlang (ixtiyoriy):", ["Mavjud emas"] + numeric_cols)

    if date_col:
        df[date_col] = pd.to_datetime(df[date_col])
        df = df.sort_values(date_col)

    # 3. MOLIYAVIY MONITORING
    st.subheader("📌 Moliyaviy Holat")
    m1, m2, m3 = st.columns(3)
    
    total_sales = df[sales_col].sum()
    total_exp = df[expense_col].sum() if expense_col != "Mavjud emas" else 0
    
    m1.metric("Umumiy Savdo", f"{total_sales:,.0f}")
    m2.metric("Umumiy Xarajat", f"{total_exp:,.0f}")
    m3.metric("Sof Foyda", f"{(total_sales - total_exp):,.0f}")

    # 4. SMART GRAFIK (Katta ma'lumotlar uchun tekislash tizimi)
    st.divider()
    st.subheader("📈 Dinamika Tahlili")
    
    plot_cols = [sales_col]
    if expense_col != "Mavjud emas": plot_cols.append(expense_col)
    
    if date_col:
        plot_df = df.copy()
        
        # Katta ma'lumotlar uchun filtrlar
        if len(df) > 30:
            view_type = st.radio("Ma'lumotlarni ko'rsatish shakli:", 
                                ["Asl holati (Kunlik)", "Haftalik trend (Tekislangan)", "Oylik xulosa"], horizontal=True)
            
            if view_type == "Haftalik trend (Tekislangan)":
                for col in plot_cols:
                    plot_df[col] = plot_df[col].rolling(window=7).mean()
                st.info("💡 Grafik 7 kunlik siljuvchi o'rtacha asosida tekislandi.")
            elif view_type == "Oylik xulosa":
                plot_df = plot_df.resample('M', on=date_col).sum().reset_index()
                st.info("💡 Ma'lumotlar oylar bo'yicha umumlashtirildi.")

        # Grafik chizish
        fig = px.line(plot_df, x=date_col, y=plot_cols, title="Biznes o'zgarish dinamikasi")
        fig.update_xaxes(rangeslider_visible=True) # Surgich qo'shish
        st.plotly_chart(fig, use_container_width=True)

    # 5. AI BASHORAT VA TAVSIYALAR
    st.divider()
    st.subheader("🤖 AI Strategik Maslahatlari")
    
    X = np.array(range(len(df))).reshape(-1, 1)
    y = df[sales_col].values
    model = LinearRegression().fit(X, y)
    pred = model.predict([[len(df)]])[0]
    avg_s = df[sales_col].mean()
    growth = ((pred - avg_s) / avg_s) * 100

    c_left, c_right = st.columns(2)
    with c_left:
        st.info(f"🔮 **Bashorat:** Kelasi davrda savdo miqdori taxminan **{pred:,.0f}** bo'lishi kutilmoqda.")
    
    with c_right:
        st.write("### 🎯 Nima qilish kerak?")
        if growth > 5:
            st.success(f"✅ **Savdo o'smoqda:** Talab yuqori. Tavsiya: Tovar zaxiralarini oshiring va mijozlar oqimiga tayyor turing.")
        elif growth < -5:
            st.warning("⚠️ **Savdo pasaymoqda:** Mijozlarni yo'qotish xavfi bor. Tavsiya: Narxlar strategiyasini qayta ko'rib chiqing yoki aksiyalar tashkil qiling.")
        else:
            st.write("ℹ️ **Stabil holat:** Katta o'zgarishlar kutilmayapti. Xizmat sifatini oshirishga e'tibor qarating.")

else:
    st.info("Boshlash uchun biznes ma'lumotlarini yuklang.")
