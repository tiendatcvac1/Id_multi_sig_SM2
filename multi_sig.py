import streamlit as st
import main
import upload_file
from coincurve import PublicKey

if "pub_key" not in st.session_state:
    st.session_state.pub_key = []

if "input_pub_key" not in st.session_state:
    st.session_state.input_pub_key = ""

if "priv_key" not in st.session_state:
    st.session_state.priv_key = []

if "lst_user" not in st.session_state:
    st.session_state.lst_user = []

if "solg" not in st.session_state:
    st.session_state.solg = 0

if "user" not in st.session_state: 
    st.session_state.user = []

if "data" not in st.session_state:
    st.session_state.lst_data = []

st.set_page_config(
    page_title="Ký số nhóm",
    page_icon="✍️",
    layout="wide"
)


# def handle_choice_method(msg):
#     choice = st.radio(label="Chọn phương thức", options=["Tự động lấy khoá công khai từ chương trình", "Nhập khoá công khai từ bàn phím"], index=None, horizontal=True)
#     if choice == "Nhập khoá công khai từ bàn phím":
#         st.session_state.input_pub_key = st.text_input(label="Hãy nhập khoá công khai")
#         button_column = st.columns(2)
#         with button_column[0]: 
#             if st.button(label="Thêm", on_click="ignore"):
#                 if st.session_state.input_pub_key.strip() != "":
#                     st.session_state.pub_key.append(st.session_state.input_pub_key)
#                 else:
#                     st.error("Vui lòng không để trống")
#         with button_column[1]:
#             if st.button(label="Xóa", icon_position="right"):
#                 if len(st.session_state.pub_key) > 0:
#                     st.session_state.pub_key.pop()
#                 else:
#                     st.error("Không có giá trị nào để xoá")
#         st.write(st.session_state.pub_key)
#     elif choice == "Tự động lấy khoá công khai từ chương trình":
#         st.session_state.solg = st.text_input(label="Nhập số lượng người tham gia ký")
#         button_column = st.columns(2)
#         if st.session_state.solg.isdigit() and int(st.session_state.solg) > 0:
#             with button_column[0]:
#                 if st.button(label="Thêm"):
#                     st.session_state.lst_user = []
#                 for i in range(int(st.session_state.solg)):
#                     st.session_state.lst_user.append(f"User {i + 1}")
#                 d_m, P_m = main.master_keygen()
#                 st.session_state.user = main.key_server_generate_for_ids(d_m, P_m, st.session_state.lst_user)
#                 for i in range(int(st.session_state.solg)):
#                     st.session_state.pub_key_1.append(st.session_state.user[i]["pk_i"].format(compressed=False).hex())
#                 r, s = main.group_sign(msg, st.session_state.user)
#             with button_column[1]:
#                 if st.button(label="Xóa", icon_position="right"):
#                     st.session_state.pub_key_1 = []
#                     r, s = None, None
#             st.markdown("<h5 style='text-align: center; color: black;'>Thông tin khoá công khai của từng người dùng trong nhóm:</h5>", unsafe_allow_html=True)
#             st.write(st.session_state.pub_key_1)
#             value_colunm = st.columns(2)
#             with value_colunm[0]:
#                 st.write("Giá trị của R:", r)
#             with value_colunm[1]:
#                 st.write("Giá trị của S:", s)
#             f = open("Chu_ky.sig", "w")
#             f.write(str(st.session_state.solg)+ "\n" + str(r) + "\n" + str(s))
#             f.close()
#             f = open("Chu_ky.sig", "r")
#             str_1 = f.read()
#             st.download_button(label="Tải xuống", data=str_1, file_name="Chu_ky.sig", mime="text/plain", on_click="ignore")
#         else:
#             st.error("Vui lòng nhập số người tham gia ký")
#     else:
#         st.write("Vui lòng chọn phương thức")
#         pass

def upload_file_key(name):
    if name == "pubkey":
        ul = st.file_uploader(
            "Chọn file chứa khoá công khai của từng người tham gia ký",
            accept_multiple_files=True
        )
    elif name == "privkey":
        ul = st.file_uploader(
            "Chọn file chúa khoá bí mật của từng người tham gia ký",
            accept_multiple_files=True
        )
    data_list = []
    if ul:
        for file in ul:
            data = file.getvalue()
            data = data.decode()
            data_list.append(data)
    return data_list

# def get_pub_priv(data):
#     parts = data.strip().split("\n")
#     if len(parts) >= 2:
#         pub = parts[0]
#         priv = parts[1]
#         st.session_state.pub_key.append(PublicKey(bytes.fromhex(pub)))
#         st.session_state.priv_key.append(int(priv))
#     return st.session_state.pub_key, st.session_state.priv_key

def get_pub_key(pub):
    st.session_state.pub_key.append(PublicKey(bytes.fromhex(pub)))
    return st.session_state.pub_key

def get_priv_key(priv):
    st.session_state.priv_key.append(int(priv))
    return st.session_state.priv_key

def handle_choice_method(msg):
    KT_1, KT_2 = False, False
    st.session_state.solg = st.number_input(label="Nhập số lượng người tham gia ký thông điệp", format="%d", min_value=1)
    if st.session_state.solg:
        files_data_pub = upload_file_key("pubkey")
        if files_data_pub:
            st.session_state.pub_key = []
            if len(files_data_pub) != st.session_state.solg:
                st.error(f"Bạn phải tải đúng {st.session_state.solg} file khóa. Hiện tại bạn tải {len(files_data_pub)} file.")
                return
            for data in files_data_pub:
                get_pub_key(data)
            st.success("Upload đúng số lượng khóa")
            KT_1 = True
            # st.write("Đây là khoá công khai của người dùng:", st.session_state.pub_key)
            # st.write("Đây là khoá bí mật của người dùng:", st.session_state.priv_key)
        files_data_priv = upload_file_key("privkey")
        if files_data_priv:
            st.session_state.priv_key = []
            if len(files_data_priv) != st.session_state.solg:
                st.error(f"Bạn phải tải đúng {st.session_state.solg} file khóa. Hiện tạiば tải {len(files_data_priv)} file.")
                return
            for data in files_data_priv:
                get_priv_key(data)
            st.success("Upload đúng số lượng khóa")
            KT_2 = True
        if KT_1 and KT_2:
            st.write("Đây là khoá công khai của người dùng:", st.session_state.pub_key)
            st.write("Đây là khoá bí mật của người dùng:", st.session_state.priv_key)
            r, s = main.group_sign(msg, st.session_state.solg, st.session_state.pub_key, st.session_state.priv_key)
            st.write("Giá trị R:", r)
            st.write("Giá trị S:", s)
            f = open("Chu_ky.sig", "w")
            f.write(str(r) + "\n" + str(s))
            f.close()
            f = open("Chu_ky.sig", "r")
            str_1 = f.read()
            f = open("Danh_sach_khoa_cong_khai.key", "w")
            for i in range(len(st.session_state.pub_key)):
                f.write(str(st.session_state.pub_key[i].format(compressed=False).hex())+"\n")
            f.close()
            f = open("Danh_sach_khoa_cong_khai.key", "r")
            str_2 = f.read()
            colunm = st.columns(2)
            with colunm[0]:
                st.download_button(label="Tải chữ ký nhóm về", data=str_1, file_name="Chu_ky.sig", mime="text/plain", on_click="ignore")
            with colunm[1]:
                st.download_button(label="Tải danh sách khoá công khai về", data=str_2, file_name="Danh_sach_khoa_cong_khai.key", mime="text/plain", on_click="ignore")
        else:
            st.warning("Vui lòng đọc kỹ")
            # print(type(st.session_state.pub_key[0]))
            # print(type(st.session_state.priv_key[0]))
            # st.write(msg, st.session_state.solg, st.session_state.pub_key, st.session_state.priv_key)
            # nếu muốn ký luôn
        # r, s = main.group_sign(msg, st.session_state.solg, st.session_state.pub_key, st.session_state.priv_key)
        # st.write("Giá trị R:", r)
        # st.write("Giá trị S:", s)
        # f = open("Chu_ky.sig", "w")
        # f.write(str(r) + "\n" + str(s))
        # f.close()
        # f = open("Chu_ky.sig", "r")
        # str_1 = f.read()
        # f = open("Danh_sach_khoa_cong_khai.key", "w")
        # for i in range(len(st.session_state.pub_key)):
        #     f.write(str(st.session_state.pub_key[i].format(compressed=False).hex())+"\n")
        # f.close()
        # f = open("Danh_sach_khoa_cong_khai.key", "r")
        # str_2 = f.read()
        # colunm = st.columns(2)
        # with colunm[0]:
        #     st.download_button(label="Tải chữ ký nhóm về", data=str_1, file_name="Chu_ky.sig", mime="text/plain", on_click="ignore")
        # with colunm[1]:
        #     st.download_button(label="Tải danh sách khoá công khai về", data=str_2, file_name="Danh_sach_khoa_cong_khai.key", mime="text/plain", on_click="ignore")
    # else:
    #     st.info("Hãy upload file khóa")

    # else:
    #     st.error("Vui lòng nhập số lượng người tham gia")

# def handle_choice_method(msg):
#     st.session_state.solg = st.number_input(label="Nhập số lượng người tham gia ký thông điệp", format="%d", min_value=1)
#     if st.session_state.solg:
#         files_data = upload_file_key()
#         if files_data:
#             st.session_state.pub_key = []
#             st.session_state.priv_key = []
#             if len(files_data) != st.session_state.solg:
#                 st.error(f"Bạn phải tải đúng {st.session_state.solg} file khóa. Hiện tại bạn tải {len(files_data)} file.")
#                 return
#             for data in files_data:
#                 get_pub_priv(data)
#             st.success("Upload đúng số lượng khóa")
#             st.write("Đây là khoá công khai của người dùng:", st.session_state.pub_key)
#             st.write("Đây là khoá bí mật của người dùng:", st.session_state.priv_key)
#             # print(type(st.session_state.pub_key[0]))
#             # print(type(st.session_state.priv_key[0]))
#             # st.write(msg, st.session_state.solg, st.session_state.pub_key, st.session_state.priv_key)
#             # nếu muốn ký luôn
#             r, s = main.group_sign(msg, st.session_state.solg, st.session_state.pub_key, st.session_state.priv_key)
#             st.write("Giá trị R:", r)
#             st.write("Giá trị S:", s)
#             f = open("Chu_ky.sig", "w")
#             f.write(str(r) + "\n" + str(s))
#             f.close()
#             f = open("Chu_ky.sig", "r")
#             str_1 = f.read()
#             f = open("Danh_sach_khoa_cong_khai.key", "w")
#             for i in range(len(st.session_state.pub_key)):
#                 f.write(str(st.session_state.pub_key[i].format(compressed=False).hex())+"\n")
#             f.close()
#             f = open("Danh_sach_khoa_cong_khai.key", "r")
#             str_2 = f.read()
#             colunm = st.columns(2)
#             with colunm[0]:
#                 st.download_button(label="Tải chữ ký nhóm về", data=str_1, file_name="Chu_ky.sig", mime="text/plain", on_click="ignore")
#             with colunm[1]:
#                 st.download_button(label="Tải danh sách khoá công khai về", data=str_2, file_name="Danh_sach_khoa_cong_khai.key", mime="text/plain", on_click="ignore")
#         else:
#             st.info("Hãy upload file khóa")

#     else:
#         st.error("Vui lòng nhập số lượng người tham gia")

        
    

st.markdown("<h3 style='text-align: center; color: black;'>Chào mừng đến với chương trình ký số nhóm</h3>", unsafe_allow_html=True) # st.markdown("<h1 style='text-align: center; color: black;'>Chào mừng đến với chương trình ký số nhóm</h1>", unsafe_allow_html=True)
choice =  st.sidebar.radio(label="Chọn phương thức để ký nhóm", options=["Thực hiện với thông điệp được nhập từ bàn phím", "Thực hiện với thông điệp được lấy từ file"], index=0)

if choice == "Thực hiện với thông điệp được nhập từ bàn phím":
    msg = st.text_input(label="Hãy nhập thông điệp vào đây")
    handle_choice_method(msg)
elif choice == "Thực hiện với thông điệp được lấy từ file":
    msg = upload_file.upload_file()
    handle_choice_method(msg)

