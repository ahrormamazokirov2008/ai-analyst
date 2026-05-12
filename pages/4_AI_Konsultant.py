import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Konsultant", layout="wide", page_icon="🤖")

st.title("🤖 AI Ma'lumotlar Konsultanti")

# 1. Xotiradan ma'lumotni tekshirish
if 'data' not in st.session_state:
    st.warning("⚠️ Diqqat! Chatbot ishlashi uchun avval asosiy sahifada (Main Page) biron bir CSV yoki Excel faylni yuklashingiz kerak.")
    st.info("Asosiy sahifaga qaytib, faylni yuklang va so'ngra bu yerga qayting.")
else:
    df = st.session_state['data']
    
    st.success("✅ Ma'lumotlar bilan bog'lanish o'rnatildi. Chatbot tayyor!")

    # 2. Chat tarixini saqlash (sahifa yangilanganda o'chib ketmasligi uchun)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Chat tarixini ko'rsatish
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 3. Savol kiritish maydoni
    if prompt := st.chat_input("Ma'lumotlar haqida biron narsa so'rang..."):
        # Foydalanuvchi savolini saqlash va ko'rsatish
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI javobini generatsiya qilish
        with st.chat_message("assistant"):
            query = prompt.lower()
            response = ""

            # ANALITIK MANTIQ (Simple Data Intelligence)
            if "salom" in query or "assalom" in query:
                response = "Assalomu alaykum! Men sizning raqamli yordamchingizman. Yuklangan ma'lumotlar asosida qanday savolingiz bor?"
            
            elif "ustun" in query or "column" in query:
                cols = ", ".join(df.columns.tolist())
                response = f"Jadvalingizda quyidagi ustunlar mavjud: **{cols}**."
                
            elif "nechta" in query or "qator" in query:
                response = f"Ushbu jadvalda jami **{len(df)}** ta qator ma'lumot mavjud."

            elif "eng katta" in query or "max" in query:
                numeric_df = df.select_dtypes(include=['number'])
                if not numeric_df.empty:
                    col = numeric_df.columns[0]
                    max_val = df[col].max()
                    response = f"Ma'lumotlardagi eng yuqori ko'rsatkich (**{col}** bo'yicha): **{max_val:,.0f}**."
                else:
                    response = "Hisoblash uchun raqamli ustun topilmadi."

            elif "o'rtacha" in query or "average" in query:
                numeric_df = df.select_dtypes(include=['number'])
                if not numeric_df.empty:
                    col = numeric_df.columns[0]
                    avg_val = df[col].mean()
                    response = f"Jadval bo'yicha o'rtacha ko'rsatkich: **{avg_val:,.0f}**."
                else:
                    response = "Raqamli ma'lumotlar mavjud emas."

            else:
                response = """Hozircha men oddiy tahliliy savollarga javob bera olaman. 
                Kelajakda ushbu modulga **Sovereign AI** (masalan, Llama 3) modelini ulab, 
                ma'lumotlarni yanada chuqurroq va insoniy tilda tahlil qilishni rejalashtirganman."""

            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
