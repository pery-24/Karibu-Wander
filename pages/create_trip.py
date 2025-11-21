
import streamlit as st
from database import SessionLocal, Trip
from datetime import date

# Must be logged in
if not st.session_state.get("logged_in"):
    st.switch_page("home.py")

db = SessionLocal()

st.title("✈️ Create a New Trip")
st.markdown(f"#### Hey **{st.session_state.username}**, where are we going next? 🌍")

with st.form("create_trip_form", clear_on_submit=True):
    st.subheader("Trip Details")
    
    col1, col2 = st.columns(2)
    with col1:
        destination = st.text_input("Destination 🗺️", placeholder="e.g. Zanzibar, Maasai Mara, Cape Town")
        start_date = st.date_input("Start Date 📅", min_value=date.today())
    with col2:
        people_needed = st.number_input("How many travelers do you want? 👥", min_value=2, max_value=10, value=4)
        end_date = st.date_input("End Date 📅", min_value=start_date)

    budget = st.select_slider(
        "Budget Level 💰",
        options=["Budget Backpacker", "Comfortable", "Mid-Range", "Luxury"],
        value="Comfortable"
    )

    vibe = st.multiselect(
        "Trip Vibe & Activities 🌴",
        ["Beach & Relaxation", "Adventure & Safari", "City Exploration", "Party & Nightlife",
         "Culture & History", "Hiking & Nature", "Food & Wine", "Road Trip", "Wellness & Yoga", "Photography"],
        default=["Beach & Relaxation", "Adventure & Safari"]
    )

    description = st.text_area(
        "Describe your dream trip (what you want to do, who you want to meet, etc.)",
        placeholder="We’re looking for fun, open-minded people to explore Zanzibar with! Love snorkeling, beach parties, and good vibes only 🔥",
        height=150
    )

    submitted = st.form_submit_button("🚀 Publish My Trip!", type="primary", use_container_width=True)

    if submitted:
        if not destination or end_date < start_date:
            st.error("Please fill all fields correctly!")
        else:
            # Map budget to a number for easier matching later
            budget_map = {"Budget Backpacker": 1, "Comfortable": 2, "Mid-Range": 3, "Luxury": 4}
            
            new_trip = Trip(
                creator_name=st.session_state.username,
                destination=destination.title(),
                start_date=start_date,
                end_date=end_date,
                budget_level=budget_map[budget],
                vibe=" • ".join(vibe),
                max_people=people_needed,
                current_people=1  # just the creator for now
            )
            db.add(new_trip)
            db.commit()
            db.close()

            st.success(f"Trip to **{destination}** published successfully! 🎉")
            st.balloons()
            st.switch_page("pages/dashboard.py")