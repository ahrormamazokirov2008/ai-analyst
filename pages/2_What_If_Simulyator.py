import streamlit as st
import pandas as pd

st.set_page_config(page_title="Strategik Simulyator", layout="wide")

st.title("🧪 What-If: Strategik Bashorat Simulyatori")

st.markdown("""
Ushbu bo'limda siz biznesingizdagi o'zgarishlar foydaga qanday ta'sir qilishini hisoblashingiz mumkin. 
Hech qanday kod yozmasdan, faqat suruvchi tugmalar (sliders) orqali kelajakni bashorat qiling.
""")

# 1. Boshlang'ich ma'lumotlar
st.sidebar.header("📊 Joriy holat ko'rsatkichlari")
current_revenue = st.sidebar.number_input("Oylik o'rtacha tushum:", min_value=0, value=50_000_000, step=1_000_000)
current_expense = st.sidebar.number_input("Oylik o'rtacha xarajat:", min_value=0, value=35_000_000, step=1_000_000)

current_profit = current_revenue - current_expense
current_margin = (current_profit / current_revenue * 100) if current_revenue > 0 else 0

# 2. Simulyatsiya sozlamalari
st.subheader("🛠 O'zgarishlarni kiriting")
col1, col2 = st.columns(2)

with col1:
    st.write("### 📈 Savdo")
    sales_growth = st.slider("Savdo o'sishi kutilmasi (%)", -50, 100, 10)
    st.caption("Masalan, yangi filial ochish yoki reklama hisobiga.")

with col2:
    st.write("### 📉 Xarajat")
    expense_change = st.slider("Xarajatlarni qisqartirish/oshish (%)", -50, 50, -5)
    st.caption("Masalan, xomashyo narxi tushishi yoki xodimlarni qisqartirish.")

# 3. Hisob-kitob
new_revenue = current_revenue * (1 + sales_growth / 100)
new_expense = current_expense * (1 + expense_change / 100)
new_profit = new_revenue - new_expense
new_margin = (new_profit / new_revenue * 100) if new_revenue > 0 else 0

profit_diff = new_profit - current_profit

# 4. Natijalarni ko'rsatish
st.divider()
st.subheader("🎯 Simulyatsiya natijasi")

res1, res2, res3 = st.columns(3)

res1.metric("Yangi kutilayotgan foyda", f"{new_profit:,.0f}", f"{profit_diff:,.0f} farq")
res2.metric("Yangi rentabellik", f"{new_margin:.1f}%", f"{(new_margin - current_margin):.1f}%")
res3.metric("Yangi oylik tushum", f"{new_revenue:,.0f}")

# 5. AI maslahati
st.divider()
st.subheader("🤖 AI Strategik tahlili")

if new_profit > current_profit:
    st.success(f"✅ Ushbu strategiya sizga oyiga qo'shimcha **{profit_diff:,.0f}** foyda keltiradi. Uni amalga oshirish tavsiya etiladi!")
    if sales_growth > 20:
        st.info("💡 Eslatma: Savdoning keskin o'sishi xizmat ko'rsatish sifatini tushirib yubormasligini ta'minlang.")
elif new_profit < current_profit:
    st.error("⚠️ Diqqat! Bu o'zgarishlar biznesni zararga olib kelishi yoki foydani kamaytirishi mumkin. Strategiyani qayta ko'rib chiqing.")
else:
    st.warning("🔄 O'zgarishlar foydaga sezilarli ta'sir qilmadi. Resurslarni tejash maqsadga muvofiqroq bo'lishi mumkin.")
