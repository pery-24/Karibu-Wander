import streamlit as st
import time  
from database import SessionLocal, User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")

st.title("🚀 Create Your Karibu Wander Account")

with st.form("signup_form"):
    username = st.text_input("Choose a username", max_chars=30)
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm = st.text_input("Confirm password", type="password")
    full_name = st.text_input("Your name (optional)")

    if st.form_submit_button("Sign Up 🎉"):
        if not username or not email or not password:
            st.error("Fill all required fields")
        elif password != confirm:
            st.error("Passwords don't match")
        elif len(password) < 6:
            st.error("Password too short")
        else:
            db = SessionLocal()
            try:
                if db.query(User).filter(User.username == username).first():
                    st.error("Username already taken")
                elif db.query(User).filter(User.email == email.lower()).first():
                    st.error("Email already registered")
                else:
                    hashed = pwd_context.hash(password)
                    new_user = User(
                        username=username,
                        email=email.lower(),
                        hashed_password=hashed,
                        full_name=full_name or username
                    )
                    db.add(new_user)
                    db.commit()
                    user_id = new_user.id
                    db.close()

                    # Auto login
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.user_id = user_id

                    st.success(f"Welcome {username}! You're in! 🎉")
                    st.balloons()
                    
                    # FIX: These 3 lines make sure you actually leave the page
                    time.sleep(1.5)                         # lets you see the balloons
                    st.switch_page("pages/dashboard.py")     # ← THIS MOVES YOU INSIDE

            except Exception as e:
                db.rollback()
                st.error("Something went wrong – try again")
                print(e)  # shows error in terminal if needed
            finally:
                db.close()