import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression

# 1. SAHIFA SOZLAMALARI
st.set_page_config(page_title="Universal Business AI", layout="wide", page_icon="🧠")

st.title("🚀 Universal AI Business Analyst")
st.markdown("Istalgan kompaniya ma'lumotlarini yuklang va AI tahlilini oling.")

# 2. MA'LUMOT YUKLASH
with st.sidebar:
    st.header("📂 Ma'lumotlar bazasi")
    uploaded_file = st.file_uploader("CSV yoki Excel faylni tanlang", type=['csv', 'xlsx'])

if uploaded_file:
    # Faylni o'qish
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    
    # AVTOMATIK USTUNLARNI ANIQLASH
    # Sanani topish
    date_col = next((col for col in df.columns if any(x in col.lower() for x in ['date', 'sana', 'vaqt', 'timestamp'])), None)
    if date_col:
        df[date_col] = pd.to_datetime(df[date_col])
        df = df.sort_values(date_col)

    # Raqamli va Kategorial ustunlarni ajratish
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

    # 3. DINAMIK FILTRLAR (Agar bor bo'lsa)
    st.sidebar.divider()
    filtered_df = df.copy()
    if cat_cols:
        st.sidebar.subheader("🎯 Filtrlash")
        for col in cat_cols[:2]: # Faqat birinchi 2 ta kategoriyani filtrga chiqaramiz (chalkashlik bo'lmasligi uchun)
            options = ["Hammasi"] + sorted(df[col].unique().tolist())
            choice = st.sidebar.selectbox(f"{col} bo'yicha:", options)
            if choice != "Hammasi":
                filtered_df = filtered_df[filtered_df[col] == choice]

    # 4. TAHLIL QILINADIGAN KO'RSATKICHNI TANLASH
    target_metric = st.sidebar.selectbox("Tahlil ko'rsatkichi:", numeric_cols)

    # 5. ASOSIY MONITORING
    st.subheader(f"📊 {target_metric} bo'yicha tahliliy hisobot")
    
    m1, m2, m3 = st.columns(3)
    current_val = filtered_df[target_metric].iloc[-1]
    avg_val = filtered_df[target_metric].mean()
    total_val = filtered_df[target_metric].sum()

    m1.metric("Umumiy miqdor", f"{total_val:,.0f}")
    m2.metric("O'rtacha ko'rsatkich", f"{avg_sales:,.0f}" if 'avg_sales' in locals() else f"{avg_val:,.0f}")
    m3.metric("Oxirgi qayd etilgan", f"{current_val:,.0f}")

    # 6. GRAFIK
    if date_col:
        fig = px.line(filtered_df, x=date_col, y=target_metric, title=f"{target_metric} o'zgarish dinamikasi",
                     line_shape='spline', render_mode='svg')
        st.plotly_chart(fig, use_container_width=True)

    # 7. AI VA STRATEGIK TAVSIYALAR (Yaxshilangan mantiq)
    st.divider()
    st.subheader("🤖 AI Strategik Insights")
    
    # Linear Regression - Bashorat uchun
    X = np.array(range(len(filtered_df))).reshape(-1, 1)
    y = filtered_df[target_metric].values
    model = LinearRegression().fit(X, y)
    next_pred = model.predict([[len(filtered_df)]])[0]
    
    # Trendni aniqlash (Slope)
    slope = model.coef_[0]
    growth_rate = (slope / avg_val) * 100 if avg_val != 0 else 0

    col_a, col_b = st.columns(2)
    
    with col_a:
        st.write("### 🔮 Bashorat")
        st.success(f"Kelasi davr uchun taxminiy miqdor: **{next_pred:,.2f}**")
        st.write(f"Trend yo'nalishi: **{'O\'sish' if slope > 0 else 'Pasayish'}** ({growth_rate:.1f}% o'zgarish)")

    with col_b:
        st.write("### 💡 Strategik Tavsiya")
        if growth_rate > 5:
            st.info("✅ **O'sish tendensiyasi:** Ma'lumotlar barqaror o'sib bormoqda. Resurslarni kengaytirish va investitsiya kiritish uchun qulay vaqt.")
        elif growth_rate < -5:
            st.warning("⚠️ **Pasayish xavfi:** Ko'rsatkichlarda pasayish kuzatilyapti. Xarajatlarni optimallashtirish va mijozlarni jalb qilish strategiyasini o'zgartirish kerak.")
        else:
            st.write("ℹ️ **Stabil holat:** Katta o'zgarishlar kutilmayapti. Mavjud resurslarni saqlab qolish va kichik innovatsiyalar qilish tavsiya etiladi.")

else:
    st.info("Boshlash uchun istalgan biznes faylini yuklang (masalan: Savdo, Mijozlar oqimi, Ombor qoldiqlari).")
