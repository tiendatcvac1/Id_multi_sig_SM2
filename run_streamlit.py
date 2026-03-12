import streamlit as st

# st.set_page_config(
#     page_title="Demo Streamlit",
#     page_icon=":tada:",
#     layout="wide"
# )



pg = st.navigation([
    st.Page("main.py", title="Trang chủ"),
    st.Page("key_gen.py", title="Thực hiện sinh khoá"),
    st.Page("multi_sig.py", title="Thực hiện ký số nhóm"),
    st.Page("verify.py", title="Thực hiện kiểm tra chữ ký số nhóm")
])

pg.run()