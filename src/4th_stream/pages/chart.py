import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import os

age_band_mapping = {
    0: "0-2",
    1: "3-9",
    2: "10-19",
    3: "20-29",
    4: "30-39",
    5: "40-49",
    6: "50-59",
    7: "60-69",
    8: "70+",
}

st.title("Chart")


def load_data(path):
    ip = os.getenv("EC2_IP", "localhost")
    url = f"http://{ip}:8022/{path}"
    r = requests.get(url).json()
    return r


data_agg = load_data("agg")
df = pd.DataFrame(data_agg)

total_correct = df["correct"].sum()
total_incorrect = df["total_count"].sum() - total_correct

labels = ["Correct", "Incorrect"]
sizes = [total_correct, total_incorrect]
explode = (0.1, 0)

fig, ax = plt.subplots(figsize=(4, 4))
ax.pie(
    sizes, explode=explode, labels=labels, autopct="%1.1f%%", shadow=True, startangle=90
)
ax.axis("equal")

with st.container():
    st.subheader("전체 데이터 예측 정확도 통계", divider="gray")
    st.pyplot(fig)

age_band_order = list(age_band_mapping.values())
df["accuracy"] = df["correct"] / df["total_count"]
df["age_band"] = df["answer"].map(age_band_mapping)
df["age_band"] = pd.Categorical(df["age_band"], categories=age_band_order, ordered=True)
df = df.sort_values(by="age_band")
chart_data = df[["age_band", "accuracy"]].set_index("age_band")

with st.container():
    st.subheader("나이대별 예측 정확도 통계", divider="gray")
    st.bar_chart(chart_data, x_label="Age Band", y_label="Prediction Accuracy")

data_all = load_data("all")
# null값 제외
df_a = pd.DataFrame(data_all).dropna(subset=["prediction_result", "answer"])

df_a["error"] = abs(df_a["prediction_result"].astype(int) - df_a["answer"].astype(int))
error_counts = df_a["error"].value_counts().reindex(range(0, 9), fill_value=0)
error_counts = error_counts[error_counts > 0]

with st.container():
    st.subheader("오차율 분석 통계", divider="gray")
    st.bar_chart(error_counts, x_label="Error", y_label="Count")
