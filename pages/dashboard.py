# pages/dashboard.py 
import streamlit as st
from database import SessionLocal, Trip, JoinRequest, User
from datetime import date

# Protection
if not st.session_state.get("logged_in"):
    st.switch_page("home.py")

db = SessionLocal()
username = st.session_state.username
user_id = st.session_state.user_id

st.title("Karibu Wander")
st.markdown(f"### Habari, **{username}**! ✈️")

# ===== COUNTDOWN WIDGET =====
upcoming = db.query(Trip).filter(
    Trip.creator_name == username,
    Trip.start_date > date.today()
).order_by(Trip.start_date).first()

if upcoming:
    days_left = (upcoming.start_date - date.today()).days
    st.success(f"⏰ Your next trip: **{upcoming.destination}** in **{days_left} days**! 🎉")
    if days_left <= 7:
        st.balloons()

# ===== METRICS =====
your_trips = db.query(Trip).filter(Trip.creator_name == username).count()
pending = db.query(JoinRequest)\
    .join(Trip, JoinRequest.trip_id == Trip.id)\
    .filter(Trip.creator_name == username, JoinRequest.status == "pending")\
    .count()
matches = db.query(JoinRequest)\
    .join(Trip, JoinRequest.trip_id == Trip.id)\
    .filter(Trip.creator_name == username, JoinRequest.status == "accepted")\
    .count()

col1, col2, col3 = st.columns(3)
with col1: st.metric("Your Trips", your_trips)
with col2: st.metric("Pending Requests", pending)
with col3: st.metric("Confirmed Matches", matches)

st.divider()

# ===== QUICK ACTIONS (FIXED: no rerun in callback) =====
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("Profile →", use_container_width=True):
        st.switch_page("pages/profile_setup.py")
with col2:
    if st.button("Create Trip", use_container_width=True):
        st.switch_page("pages/create_trip.py")
with col3:
    if st.button("Browse Trips", use_container_width=True):
        st.switch_page("pages/browse_trips.py")
with col4:
    if st.button("My Squad ❤️", use_container_width=True, type="primary"):
        st.switch_page("pages/my_squad.py")

st.divider()

# ===== YOUR TRIPS + SHARE =====
st.subheader("Your Active Trips ✈️")
trips = db.query(Trip).filter(Trip.creator_name == username).all()
if trips:
    for trip in trips:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"**{trip.destination}**")
            st.caption(f"{trip.start_date} → {trip.end_date} • {trip.current_people}/{trip.max_people} going")
        with col2:
            share_link = f"https://karibuwander.app/trip/{trip.id}"
            if st.button("Share ↗", key=f"share_{trip.id}"):
                st.code(share_link)
                st.success("Link copied!")
else:
    st.info("No trips yet — create your first adventure!")

# ===== JOIN REQUESTS =====
st.divider()
st.subheader("Join Requests")
requests = db.query(JoinRequest)\
    .join(Trip, JoinRequest.trip_id == Trip.id)\
    .filter(Trip.creator_name == username, JoinRequest.status == "pending")\
    .all()

if requests:
    for req in requests:
        trip = db.query(Trip).filter(Trip.id == req.trip_id).first()
        requester = db.query(User).filter(User.username == req.requester_name).first()
        with st.container(border=True):
            st.write(f"**{req.requester_name}** ({requester.age if requester else ''}, {requester.gender if requester else ''}) wants to join:")
            st.success(trip.destination)
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Accept", key=f"acc_{req.id}"):
                    req.status = "accepted"
                    trip.current_people += 1
                    db.commit()
                    st.success("Accepted!")
                    st.rerun()
            with col2:
                if st.button("Decline", key=f"dec_{req.id}"):
                    req.status = "declined"
                    db.commit()
                    st.rerun()
else:
    st.info("No new requests")

# ===== LIVE MAP! =====
st.divider()
st.subheader("Live Travel Tribe Map – Africa is Calling ✊🏾")

all_trips = db.query(Trip).all()
if all_trips:
    try:
        from streamlit_folium import folium_static
        import folium
    except ImportError:
        st.error("Run: pip install streamlit-folium folium")
        st.stop()

    coords = {
        "Mount Kenya": [-0.15, 37.31],
        "Pyramids of Giza": [29.9792, 31.1342],
        "Victoria Falls": [-17.9244, 25.8572],
        "Serengeti Migration": [-2.3333, 34.8333],
        "Table Mountain": [-33.9621, 18.4098],
        "Chefchaouen": [35.1688, -5.2636],
        "Okavango Delta": [-19.2855, 22.9074],
        "Lake Nakuru": [-0.2833, 36.0833],
        "Sossusvlei Dunes": [-24.7356, 15.2872],
        "Zanzibar Stone Town": [-6.1659, 39.1992],
    }

    m = folium.Map(location=[0, 20], zoom_start=4, tiles="CartoDB positron")
    for trip in all_trips:
        dest = trip.destination.split(",")[0].strip()
        lat, lon = coords.get(dest, [0, 20])
        color = "green" if trip.current_people < trip.max_people*0.7 else "orange" if trip.current_people < trip.max_people else "red"
        popup = f"<b>{trip.destination}</b><br>By {trip.creator_name}<br>{trip.start_date} → {trip.end_date}<br>{trip.current_people}/{trip.max_people} going"
        folium.CircleMarker([lat, lon], radius=15 + trip.current_people*4, color=color, fill=True, popup=popup, tooltip=trip.destination).add_to(m)

    folium_static(m, width=725, height=500)
else:
    st.info("Be the first to light up Africa!")

# ===== LOGOUT =====
st.divider()
if st.button("Log out"):
    st.session_state.clear()
    st.switch_page("home.py")

db.close()