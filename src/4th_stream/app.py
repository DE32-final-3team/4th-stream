import streamlit as st

page_u1 = st.Page("pages/upload.py", title="Upload Image", icon="🖼️")
page_u2 = st.Page("pages/camera.py", title="Camera", icon="📸")
page_u3 = st.Page("pages/all.py", title="Result", icon="👓")
page_M1 = st.Page("pages/admin.py", title="관리자 페이지", icon="⚙️")

pg = st.navigation(
    {
        "User": [page_u1, page_u2, page_u3],
        "Manage": [page_M1],
    }
)

pg.run()
