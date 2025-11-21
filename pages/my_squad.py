# pages/my_squad.py
import streamlit as st
from database import SessionLocal, Trip, JoinRequest, User

if not st.session_state.get("logged_in"):
    st.switch_page("home.py")

db = SessionLocal()
username = st.session_state.username

st.title("My Travel Squad ✊🏾❤️")
st.markdown("Your future travel family across all trips")

# Find all people in user's trips
members = set()
trips_as_creator = db.query(Trip).filter(Trip.creator_name == username).all()
for trip in trips_as_creator:
    members.add(trip.creator_name)
    accepted = db.query(JoinRequest).filter(JoinRequest.trip_id == trip.id, JoinRequest.status == "accepted").all()
    for a in accepted:
        members.add(a.requester_name)

joined_trips = db.query(JoinRequest).filter(JoinRequest.requester_name == username, JoinRequest.status == "accepted").all()
for j in joined_trips:
    trip = db.query(Trip).filter(Trip.id == j.trip_id).first()
    members.add(trip.creator_name)
    others = db.query(JoinRequest).filter(JoinRequest.trip_id == trip.id, JoinRequest.status == "accepted").all()
    for o in others:
        members.add(o.requester_name)

if members:
    cols = st.columns(5)
    for i, name in enumerate(members):
        user = db.query(User).filter(User.username == name).first()
        with cols[i % 5]:
            st.image("https://via.placeholder.com/120?text=👤", width=120)
            st.write(f"**{user.full_name or user.username}**")
            st.caption(f"{user.age or ''} • {user.gender or ''}")
            if user.instagram:
                st.write(f"@{user.instagram}")
else:
    st.info("Your squad is waiting — join or create a trip!")

db.close()