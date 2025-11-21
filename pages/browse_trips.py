# pages/browse_trips.py  
import streamlit as st
from database import SessionLocal, Trip, JoinRequest, User

if not st.session_state.get("logged_in"):
    st.switch_page("home.py")

# 10 DESTINATIONS WITH LOCAL IMAGES
places = [
    {"name": "Mount Kenya", "img": "images/Mount Kenya.jpg"},
    {"name": "Pyramids of Giza", "img": "images/Pyramids of Giza.jpg"},
    {"name": "Victoria Falls", "img": "images/Victoria Falls.jpg"},
    {"name": "Serengeti Migration", "img": "images/Serengeti Migration.jpg"},
    {"name": "Table Mountain", "img": "images/Table Mountain.jpg"},
    {"name": "Chefchaouen", "img": "images/Chefchaouen.jpg"},
    {"name": "Okavango Delta", "img": "images/Okavango Delta.jpg"},
    {"name": "Lake Nakuru", "img": "images/Lake Nakuru.jpg"},
    {"name": "Sossusvlei Dunes", "img": "images/Sossusvlei Dunes.jpg"},
    {"name": "Zanzibar Stone Town", "img": "images/Zanzibar Stone Town.jpg"},
]

db = SessionLocal()
username = st.session_state.username

st.title("Browse Trips Across Africa ✈️")

trips = db.query(Trip).filter(Trip.creator_name != username).order_by(Trip.start_date).all()

if not trips:
    st.info("No trips yet — be the first to create one!")
else:
    for trip in trips:
        creator = db.query(User).filter(User.username == trip.creator_name).first()

        # Find matching photo safely
        photo_path = None
        for p in places:
            if p["name"] in trip.destination:
                photo_path = p["img"]
                break

        # If no match, use a beautiful placeholder from the web (no local file needed)
        if not photo_path:
            photo_path = f"https://source.unsplash.com/800x600/?{trip.destination.split(',')[0]},africa,travel"

        with st.container(border=True):
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(photo_path, use_container_width=True)
            with col2:
                st.subheader(f"✈️ {trip.destination}")
                st.write(f"**By:** {trip.creator_name} • Age {creator.age if creator else '?'} • {creator.gender if creator else ''}")
                st.write(f"📅 {trip.start_date} → {trip.end_date}")
                st.write(f"👥 {trip.current_people}/{trip.max_people} going • Budget level {trip.budget_level}")
                st.write(f"**Vibe:** {trip.vibe}")
                st.caption(trip.description or "Amazing adventure!")

                
                               # =============== MATCH SCORE + JOIN BUTTON (MAGIC ADDED) ===============
                already = db.query(JoinRequest).filter(
                    JoinRequest.trip_id == trip.id,
                    JoinRequest.requester_name == username
                ).first()

                # Get current logged-in user details for match calculation
                current_user = db.query(User).filter(User.id == st.session_state.user_id).first()

                if already:
                    if already.status == "pending":
                        st.warning("⏳ Request Sent")
                    elif already.status == "accepted":
                        st.success("✅ You're In This Trip!")
                    else:
                        st.info("Request declined")
                else:
                    # ==== CALCULATE MATCH SCORE ====
                    score = 60  # base score

                    if creator and current_user:
                        # Age compatibility
                        if creator.age and current_user.age:
                            age_diff = abs(creator.age - current_user.age)
                            if age_diff <= 5:
                                score += 20
                            elif age_diff <= 12:
                                score += 10

                        # Travel style overlap
                        creator_styles = set((creator.travel_style or "").split("|||"))
                        user_styles = set((current_user.travel_style or "").split("|||"))
                        common = creator_styles & user_styles
                        score += len(common) * 8

                        # Gender balance bonus (optional fun)
                        if creator.gender and current_user.gender and creator.gender != current_user.gender:
                            score += 5

                    score = min(score, 98)  # cap at 98%

                    # ==== BUTTON WITH MATCH SCORE ====
                    if st.button(
                        f"I'm Interested! 🔥 ({score}% Match)",
                        key=f"join_{trip.id}",
                        use_container_width=True,
                        type="primary" if score >= 80 else "secondary"
                    ):
                        db.add(JoinRequest(trip_id=trip.id, requester_name=username, status="pending"))
                        db.commit()
                        st.success("Request sent! They'll reply soon 🎉")
                        st.rerun()
                # =======================================================================
db.close()