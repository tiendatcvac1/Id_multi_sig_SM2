import streamlit as st
import time
import secrets
import hashlib
from coincurve import PrivateKey, PublicKey
import datetime


st.set_page_config(
    page_title="Trang chủ",
    page_icon="🏠",
    layout="wide"
)

column = st.columns(3)
with column[0]:
    st.image("logo.jpg")
with column[1]:
    st.image("t4.png", width=500)
with column[2]:
    st.image("logo.jpg")


def clock():

    # Create an empty placeholder to update the time dynamically
    placeholder = st.empty()

    while True:
        # Get the current time
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S %p") # Format as HH:MM:SS AM/PM

        # Update the placeholder with the current time using st.metric
        with placeholder.container():
            st.metric("Thời gian hiện tại",value=current_time)

        # Wait for 1 second before the next update
        time.sleep(1)

        # Note: In a typical Streamlit app, a while loop like this
        # will block other interactions. This is a simple
        # implementation for a basic clock display.
st.markdown("<h1 style='text-align: center; color: black;'>Chào mừng bạn đã đến với chương trình chữ ký số nhóm SM2</h1>", unsafe_allow_html=True)




# ======================================================================================================


# ===============================
# === Elliptic curve constants ==
# ===============================
SECP256K1_ORDER = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
# Field prime for secp256k1 (used to negate y coordinate)
FIELD_PRIME = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F


# ===============================
# === Utility functions =========
# ===============================
def H(*args):
    """SHA-256 hash function returning integer mod curve order"""
    m = hashlib.sha256()

    for a in args:

        if isinstance(a, str):
            a = a.encode()

        elif isinstance(a, int):
            a = a.to_bytes((a.bit_length() + 7) // 8, 'big')

        elif isinstance(a, PublicKey):
            a = a.format(compressed=False)

        m.update(a)

    return int.from_bytes(m.digest(), 'big') % SECP256K1_ORDER


def negate_public_key(P: PublicKey) -> PublicKey:
    """
    Return the elliptic-curve point -P as a PublicKey.
    Assumes P.format(compressed=False) returns 0x04 || x(32) || y(32).
    """
    raw = P.format(compressed=False)
    if raw[0] != 4:
        # Unexpected format; try to reformat to uncompressed
        raw = P.format(compressed=False)
    x_bytes = raw[1:33]
    y_bytes = raw[33:65]
    x = int.from_bytes(x_bytes, 'big')
    y = int.from_bytes(y_bytes, 'big')
    y_neg = (-y) % FIELD_PRIME
    y_neg_bytes = y_neg.to_bytes(32, 'big')
    neg_bytes = b'\x04' + x_bytes + y_neg_bytes
    return PublicKey(neg_bytes)


# ==================================
# === Phase 1: Setup and KeyGen ====
# ==================================
def setup():
    """System setup: define elliptic curve and generator"""
    G = PrivateKey.from_int(1).public_key  # Base point
    q = SECP256K1_ORDER
    params = {"q": q, "curve": "secp256k1", "G": G}
    return params


def master_keygen():
    """Generate master key pair (CA or key server)"""
    d_m = secrets.randbelow(SECP256K1_ORDER - 1) + 1
    sk_m = PrivateKey(d_m.to_bytes(32, 'big'))
    P_m = sk_m.public_key
    return d_m, P_m


def key_server_generate_for_ids(d_m, P_m, ids):
    """
    Generate private/public key pairs for all signers.
    Includes timing measurement for each key generation.
    """
    N = SECP256K1_ORDER
    records = []

    # Create a random reference G_bytes (ensure bytes input to PrivateKey)
    rand_int = secrets.randbelow(N - 1) + 1
    G_bytes = PrivateKey(rand_int.to_bytes(32, "big")).public_key.format(compressed=False)

    for uid in ids:
        # Step 1: Generate user private component z_i and M_i = z_i * G
        z_i = secrets.randbelow(N - 1) + 1
        M_i = PrivateKey(z_i.to_bytes(32, 'big')).public_key

        # Step 2: Compute c_i and d_i
        c_i = H(uid, str(N), G_bytes, P_m.format(compressed=False))
        d_i = (z_i + c_i * d_m) % N

        # Step 3: Compute public key P_i = M_i + c_i * P_m
        # multiply expects scalar bytes
        c_bytes = c_i.to_bytes(32, 'big')
        cP_m = P_m.multiply(c_bytes)
        P_i = PublicKey.combine_keys([M_i, cP_m])


        records.append({
            "ID": uid,
            "sk_i": d_i,
            "pk_i": P_i,
            "c_i": c_i
        })

    return records


# ==================================
# === Phase 2: Group Signing =======
# ==================================
def group_sign(message, solg, lst_pub_key, lst_priv_key):
    """Perform group signing among t users"""
    t = solg

    # Step 1: Each signer generates ephemeral key k_i and R_i = k_i * G
    k_values = []
    R_points = []
    for i in range(t):
        k_i = secrets.randbelow(SECP256K1_ORDER - 1) + 1
        k_values.append(k_i)
        R_i = PrivateKey(k_i.to_bytes(32, 'big')).public_key
        R_points.append(R_i)

    # Step 2: Aggregate ephemeral public keys
    R_sum = PublicKey.combine_keys(R_points)
    r = int.from_bytes(R_sum.format(compressed=False)[1:33], 'big') % SECP256K1_ORDER

    # Step 3: Compute challenge e
    P_list_bytes = []
    for i in range(t):
        P_list_bytes.append((lst_pub_key[i]).format(compressed=False))
    e = H(message, str(r), *P_list_bytes)
    # print("Kiểu dữ liệu của e là: ",type(e))
    # print("Kiểu dữ liệu của aaa là: ", type(lst_priv_key[0]), lst_priv_key[0])
    # Step 4: Partial signatures s_i = k_i + e * d_i
    s_values = [(k_values[i] + e * lst_priv_key[i]) % SECP256K1_ORDER for i in range(t)]
    s = sum(s_values) % SECP256K1_ORDER

    return (r, s)

# ==================================
# === Phase 3: Verification ========
# ==================================
def verify_signature(message, r, s, lst_pub_key):
    """Verify the group signature"""

    P_list = lst_pub_key
    P_list_bytes = [p.format(compressed=False) for p in P_list]
    e = H(message, str(r), *P_list_bytes)

    # Compute P_sum
    P_sum = PublicKey.combine_keys(P_list)

    # Compute sG (s * G)
    sG = PrivateKey(s.to_bytes(32, 'big')).public_key

    # Compute e * P_sum
    ePsum = P_sum.multiply(e.to_bytes(32, 'big'))

    # R' = sG - e*P_sum  => use negate_public_key for subtraction
    neg_eP = negate_public_key(ePsum)
    R_prime = PublicKey.combine_keys([sG, neg_eP])

    # Extract x-coordinate as integer (uncompressed format: 0x04 || x || y)
    r_prime = int.from_bytes(R_prime.format(compressed=False)[1:33], 'big') % SECP256K1_ORDER
    valid = (r_prime == r)


    return valid