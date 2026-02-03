import streamlit as st
import sqlite3
import requests
from streamlit_lottie import st_lottie

# --- 1. THEME & STYLING ---
def apply_theme():
    st.markdown("""
    <style>
    /* Main Background and Text */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    
    /* Custom Card for Metrics */
    div[data-testid="stMetricValue"] {
        font-size: 32px;
        color: #FFD700 !important; /* Gold */
    }
    
    /* Styled Buttons */
    .stButton>button {
        background-color: #1f4068;
        color: white;
        border-radius: 20px;
        border: 1px solid #FFD700;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #FFD700;
        color: #1f4068;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #16213e !important;
        border-right: 2px solid #FFD700;
    }

    /* Input Box Focus */
    input {
        background-color: #1b1b1b !important;
        color: white !important;
        border: 1px solid #FFD700 !important;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #1f4068;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
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

    # Load Data into Session State
    db_bal, db_count = get_db_data()
    if 'balance' not in st.session_state: st.session_state.balance = db_bal
    if 'count' not in st.session_state: st.session_state.count = db_count

    # Sidebar
    with st.sidebar:
        st.title("🏦 Dashboard")
        lottie_coin = load_lottie("https://assets5.lottiefiles.com/packages/lf20_yem69hui.json")
        if lottie_coin:
            st_lottie(lottie_coin, height=150, key="coin")
        
        st.write("---")
        st.info(f"User ID: sathwika9121")
        
        if st.button("🔄 Reset Daily Limit"):
            update_db(st.session_state.balance, 0)
            st.session_state.count = 0
            st.success("Limit reset!")
            st.rerun()

    # Header Section
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("<h1 style='color: #FFD700; margin-bottom: 0;'>Sathwika Premium Bank</h1>", unsafe_allow_html=True)
        st.write("Secure | Reliable | Digital")
    with col2:
        lottie_bank = load_lottie("https://assets9.lottiefiles.com/packages/lf20_y9m9pmo7.json")
        if lottie_bank:
            st_lottie(lottie_bank, height=100, key="bank")

    st.markdown("---")

    # Metrics Display
    m1, m2, m3 = st.columns(3)
    m1.metric("Current Balance", f"₹{st.session_state.balance:,.2f}")
    m2.metric("Daily Transactions", f"{st.session_state.count} / 3")
    m3.metric("Account Type", "Premium Savings", delta="Verified")

    st.markdown("---")

    # Transaction Logic
    if st.session_state.count >= 3:
        st.error("🚫 Daily transaction limit reached. Please visit the branch or try again tomorrow.")
    else:
        tab1, tab2 = st.tabs(["💰 Deposit Funds", "💸 Withdraw Funds"])

        with tab1:
            st.subheader("Cash Deposit")
            d_amt = st.number_input("Enter Amount to Deposit (Multiples of 100):", min_value=0, step=100, key="dep_input")
            if st.button("Confirm Deposit", key="dep_btn"):
                if d_amt > 0 and d_amt <= 50000 and d_amt % 100 == 0:
                    st.session_state.balance += d_amt
                    st.session_state.count += 1
                    update_db(st.session_state.balance, st.session_state.count)
                    st.balloons()
                    st.success(f"Deposit successful: ₹{d_amt}")
                    st.rerun()
                elif d_amt > 50000:
                    st.warning("Max deposit limit is ₹50,000.")
                else:
                    st.warning("Please enter a valid multiple of 100.")

        with tab2:
            st.subheader("Cash Withdrawal")
            w_amt = st.number_input("Enter Amount to Withdraw (Multiples of 100):", min_value=0, step=100, key="with_input")
            if st.button("Confirm Withdrawal", key="with_btn"):
                if w_amt > 0 and w_amt <= 20000 and w_amt % 100 == 0:
                    if w_amt <= st.session_state.balance:
                        st.session_state.balance -= w_amt
                        st.session_state.count += 1
                        update_db(st.session_state.balance, st.session_state.count)
                        st.snow()
                        
                        # Note calculation
                        f = w_amt // 500
                        rem = w_amt % 500
                        t = rem // 200
                        o = (rem % 200) // 100
                        
                        st.success(f"Successfully withdrawn: ₹{w_amt}")
                        st.info(f"Dispensed Notes: ₹500 x {f}, ₹200 x {t}, ₹100 x {o}")
                        st.rerun()
                    else:
                        st.error("Insufficient balance.")
                elif w_amt > 20000:
                    st.warning("Max withdrawal limit is ₹20,000.")
                else:
                    st.warning("Please enter a valid multiple of 100.")

if __name__ == '__main__':
    main()