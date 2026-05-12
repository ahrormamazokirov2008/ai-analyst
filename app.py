import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression
st.set_page_config(page_title="AI Business Intelligence Pro", layout="wide", page_icon="📊")

# TILLAR LUG'ATI
translations = {
    "O'zbekcha": {
        "title": "🚀 Professional Biznes Analitika",
        "sidebar_head": "📂 Ma'lumotlar",
        "upload_label": "CSV yoki Excel faylni tanlang",
        "sales_label": "Savdo (Tushum) ustunini tanlang:",
        "exp_label": "Xarajat (Chiqim) ustunini tanlang:",
        "no_data": "Boshlash uchun biznes ma'lumotlarini yuklang."
    },
    "English": {
        "title": "🚀 Professional Business Analytics",
        "sidebar_head": "📂 Data Management",
        "upload_label": "Choose CSV or Excel file",
        "sales_label": "Select Sales Column:",
        "exp_label": "Select Expense Column:",
        "no_data": "Please upload data to start analysis."
    },
    "Русский": {
        "title": "🚀 Профессиональная Бизнес Аналитика",
        "sidebar_head": "📂 Данные",
        "upload_label": "Выберите CSV или Excel файл",
        "sales_label": "Выберите колонку продаж:",
        "exp_label": "Выберите колонку расходов:",
        "no_data": "Загрузите данные для начала анализа."
    }
}
# 1. SIDEBARDA TILNI TANLASH
with st.sidebar:
    lang = st.selectbox("🌐 Til / Language", ["O'zbekcha", "English", "Русский"])
    t = translations[lang] # Tanlangan tilni yuklash
    
    st.divider()
    st.header(t["sidebar_head"])
    uploaded_file = st.file_uploader(t["upload_label"], type=['csv', 'xlsx'])

st.title("🚀 Professional Biznes Analitika va Bashorat")

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

    st.sidebar.divider()
    # Tanlangan tilga mos sarlavha (t["sales_label"])
    sales_col = st.sidebar.selectbox(t["sales_label"], df.columns.tolist(), index=df.columns.tolist().index(sales_col) if sales_col in df.columns else 0)
    
    # Tanlangan tilga mos sarlavha (t["exp_label"])
    expense_col = st.sidebar.selectbox(t["exp_label"], ["Mavjud emas"] + df.columns.tolist())

    if date_col:
        df[date_col] = pd.to_datetime(df[date_col])
        df = df.sort_values(date_col)
        # Ma'lumot oralig'ini aniqlash (Kunlik, Haftalik, Oylik)
        days_diff = (df[date_col].max() - df[date_col].min()).days
        data_points = len(df)
        time_unit = "kunlik" if days_diff / data_points < 2 else "haftalik" if days_diff / data_points < 10 else "oylik"
        
    # 2. METRIKALAR (SAVDO VA XARAJAT ALOHIDA)


   st.subheader(t["fin_status"])

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
        
        fig.update_xaxes(rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

    # 5. AI Strategik Maslahatlari
    st.divider()
    st.subheader("🤖 AI Strategik Maslahatlari")

    if sales_col:
        # AI Modelini tayyorlash va bashorat
        X = np.array(range(len(df))).reshape(-1, 1)
        y_sales = df[sales_col].values
        model = LinearRegression().fit(X, y_sales)
        sales_pred = model.predict([[len(df)]])[0]
        
        # O'rtacha savdoni hisoblash
        avg_sales = df[sales_col].mean()
        
        # O'sish sur'atini hisoblash (Ziddiyatni oldini olish uchun)
        sales_growth = ((sales_pred - avg_sales) / avg_sales) * 100 if avg_sales != 0 else 0

        # Bir xil mantiqiy holatlarni belgilash
        if sales_growth > 3:
            holat_matni = "o'sish"
            holat_rangi = "success"
            tavsiya = "✅ **Savdo o'smoqda:** Talab yuqori. Tavsiya: Tovar zaxiralarini oshiring va marketingni kuchaytiring."
        elif sales_growth < -3:
            holat_matni = "pasayish"
            holat_rangi = "warning"
            tavsiya = "⚠️ **Savdo pasaymoqda:** Mijozlar kamayishi kutilmoqda. Tavsiya: Narxlar strategiyasini qayta ko'rib chiqing yoki aksiyalar qiling."
        else:
            holat_matni = "barqaror"
            holat_rangi = "info"
            tavsiya = "ℹ️ **Barqaror holat:** Bozorda keskin o'zgarish kutilmayapti. Xizmat sifatini oshirishga va mijozlar sodiqligiga e'tibor bering."

        # Ekranga chiqarish (Metrikalar va Tavsiyalar)
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.info(f"🔮 **Keyingi davr uchun bashorat:** {sales_pred:,.0f}")
            st.write(f"Joriy holatda savdo yo'nalishi **{holat_matni}** tomon ketyapti.")

        with col_b:
            st.write(f"### {t['action_plan']}")
            if holat_rangi == "success": st.success(tavsiya)
            elif holat_rangi == "warning": st.warning(tavsiya)
            else: st.info(tavsiya)
        
        # 6. Xarajatlar tahlili (agar tanlangan bo'lsa)
        if expense_col != "Mavjud emas":
            st.divider()
            total_sales = df[sales_col].sum()
            total_expenses = df[expense_col].sum()
            expense_ratio = (total_expenses / total_sales) * 100 if total_sales > 0 else 0
            
            if expense_ratio > 80:
                st.error(f"❗ **Xarajatlar juda yuqori:** Tushumning {expense_ratio:.1f}% qismi xarajatga ketyapti. Tejamkorlik choralarini ko'ring.")
            elif expense_ratio < 40:
                st.success(f"💎 **Yuqori rentabellik:** Xarajatlar nazoratda ({expense_ratio:.1f}%). Biznesni kengaytirish haqida o'ylash mumkin.")
