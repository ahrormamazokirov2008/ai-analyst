import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="AI Business Intelligence Pro", layout="wide", page_icon="📊")

st.title("🚀 Professional Biznes Analitika va Bashorat")

# 1. MA'LUMOT YUKLASH
with st.sidebar:
    st.header("📂 Ma'lumotlar")
    uploaded_file = st.file_uploader("CSV yoki Excel faylni tanlang", type=['csv', 'xlsx'])

if uploaded_file:
    # 1. Faylni o'qish (Encoding xatosini oldini olish bilan)
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, encoding='utf-8')
        else:
            df = pd.read_excel(uploaded_file)
    except:
        uploaded_file.seek(0)
        df = pd.read_csv(uploaded_file, encoding='latin-1')

    # ✨ Chatbot boshqa sahifada ma'lumotni ko'rishi uchun xotiraga saqlaymiz
    st.session_state['data'] = df 

    # Avtomatik ustunlarni aniqlash (Sana, Savdo, Xarajat)
    date_col = next((col for col in df.columns if any(x in col.lower() for x in ['date', 'sana', 'vaqt'])), None)
    sales_col = next((col for col in df.columns if any(x in col.lower() for x in ['sales', 'savdo', 'tushum'])), None)
    expense_col = next((col for col in df.columns if any(x in col.lower() for x in ['expense', 'xarajat', 'chiqim'])), None)

    if date_col:
        df[date_col] = pd.to_datetime(df[date_col])
        df = df.sort_values(date_col)
        # Ma'lumot oralig'ini aniqlash (Kunlik, Haftalik, Oylik)
        days_diff = (df[date_col].max() - df[date_col].min()).days
        data_points = len(df)
        time_unit = "kunlik" if days_diff / data_points < 2 else "haftalik" if days_diff / data_points < 10 else "oylik"
        
    # 2. METRIKALAR (SAVDO VA XARAJAT ALOHIDA)
    st.subheader("📌 Moliyaviy Holat")
    m1, m2, m3, m4 = st.columns(4)
    
    total_sales = df[sales_col].sum() if sales_col else 0
    total_expenses = df[expense_col].sum() if expense_col else 0
    total_profit = total_sales - total_expenses
    
    m1.metric("Umumiy Savdo", f"{total_sales:,.0f}")
    m1.caption("Barcha davrlar uchun jami tushum")
    
    m2.metric("Umumiy Xarajat", f"{total_expenses:,.0f}")
    m2.caption("Barcha davrlar uchun jami chiqim")
    
    m3.metric("Sof Foyda", f"{total_profit:,.0f}")
    m3.caption("Savdo va xarajat o'rtasidagi farq")
    
    # 3. VAQTGA BOG'LANGAN O'RTACHA KO'RSATKICH (Tuzatish 2)
    avg_expense = df[expense_col].mean() if expense_col else 0
    m4.metric(f"O'rtacha {time_unit} xarajat", f"{avg_expense:,.0f}")
    m4.caption(f"Ma'lumotlar {time_unit} formatda tahlil qilinmoqda")

    # 4. Aqlli va tiniq grafik
    st.divider()
    st.subheader("📈 Savdo va Xarajat Dinamikasi")
    
    plot_cols = [sales_col]
    if expense_col != "Mavjud emas": plot_cols.append(expense_col)
    
    if date_col:
        plot_df = df.copy()
        
        # AVTOMATIK GRUPLASH (Chalkashlikni oldini olish uchun)
        if len(df) > 90: # Agar 3 oydan ko'p ma'lumot bo'lsa
            plot_df = plot_df.resample('W', on=date_col).mean().reset_index()
            st.info("💡 Ma'lumotlar juda ko'p bo'lgani uchun grafik 'Haftalik o'rtacha' ko'rinishiga o'tkazildi.")
        elif len(df) > 30: # Agar 1 oydan ko'p bo'lsa
            plot_df = plot_df.resample('3D', on=date_col).mean().reset_index()
            st.info("💡 Grafik tushunarli bo'lishi uchun ma'lumotlar 3 kunlik oraliqda umumlashtirildi.")

        fig = px.line(plot_df, x=date_col, y=plot_cols, 
                     title="Biznes dinamikasi (Optimallashtirilgan)",
                     template="plotly_dark") # Dizaynni chiroyli qilish uchun
        
        fig.update_xaxes(rangeslider_visible=True)
        st.plotly_chart(fig, use_container_width=True)

    # 5. BASHORAT VA ANIQ TAVSIYALAR (Tuzatish 4 va 5)
    st.divider()
    st.subheader("💡 AI Strategik Maslahatlari")
    
    if sales_col:
        # AI Training (Simple)
        X = np.array(range(len(df))).reshape(-1, 1)
        y_sales = df[sales_col].values
        model = LinearRegression().fit(X, y_sales)
        sales_pred = model.predict([[len(df)]])[0]
        sales_growth = ((sales_pred - df[sales_col].mean()) / df[sales_col].mean()) * 100

        c_a, c_b = st.columns(2)
        with c_a:
            st.info(f"🔮 **Keyingi davr uchun bashorat:** {sales_pred:,.0f}")
            st.write(f"Joriy holatda savdo yo'nalishi **{'o\'sish' if sales_growth > 0 else 'pasayish'}** tomon ketyapti.")

        with c_b:
            st.subheader("🎯 Nima qilish kerak?")
            # TADBIRKOR UCHUN ANIQ TAVSIYALAR
            if sales_growth > 5:
                st.success(f"✅ **Savdo o'smoqda:** Mijozlar talabi yuqori. Tavsiya: Tovar zaxiralarini {abs(sales_growth):.0f}% ga oshiring va marketingni kuchaytiring.")
            elif sales_growth < -5:
                st.warning(f"⚠️ **Diqqat, savdo pasaymoqda:** Mijozlarni yo'qotish xavfi bor. Tavsiya: Narxlar strategiyasini qayta ko'rib chiqing yoki aksiyalar tashkil qiling.")
            
            if expense_col:
                expense_ratio = (total_expenses / total_sales) * 100 if total_sales > 0 else 0
                if expense_ratio > 80:
                    st.error(f"❗ **Xarajatlar juda yuqori:** Har bir so'm tushumning {expense_ratio:.0f}% qismi xarajatga ketyapti. Tavsiya: Keraksiz operatsion chiqimlarni zudlik bilan qisqartiring.")
                elif expense_ratio < 40:
                    st.success(f"💎 **Yuqori rentabellik:** Xarajatlar nazoratda. Tavsiya: Foydani biznesni kengaytirishga yoki yangi filiallar ochishga yo'naltiring.")

else:
    st.info("Boshlash uchun biznes ma'lumotlarini yuklang. AI tizimi ularni avtomatik tahlil qilib, sizga tavsiyalar beradi.")
