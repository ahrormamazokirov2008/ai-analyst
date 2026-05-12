# ... (avvalgi kodlar)

# 3. GRAFIK BO'LIMI
st.divider()
st.subheader("📈 Dinamika Tahlili")

if date_col:
    # Katta ma'lumotlar uchun qo'shimcha filtr
    if len(df) > 30:
        st.write("💡 *Ma'lumotlar ko'p bo'lgani uchun tahlilni osonlashtirishni tanlang:*")
        view_type = st.radio("Ko'rinish turi:", ["Asl holati (Kunlik)", "Haftalik trend (Tekislangan)", "Oylik xulosa"], horizontal=True)
        
        plot_df = df.copy()
        
        if view_type == "Haftalik trend (Tekislangan)":
            # 7 kunlik siljuvchi o'rtacha hisoblash
            plot_df[sales_col] = plot_df[sales_col].rolling(window=7).mean()
            if expense_col != "Mavjud emas":
                plot_df[expense_col] = plot_df[expense_col].rolling(window=7).mean()
            st.info("Grafik 7 kunlik o'rtacha ko'rsatkichlar asosida tekislandi.")
            
        elif view_type == "Oylik xulosa":
            # Oylik guruhlash
            plot_df = plot_df.resample('M', on=date_col).sum().reset_index()
            st.info("Ma'lumotlar oylar bo'yicha umumlashtirildi.")
    else:
        plot_df = df

    # Grafik chizish
    fig = px.line(plot_df, x=date_col, y=plot_cols, 
                 title=f"Biznes dinamikasi ({'Tekislangan' if len(df)>30 else ''})",
                 markers=True if len(plot_df) < 50 else False) # Nuqtalarni faqat ma'lumot kam bo'lsa chiqaramiz

    # Katta ma'lumotlar uchun "Surgich" (Range Slider) qo'shish
    fig.update_xaxes(rangeslider_visible=True)
    
    st.plotly_chart(fig, use_container_width=True)

    # 4. Katta ma'lumotlar uchun jadval xulosasi (Top 5 kun/oy)
    with st.expander("📑 Eng yuqori ko'rsatkichlar jadvalini ko'rish"):
        top_data = df.sort_values(by=sales_col, ascending=False).head(10)
        st.table(top_data[[date_col, sales_col]])

# ... (qolgan AI tavsiya qismlari)
