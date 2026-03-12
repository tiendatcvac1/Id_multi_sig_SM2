import streamlit as st
import main

if "solg" not in st.session_state:
    st.session_state.solg = 0

if "lst_user" not in st.session_state:
    st.session_state.lst_user = []

if "temp_lst" not in st.session_state:
    st.session_state.temp_lst = []

if "user" not in st.session_state:
    st.session_state.user = []    

st.set_page_config(
    page_title="Sinh khoá",
    page_icon="✍️",
    layout="wide"
)

st.markdown("<h3 style='text-align: center; color: black;'>Chào mừng đến với chương trình sinh khoá</h3>", unsafe_allow_html=True)
st.session_state.solg = st.number_input("Hãy nhập số lượng người tham gia ký", min_value=0, format="%d")

def handle_input():
    for i in range (st.session_state.solg):
        temp = st.text_input(f"Nhập thông tin của người dùng thứ {i + 1}",help="Thông tin có thể là số điện thoại hoặc số định danh của người tham gia ký")
        if temp.isdigit() and int(temp) > 0:
            st.session_state.temp_lst.append(temp)
        else:
            st.warning("Vui lòng nhập số điện thoại hoặc số định danh của người ký")

    st.session_state.temp_lst.reverse()
    st.session_state.lst_user = st.session_state.temp_lst[:int(st.session_state.solg)]
    st.session_state.lst_user.reverse()
    return st.session_state.lst_user

def handle_generate():
    d_m, P_m = main.master_keygen()
    st.session_state.user = main.key_server_generate_for_ids(d_m, P_m, handle_input())
    return st.session_state.user

def out_pub_priv_key():
    user = handle_generate()
    st.markdown("<h5 style='text-align: center; color: black;'>Thông tin khoá công khai của những người tham gia ký số nhóm:</h5>", unsafe_allow_html=True)
    for i in range(len(user)):
        f = open(f"User {i + 1}_public.key", "w")
        f.write(user[i]['pk_i'].format(compressed=False).hex())
        st.write(f"User {i + 1}: {user[i]['pk_i'].format(compressed=False).hex()}")
        f.close()
        f = open(f"User {i + 1}_public.key", "r")
        str_1 = f.read()
        f.close()
        f = open(f"User {i + 1}_private.key", "w")
        f.write(str(user[i]['sk_i']))
        f.close()
        f = open(f"User {i + 1}_private.key", "r")
        str_2 = f.read()   
        cl = st.columns(2)
        with cl[0]:
            st.download_button(label="Tải khoá công khai của người dùng về", data=str_1, file_name=f"User {i + 1}_public.key", mime="text/plain", on_click="ignore")
        with cl[1]:
            st.download_button(label="Tải khoá bí mật của người dùng về", data=str_2, file_name=f"User {i + 1}_private.key", mime="text/plain", on_click="ignore")



if __name__ == "__main__":
    # st.write(handle_input())
    # st.write("\n")
    # st.write(handle_generate())
    out_pub_priv_key()
    pass
