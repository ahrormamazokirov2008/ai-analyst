import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Raqamli Tahlilchi", layout="wide")
st.title("📊 KOB uchun AI 'Raqamli Tahlilchi'")

# Test ma'lumotlari
data = {
    'Sana': pd.date_range(start='2024-01-01', periods=12, freq='ME'),
    'Savdo': [120, 150, 140, 180, 210, 195, 230, 260, 245, 290, 310, 340],
    'Xarajat': [80, 95, 90, 110, 130, 125, 140, 155, 150, 170, 185, 200]
}
df = pd.DataFrame(data)

st.subheader("📈 Savdo va Xarajatlar dinamikasi")
fig = px.line(df, x='Sana', y=['Savdo', 'Xarajat'], markers=True)
st.plotly_chart(fig, use_container_width=True)

# AI Bashorati
X = np.array(range(len(df))).reshape(-1, 1)
y = df['Savdo'].values
model = LinearRegression().fit(X, y)
bashorat = model.predict([[len(df)]])[0]

st.success(f"🤖 AI Bashorati: Kelasi oyda kutilayotgan savdo: {bashorat:.1f} mln so'm")
