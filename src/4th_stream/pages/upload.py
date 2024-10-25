import streamlit as st
from mtcnn import MTCNN
from PIL import Image
from requests.exceptions import ConnectionError
import numpy as np
import requests
import os
import io

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


def find_face(img):
    detector = MTCNN()

    img_np = np.array(img)
    faces = detector.detect_faces(img_np)
    return faces


def upload_img(img, name):
    ip = os.getenv("EC2_IP", "localhost")
    url = f"http://{ip}:3003/uploadfile"

    img_bytes = io.BytesIO()
    img.save(img_bytes, format="JPEG")
    img_bytes.seek(0)

    p_result = 1

    params = {
        "file": (name + ".jpeg", img_bytes, "image/jpeg"),
        "prediction_result": (None, p_result),
    }
    r = requests.post(url, files=params)
    return r


st.title("Upload Picture")
pic = st.file_uploader(
    "img", type=["png", "jpg", "jpeg", "webp"], label_visibility="hidden"
)

if pic is not None:
    image = Image.open(pic).convert("RGB")
    faces = find_face(image)

    if len(faces) == 0:
        st.error("No faces detected.")
    else:
        for i, face in enumerate(faces):
            x, y, w, h = face["box"]

            face_crop = image.crop((x - 15, y - 15, x + w + 15, y + h + 15))
            st.image(face_crop, width=100)

            file_name = f"{pic.name.split('.')[-2]}({i+1})"

            try:
                r = upload_img(face_crop, file_name)
                if r.status_code == 200:
                    st.success("이미지 업로드 성공!")
                else:
                    st.warning("이미지 업로드에 실패하였습니다.")
            except ConnectionError:
                st.warning("연결 오류 발생 : 이미지 업로드에 실패하였습니다.")
            except Exception as e:
                st.error(f"알 수 없는 오류 발생: {e}")
