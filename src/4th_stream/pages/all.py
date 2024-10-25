import streamlit as st
import pandas as pd
import numpy as np
import requests
import os

st.title("Result")

age_mapping = {
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

ip = os.getenv("EC2_IP", "172.17.0.1")


def load_data():
    url = f"http://{ip}:3003/all"
    r = requests.get(url).json()
    return r


data = load_data()
df = pd.DataFrame(data)

for i in range(len(df)):
    p = df["predictionResult"][i]
    r = df["answer"][i]

    if p is not None and r is not None:
        with st.container(border=True):
            img, info = st.columns([1, 3])
            img.image(df["filePath"][i], width=100)
            p_age = age_mapping[int(p)]
            r_age = age_mapping[int(r)]
            info.markdown("")
            info.markdown("")
            info.markdown(
                f"사진 속 사람의 예상 나이대는 :blue-background[**{p_age}**] 입니다."
            )
            info.markdown(
                f"사진 속 사람의 실제 나이대는 :red-background[**{r_age}**] 입니다."
            )
