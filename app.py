# ... (kodning yuqori qismi o'zgarishsiz qoladi)

        # YANGI ANALITIKA MODULLARI
        st.divider()
        st.subheader("🧐 Biznesning Chuqur Tahlili")
        
        # 1. O'sish sur'atini hisoblash
        df['O\'sish_%'] = df['Savdo'].pct_change() * 100
        oxirgi_osish = df['O\'sish_%'].iloc[-1]
        
        # 2. Xarajat ulushi
        xarajat_ulushi = (df['Xarajat'].sum() / df['Savdo'].sum()) * 100
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.info(f"📈 **O'sish sur'ati:** Oxirgi oyda savdo {oxirgi_osish:.1f}% ga o'zgardi.")
        with col_b:
            st.info(f"💸 **Xarajat ulushi:** Har 100 so'm savdoning {xarajat_ulushi:.1f} so'mi xarajatga ketyapti.")

        # 3. AI Strategik Tavsiyasi
        st.subheader("💡 AI Strategik Tavsiyalari")
        if oxirgi_osish > 0 and xarajat_ulushi < 70:
            st.success("✅ Biznesingiz ideal holatda! Hozirgi strategiyani davom ettiring va ko'proq investitsiya kiriting.")
        elif xarajat_ulushi > 80:
            st.warning("⚠️ Diqqat! Xarajatlar juda yuqori. Operatsion samaradorlikni oshirish yoki keraksiz xarajatlarni qisqartirish lozim.")
        else:
            st.info("ℹ️ Stabil holat. Savdoni oshirish uchun yangi marketing kanallarini sinab ko'ring.")

# ... (kodning qolgan qismi)        fig = px.line(df, x='Sana', y=['Savdo', 'Xarajat'], title="📈 Biznes Dinamikasi", markers=True)
        st.plotly_chart(fig, use_container_width=True)

        # AI Bashorat
        X = np.array(range(len(df))).reshape(-1, 1)
        y = df['Savdo'].values
        model = LinearRegression().fit(X, y)
        bashorat = model.predict([[len(df)]])[0]
        
        st.success(f"🤖 **AI Bashorati:** Kelasi oyda kutilayotgan savdo: **{bashorat:.1f} mln so'm**")

        # PDF Yaratish funksiyasi
        def create_pdf_file(df_report, pred):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, txt="AI Raqamli Tahlilchi Hisoboti", ln=True, align='C')
            pdf.ln(10)
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Umumiy Savdo: {df_report['Savdo'].sum()} mln so'm", ln=True)
            pdf.cell(200, 10, txt=f"Umumiy Foyda: {df_report['Foyda'].sum()} mln so'm", ln=True)
            pdf.cell(200, 10, txt=f"AI Bashorati (kelasi oy): {pred:.1f} mln so'm", ln=True)
            pdf.ln(10)
            pdf.cell(200, 10, txt="Oxirgi ko'rsatkichlar:", ln=True)
            pdf.set_font("Arial", size=10)
            for i in range(len(df_report)):
                txt_row = f"{df_report['Sana'].dt.date.iloc[i]} | Savdo: {df_report['Savdo'].iloc[i]} | Xarajat: {df_report['Xarajat'].iloc[i]}"
                pdf.cell(200, 10, txt=txt_row, ln=True)
            return pdf.output(dest='S').encode('latin-1')

        st.divider()
        pdf_bytes = create_pdf_file(df, bashorat)
        st.download_button(label="📥 PDF Hisobotni yuklab olish",
                           data=pdf_bytes,
                           file_name="biznes_hisobot.pdf",
                           mime="application/pdf")

    except Exception as e:
        st.error(f"Xatolik yuz berdi: {e}")
else:
    st.info("Iltimos, chap tarafdagi menyu orqali Excel faylingizni yuklang.")
