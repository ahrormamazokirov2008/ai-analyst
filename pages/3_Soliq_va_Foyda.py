import streamlit as st

st.set_page_config(page_title="Soliq va Foyda", layout="wide")

st.title("💰 Soliq va Sof Foyda Hisoblagichi (O'zbekiston)")

st.info("Ushbu bo'lim biznesingizning barcha soliqlardan keyingi real foydasini hisoblaydi.")

# 1. Ma'lumotlarni kiritish
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Moliyaviy ko'rsatkichlar")
    revenue = st.number_input("Jami Savdo (tushum):", min_value=0.0, step=1000000.0, value=50000000.0)
    expenses = st.number_input("Jami Xarajatlar (ijara, ish haqi, xomashyo):", min_value=0.0, step=1000000.0, value=30000000.0)

with col2:
    st.subheader("📑 Soliq rejimi")
    tax_type = st.selectbox("Soliq turini tanlang:", 
                             ["Aylanmadan olinadigan soliq (4%)", "Umumiy rejim (QQS 12% + Foyda solig'i 15%)"])

# 2. Hisob-kitob mantig'i
if tax_type == "Aylanmadan olinadigan soliq (4%)":
    tax_amount = revenue * 0.04
    net_profit = revenue - expenses - tax_amount
else:
    # Umumiy rejim (soddalashtirilgan hisob)
    vat = revenue * 0.12
    profit_before_tax = revenue - expenses - vat
    profit_tax = max(0, profit_before_tax * 0.15)
    tax_amount = vat + profit_tax
    net_profit = revenue - expenses - tax_amount

# 3. Natijalarni ko'rsatish
st.divider()
c1, c2, c3 = st.columns(3)

c1.metric("To'lanadigan jami soliq", f"{tax_amount:,.0f}")
c2.metric("Sof Foyda (Soliqdan keyin)", f"{net_profit:,.0f}", delta=f"{(net_profit/revenue*100):.1f}% rentabellik")
c3.metric("Xarajatlar ulushi", f"{(expenses/revenue*100):.1f}%")

# 4. AI Strategik tavsiyasi
st.subheader("🤖 AI Moliya Maslahatchisi")

if net_profit <= 0:
    st.error("⚠️ Diqqat! Sizning biznesingiz hozirda zarar bilan ishlayapti. Xarajatlarni zudlik bilan tahlil qiling.")
elif net_profit / revenue < 0.1:
    st.warning("⚠️ Rentabellik juda past (10% dan kam). Narxlarni oshirish yoki xarajatlarni kamaytirish choralarini ko'ring.")
else:
    st.success("✅ Tabriklaymiz! Biznesingiz barqaror foyda keltirmoqda. Foydaning bir qismini investitsiyaga yo'naltirishingiz mumkin.")

if tax_type == "Aylanmadan olinadigan soliq (4%)" and (expenses/revenue) > 0.7:
    st.info("💡 Maslahat: Xarajatlaringiz yuqori ekan. Ehtimol, QQS rejimiga o'tish orqali soliqlarni optimallashtirishingiz mumkin.")
