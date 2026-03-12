import streamlit as st
import main
import multi_sig
import docx
import upload_file
from coincurve import PublicKey

st.set_page_config(
    page_title="Xác thực chữ ký",
    page_icon="✅",
    layout="wide"
)

if "pub_key_1" not in st.session_state:
    st.session_state.pub_key_1 = []


st.markdown("<h3 style='text-align: center; color: black;'>Chào mừng đến với chương trình kiểm tra chữ ký số nhóm</h3>", unsafe_allow_html=True)

def upload_file_sign():
    ul = st.file_uploader("Chọn file chứa chữ ký", accept_multiple_files=False)
    if ul:
        data = ul.getvalue()
        data = data.decode()
        return data

def upload_file_lst_pub_key():
    ul = st.file_uploader("Chọn file chứa danh sách khoá công khai", accept_multiple_files=False)
    if ul:
        data = ul.getvalue()
        data = data.decode()
        return data

def Get_r_s(data):
    lst_data = []
    temp = 0
    try:
        for i in range(len(data)):
            if data[i] == "\n":
                lst_data.append(data[temp:i])
                temp = i + 1
        lst_data.append(data[temp:])
        return lst_data
    except:
        return None, None

def get_pub_key(data):
    if data == None: 
        st.info("Vui lòng chọn file có chứa danh sách khoá công khai")
        return
    else:
        st.session_state.pub_key_1 = []
        parts = data.strip().split("\n")
        for i in range(len(parts)):
            st.session_state.pub_key_1.append(PublicKey(bytes.fromhex(parts[i])))
        return st.session_state.pub_key_1


choice = st.radio(label="Chọn phương thức", options=["Lấy thông điệp từ file", "Nhập thông điệp từ bàn phím"], index=0, horizontal=True)
if choice == "Nhập thông điệp từ bàn phím":
    msg =  st.text_input(label="Hãy nhập thông điệp vào đây")
elif choice == "Lấy thông điệp từ file":
    msg = upload_file.upload_file()

lst = []
r, s = Get_r_s(upload_file_sign())
lst = get_pub_key(upload_file_lst_pub_key())
if r and s and lst:
    # st.write("R, s: ", r, s)
    valid = main.verify_signature(msg, int(r), int(s), lst)
    st.write("Danh sách khóa cong khai: ", lst)
    st.write("R, s: ", r, s)
    st.write(msg)
    if valid == True: st.success(f"Xác thực chữ ký thành công")
    else: st.error(f"Xác thực chữ ký thất bại")
else:
    st.warning("Vui lòng thực hiện các yêu cầu trên")

# r = st.text_input(label="Hãy nhập r vào đây")
# if r.isdigit() and int(r) > 0:
#     st.write(r)
#     print(type(r))
# s = st.text_input(label="Hãy nhập s vào đây")
# st.write(r, s)
# print(type(r), type(s))
# so_lg = multi_sig.st.session_state.solg
# st.write(so_lg)

# u = multi_sig.st.session_state.user
# st.write(u)

# st.write(main.verify_signature(msg, int(r), int(s), u))



