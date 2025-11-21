# pages/profile_setup.py
import streamlit as st
from database import SessionLocal, User
from PIL import Image
import io

# Protection: must be logged in
if not st.session_state.get("logged_in"):
    st.switch_page("home.py")

db = SessionLocal()
current_user = db.query(User).filter(User.id == st.session_state.user_id).first()

st.title("👤 Complete Your Travel Profile")
st.markdown(f"#### Hey **{st.session_state.username}**! Let's make you discoverable ✈️")

# Profile picture upload
col1, col2 = st.columns([1, 2])
with col1:
    st.subheader("Profile Picture")
    uploaded_file = st.file_uploader("Upload a photo", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, width=200, caption="Looking good! 🔥")
        # Convert to bytes to save later
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        photo_bytes = buf.getvalue()
    else:
        st.image("https://via.placeholder.com/200x200.png?text=Your+Photo", width=200)
        photo_bytes = current_user.instagram if current_user.instagram else None  # reuse old if exists

with col2:
    st.subheader("About You")
    age = st.slider("How old are you?", 18, 70, current_user.age if current_user else 25)
    gender = st.selectbox("Gender", ["Male", "Female", "Non-binary", "Rather not say"], 
                          index=["Male", "Female", "Non-binary", "Rather not say"].index(current_user.gender) if current_user and current_user.gender else 3)
    
    full_name = st.text_input("Full name (shown to matches)", value=current_user.full_name if current_user else "")
    bio = st.text_area("Tell us about yourself (max 300 chars)", 
                       value=current_user.bio if current_user else "", 
                       max_chars=300, height=120)
    
    travel_style = st.multiselect("Your travel style", 
        ["Adventure & Hiking", "Beach & Chill", "City Explorer", "Foodie Tours", "Budget Backpacker", 
         "Luxury & Comfort", "Solo Traveler", "Party & Nightlife", "Culture & History", "Nature & Wildlife"],
        default=current_user.travel_style.split("|||") if current_user and current_user.travel_style else [])

    instagram = st.text_input("Instagram handle (optional)", value=current_user.instagram if current_user else "", placeholder="@yourhandle")

st.divider()

if st.button("💾 Save Profile & Go to Dashboard", type="primary", use_container_width=True):
    # Save everything to database
    updated_user = current_user or db.query(User).filter(User.id == st.session_state.user_id).first()
    updated_user.age = age
    updated_user.gender = gender
    updated_user.full_name = full_name or st.session_state.username
    updated_user.bio = bio
    updated_user.travel_style = "|||".join(travel_style)  # store as string
    updated_user.instagram = instagram.replace("@", "") if instagram else ""

    db.commit()
    db.close()

    st.success("Profile saved successfully! You're ready to match! 🎉")
    st.balloons()
    st.switch_page("pages/dashboard.py")

# Back button
if st.button("← Back without saving"):
    st.switch_page("pages/dashboard.py")