import streamlit as st
from PIL import Image

st.set_page_config(page_title="Karibu Wander | Home", layout="wide")


logo = Image.open("logo.png")

# --- Soft Gradient Background ---
gradient = """
<style>
.stApp {
    background: linear-gradient(160deg, #e76f51, #2a9d8f, #264653);
    background-size: cover;
}
</style>
"""
st.markdown(gradient, unsafe_allow_html=True)

# --- Center Logo & Title ---
st.image(logo, width=200)

st.markdown(
    "<h1 style='text-align:center; color:#e9c46a; "
    "text-shadow:0px 0px 10px rgba(233,196,106,0.5);'>KARIBU WANDER</h1>",
    unsafe_allow_html=True,
)

st.markdown(
    "<p style='text-align:center; font-size:20px; color:#f4a261;'>"
    "Journeys Made With Tribe"
    "</p>",
    unsafe_allow_html=True,
)

st.write("")
st.write("")

# --- Feature Highlights ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🌍 Explore Africa")
    st.write("Discover beautiful destinations across 54 African countries.")

with col2:
    st.markdown("### 🤝 Find Your Tribe")
    st.write("Match with travel companions who share your vibe and interests.")

with col3:
    st.markdown("### 🛡️ Safe Adventures")
    st.write("Verified profiles, community trust, and guided safety options.")

col1, col2 = st.columns(2)

with col1:
    if st.button("Start →", use_container_width=True, type="primary"):
        st.switch_page("pages/signup.py")

with col2:
    if st.button("Already have an account? Log In", use_container_width=True):
        st.switch_page("pages/login.py")


