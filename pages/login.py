# pages/login.py  
import streamlit as st
from database import SessionLocal, User
from passlib.context import CryptContext

# THIS MUST MATCH THE ONE IN SIGNUP.PY !!!
pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")

st.title("🔑 Welcome Back to Karibu Wander")

with st.form("login_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    login_btn = st.form_submit_button("Log In 🚀")

    if login_btn:
        if not username or not password:
            st.error("Please fill both fields")
        else:
            db = SessionLocal()
            user = db.query(User).filter(User.username == username).first()
            db.close()

            if user and pwd_context.verify(password, user.hashed_password):
                # SUCCESS – LOG THEM IN
                st.session_state.logged_in = True
                st.session_state.username = user.username
                st.session_state.user_id = user.id

                st.success(f"Karibu tena, {username}! ✊🏾")
                st.balloons()
                st.switch_page("pages/dashboard.py")
            else:
                st.error("Wrong username or password 😅 Try again!")