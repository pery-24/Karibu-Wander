import streamlit as st
from datetime import date
from database import SessionLocal, User, Trip, JoinRequest
import random
import base64




# Clear cache to prevent image issues
st.query_params.clear()

st.set_page_config(page_title="Karibu Wander", page_icon="plane", layout="centered")

# BEAUTIFUL AFRICAN THEME
st.markdown("""
<style>
    .main {background: linear-gradient(135deg, #ff6b35, #f7931e, #ffb400); min-height: 100vh;}
    h1 {font-family: 'Georgia', serif; color: #2c3e50; text-align: center;}
    .card {background: white; border-radius: 20px; padding: 35px; max-width: 500px; margin: 30px auto;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);}
    .stButton>button {background: #2c3e50; color: white; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

def encode_image(img):
    return base64.b64encode(img.read()).decode()

db = SessionLocal()

# DUMMY DATA — ONLY RUNS ONCE
if db.query(Trip).count() == 0:
    dummy_users = [
        ("Aisha Kamau", 26, "Female", "Love sunsets and good jollof", "@aisha_wanders"),
        ("Kwame Osei", 29, "Male", "Chasing waterfalls & vibes", "@kwame_travels"),
        ("Zuri Nala", 24, "Female", "Culture, food, and deep talks", "@zuriinafrica"),
        ("Tunde Adebayo", 31, "Male", "Road trips & afrobeats only", "@tundeonthemove"),
        ("Fatou Diallo", 27, "Female", "Art, history, and ocean air", "@fatouexplores"),
        ("Chidi Okonkwo", 28, "Male", "Safari dreams & braai nights", "@chidiadventures"),
    ]
    
    dummy_trips = [
        ("Zanzibar", "2025-12-20", "2025-12-28", 1, "Spice island escape — beaches, dhow cruises, fresh seafood"),
        ("Cape Town", "2025-12-15", "2025-12-25", 2, "Table Mountain hike, wine tasting, ocean road trip"),
        ("Maasai Mara", "2025-08-05", "2025-08-12", 3, "Great Migration safari + hot air balloon ride"),
        ("Lamuu", "2026-01-10", "2026-01-17", 2, "Swahili culture, old town walks, sunset dhow"),
        ("Victoria Falls", "2025-11-18", "2025-11-23", 4, "Devil’s Pool swim, bungee, helicopter flip"),
        ("Accra to Cape Coast", "2025-12-26", "2026-01-04", 2, "Afrobeats, Year of Return, castles & beaches"),
    ]

    for name, age, gender, bio, insta in dummy_users:
        if not db.query(User).filter(User.name == name).first():
            db.add(User(name=name, age=age, gender=gender, bio=bio, instagram=insta))
    
    for dest, s, e, budget, vibe in dummy_trips:
        creator = random.choice([u[0] for u in dummy_users])
        db.add(Trip(
            creator_name=creator,
            destination=dest,
            start_date=date.fromisoformat(s),
            end_date=date.fromisoformat(e),
            budget_level=budget,
            vibe=vibe,
            max_people=random.randint(4,7),
            current_people=random.randint(1,4)
        ))
    db.commit()

# SIGN-UP PAGE
if "user" not in st.session_state:
    st.markdown("<h1>KARIBU WANDER</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center; color:#2c3e50;'>Find your African travel buddy</h3>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        with st.form("signup"):
            st.write("### Create your profile")
            name = st.text_input("Full Name", placeholder="e.g. Aisha Mohammed")
            age = st.slider("Age", 18, 60, 25)
            gender = st.selectbox("Gender", ["Female", "Male", "Non-binary", "Prefer not to say"])
            bio = st.text_area("Short bio", "Love travelling, food, culture...")
            instagram = st.text_input("Instagram (optional)", placeholder="@aisha_travels")
            uploaded_photo = st.file_uploader("Upload your photo", type=["jpg", "jpeg", "png"])
            
            col1, col2 = st.columns(2)
                if name.strip():
                    photo_url = f"https://i.pravatar.cc/300?u={random.randint(1,1000)}"
                    if uploaded_photo:
                        photo_bytes = uploaded_photo.read()
                        encoded = base64.b64encode(photo_bytes).decode()
                        photo_url = f"data:image/png;base64,{encoded}"
                    
                    st.session_state.user = {
                        "name": name.strip(),
                        "age": age,
                        "gender": gender,
                        "bio": bio,
                        "instagram": instagram,
                        "photo": photo_url
                    }
                    if not db.query(User).filter(User.name == name.strip()).first():
                        db.add(User(name=name.strip(), age=age, gender=gender, bio=bio, instagram=instagram))
                        db.commit()
                    
                    st.balloons()
                    st.success(f"Karibu {name.split()[0]}! Welcome to the family")
                    st.rerun()
                else:
                    st.error("Please enter your name")
        st.markdown("</div>", unsafe_allow_html=True)

else:
    # MAIN APP — LOGGED IN
    with st.sidebar:
        st.image(st.session_state.user["photo"], width=100)
        st.write(f"**{st.session_state.user['name']}**")
        st.caption(st.session_state.user.get("bio", ""))
        choice = st.radio("Menu", ["Create Trip", "Swipe", "My Matches", "Profile", "Discover Africa"])

    # DISCOVER AFRICA — PERFECT & WORKING
    if choice == "Discover Africa":
        st.markdown("<h1 style='text-align:center; color:#2c3e50;'>Discover Africa</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; font-size:18px; color:#555;'>Iconic places to visit across the continent</p>", unsafe_allow_html=True)

        countries = ["All", "Kenya", "Egypt", "South Africa", "Tanzania", "Morocco", "Zambia", "Botswana", "Namibia", "Zimbabwe"]
        country = st.selectbox("Filter by country", countries, key="discover_africa_filter")

        places = [
            {"name": "Mount Kenya", "country": "Kenya", "img": "images/Mount Kenya.jpg", "desc": "Snow-capped peaks and alpine meadows.", "activities": "Hiking • Climbing • Wildlife"},
            {"name": "Pyramids of Giza", "country": "Egypt", "img": "images/Pyramids of Giza.jpg", "desc": "The last remaining ancient wonder.", "activities": "History • Camel Ride"},
            {"name": "Victoria Falls", "country": "Zambia/Zimbabwe", "img": "images/Victoria Falls.jpg", "desc": "The Smoke That Thunders.", "activities": "Devil's Pool • Bungee"},
            {"name": "Serengeti Migration", "country": "Tanzania", "img": "images/Serengeti Migration.jpg", "desc": "Nature's greatest show.", "activities": "Safari • Balloon"},
            {"name": "Table Mountain", "country": "South Africa", "img": "images/Table Mountain.jpg", "desc": "Iconic views of Cape Town.", "activities": "Cable Car • Hiking"},
            {"name": "Chefchaouen", "country": "Morocco", "img": "images/Chefchaouen.jpg", "desc": "The stunning blue city.", "activities": "Photography • Culture"},
            {"name": "Okavango Delta", "country": "Botswana", "img": "images/Okavango Delta.jpg", "desc": "Desert meets water.", "activities": "Mokoro • Safari"},
            {"name": "Lake Nakuru", "country": "Kenya", "img": "images/Lake Nakuru.jpg", "desc": "Flamingos turn the lake pink.", "activities": "Birdwatching • Safari"},
            {"name": "Sossusvlei Dunes", "country": "Namibia", "img": "images/Sossusvlei Dunes.jpg", "desc": "Towering red dunes.", "activities": "Sandboarding • Hiking"},
            {"name": "Zanzibar Stone Town", "country": "Tanzania", "img": "images/Zanzibar Stone Town.jpg", "desc": "Historic Swahili charm.", "activities": "Culture • Markets"},
        ]

        filtered = [p for p in places if country == "All" or country in p["country"]]

        for place in filtered:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(place["img"], use_container_width=True)
            with col2:
                st.markdown(f"### {place['name']}")
                st.write(f"**{place['country']}**")
                st.write(place["desc"])
                st.caption(f"Do: {place['activities']}")
            st.markdown("---")

    elif choice == "Create Trip":
        st.markdown("<h1>Create Your Trip</h1>", unsafe_allow_html=True)
        with st.form("trip"):
            destination = st.text_input("Destination", "Lagos, Marrakech, Nairobi...")
            c1, c2 = st.columns(2)
            start = c1.date_input("From", date(2025, 12, 20))
            end = c2.date_input("To", date(2026, 1, 5))
            budget = st.selectbox("Budget", ["Budget", "Comfort", "Luxury"])
            vibe = st.text_area("Trip vibe")
            if st.form_submit_button("Post Trip"):
                db.add(Trip(
                    creator_name=st.session_state.user["name"],
                    destination=destination,
                    start_date=start,
                    end_date=end,
                    budget_level=["Budget", "Comfort", "Luxury"].index(budget) + 1,
                    vibe=vibe,
                    max_people=6,
                    current_people=1
                ))
                db.commit()
                st.success("Trip posted!")
                st.balloons()

    elif choice == "Swipe":
        with open("pages/1_Browse_Trips.py", encoding="utf-8") as f:
            exec(f.read())

    elif choice == "My Matches":
        with open("pages/2_My_Trips.py", encoding="utf-8") as f:
            exec(f.read())

    elif choice == "Profile":
        st.markdown("<h1 style='text-align:center; color:#2c3e50;'>Your Profile</h1>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(st.session_state.user["photo"], width=220, use_container_width=True)
        with col2:
            st.markdown(f"### {st.session_state.user['name']}")
            st.write(f"**Age:** {st.session_state.user['age']}")
            st.write(f"**Gender:** {st.session_state.user['gender']}")
            st.write(f"**Bio:** {st.session_state.user['bio']}")
            if st.session_state.user.get("instagram"):
                st.write(f"**Instagram:** @{st.session_state.user['instagram']}")
            st.markdown("---")
            if st.button("Logout", use_container_width=True):
                st.session_state.user = None
                st.rerun()

db.close()