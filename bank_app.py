import streamlit as st
import sqlite3
import requests
from streamlit_lottie import st_lottie

# --- 1. THEME & STYLING ---
def apply_theme():
    st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    div[data-testid="stMetricValue"] {
        font-size: 32px;
        color: #FFD700 !important;
    }
    .stButton>button {
        background-color: #1f4068;
        color: white;
        border-radius: 20px;
        border: 1px solid #FFD700;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #FFD700;
        color: #1f4068;
    }
    section[data-testid="stSidebar"] {
        background-color: #16213e !important;
        border-right: 2px solid #FFD700;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE LOGIC ---
def init_db():
    conn = sqlite3.connect('sathwika_bank.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS account (id INTEGER PRIMARY KEY, balance REAL, trans_count INTEGER)')
    c.execute("SELECT count(*) FROM account")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO account (balance, trans_count) VALUES (10000, 0)")
    conn.commit()
    conn.close()

def update_db(balance, count):
    conn = sqlite3.connect('sathwika_bank.db')
    c = conn.cursor()
    c.execute("UPDATE account SET balance = ?, trans_count = ? WHERE id = 1", (balance, count))
    conn.commit()
    conn.close()

def get_db_data():
    conn = sqlite3.connect('sathwika_bank.db')
    data = conn.execute("SELECT balance, trans_count FROM account WHERE id = 1").fetchone()
    conn.close()
    return data

# --- 3. ANIMATION LOADER ---
def load_lottie(url):
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except:
        return None

# --- 4. MAIN APP ---
def main():
    st.set_page_config(page_title="Sathwika Premium Bank", layout="wide")
    apply_theme()
    init_db()

    db_bal, db_count = get_db_data()
    if 'balance' not in st.session_state: st.session_state.balance = db_bal
    if 'count' not in st.session_state: st.session_state.count = db_count

    with st.sidebar:
        st.title("🏦 Dashboard")
        lottie_coin = load_lottie("https://assets5.lottiefiles.com/packages/lf20_yem69hui.json")
        if lottie_coin: st_lottie(lottie_coin, height=150)
        if st.button("🔄 Reset Daily Limit"):
            update_db(st.session_state.balance, 0)
            st.session_state.count = 0
            st.rerun()

    st.markdown("<h1 style='color: #FFD700;'>Sathwika Premium Bank</h1>", unsafe_allow_html=True)
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Current Balance", f"₹{st.session_state.balance:,.2f}")
    m2.metric("Daily Transactions", f"{st.session_state.count} / 3")
    m3.metric("Account Status", "Premium")

    # Fixed the SyntaxError here by adding the '3'
    if st.session_state.count >= 3:
        st.error("Daily limit reached. Please reset in the sidebar.")
    else:
        tab1, tab2 = st.tabs(["💰 Deposit", "💸 Withdraw"])
        with tab1:
            d_amt = st.number_input("Deposit Amount:", min_value=0, step=100)
            if st.button("Confirm Deposit"):
                if d_amt > 0 and d_amt <= 50000 and d_amt % 100 == 0:
                    st.session_state.balance += d_amt
                    st.session_state.count += 1
                    update_db(st.session_state.balance, st.session_state.count)
                    st.balloons()
                    st.rerun()
        with tab2:
            w_amt = st.number_input("Withdrawal Amount:", min_value=0, step=100)
            if st.button("Confirm Withdrawal"):
                if w_amt > 0 and w_amt <= 20000 and w_amt <= st.session_state.balance:
                    st.session_state.balance -= w_amt
                    st.session_state.count += 1
                    update_db(st.session_state.balance, st.session_state.count)
                    st.snow()
                    st.rerun()

if __name__ == '__main__':
    main()