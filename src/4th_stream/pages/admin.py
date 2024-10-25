import streamlit as st
import pandas as pd
import numpy as np
import requests
import os

PASSWORD = os.getenv("PWD", "0000")
ip = os.getenv("EC2_IP", "localhost")

age_mapping = {
    0: "0-2 years",
    1: "3-9 years",
    2: "10-19 years",
    3: "20-29 years",
    4: "30-39 years",
    5: "40-49 years",
    6: "50-59 years",
    7: "60-69 years",
    8: "70+ years",
}

reversed_age_mapping = {v: k for k, v in age_mapping.items()}

# 세션 상태를 통해 로그인 여부 관리
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


def load_data():
    url = f"http://{ip}:8022/all"
    r = requests.get(url).json()
    return r


def login():
    """로그인 처리 함수"""
    password = st.text_input("비밀번호를 입력하세요", type="password")
    if st.button("로그인"):
        if password == PASSWORD:
            st.session_state.logged_in = True
            st.success("로그인 성공!")
            st.rerun()
        else:
            st.error("비밀번호가 잘못되었습니다.")


def admin_page():
    st.title("Admin Dashboard")

    data = load_data()
    df = pd.DataFrame(data)

    for i in range(len(df)):
        p = df["prediction_result"][i]
        r = df["answer"][i]

        p_age = p if pd.isnull(p) else age_mapping[int(p)]
        r_age = r if pd.isnull(r) else age_mapping[int(r)]

        with st.container(border=True):
            img, info = st.columns([1, 3])
            img.image(df["file_path"][i], width=100)

            with info.container():
                h1, h2 = st.columns([3, 1])
                h1.markdown(f"#### {df['num'][i]}. {df['origin_name'][i]}")
                if h2.button("Delete", key=f"delete{i}", type="primary"):
                    url = f"http://{ip}:8022/delete?num={df['num'][i]}"
                    r = requests.get(url)
                    st.rerun()

                r1, r2 = st.columns([1, 1])
                r1.markdown(f"**예측 결과** : {p_age}")
                r2.markdown(f"**실제 정답** : {r_age}")

                label = st.selectbox(
                    "정답 업데이트", options=age_mapping.values(), key=f"{i}_label"
                )
                if st.button("Update", key=f"updafe{i}"):
                    url = f"http://{ip}:8022/up?num={df['num'][i]}&label={reversed_age_mapping[label]}"
                    r = requests.get(url)

                    if r.status_code == 200:
                        st.rerun()


# 로그인 여부에 따라 화면을 제어
if not st.session_state.logged_in:
    st.title("관리자 페이지 접근")
    login()
else:
    admin_page()
