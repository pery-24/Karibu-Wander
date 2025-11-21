# seed_data.py 
import random
from datetime import date, timedelta
from database import SessionLocal, Base, engine, User, Trip
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")

# Create tables
Base.metadata.create_all(bind=engine)
db = SessionLocal()

# === YOUR 10 BEAUTIFUL DESTINATIONS WITH YOUR LOCAL IMAGES ===
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

# Create 55 African users
names = ["Amina", "Kwame", "Zuri", "Jabari", "Fatima", "Lerato", "Thabo", "Imani", "Chidi", "Nala", "Sipho", "Adanna", "Kofi", "Zainab", "Ngozi"]
surnames = ["Kamau", "Osei", "Nkosi", "Diallo", "Mokoena", "Okonkwo", "Dlamini", "Eze", "Wanjiku", "Adebayo"]
for i in range(55):
    first = random.choice(names)
    last = random.choice(surnames)
    username = first.lower() + last.lower()[:3] + str(random.randint(10,99))
    if db.query(User).filter(User.username == username).first():
        continue
    user = User(
        username=username,
        email=f"{username}@karibu.app",
        hashed_password=pwd_context.hash("pass123"),
        full_name=f"{first} {last}",
        age=random.randint(22,48),
        gender=random.choice(["Male","Female","Rather not say"]),
        bio="Ready for African adventures ✊🏾",
        travel_style="|||".join(random.sample(["Safari","Beach","Culture","Adventure"],3)),
        instagram=username
    )
    db.add(user)
db.commit()


users = db.query(User).all()
for place in places:
    creator = random.choice(users)
    start_in = random.randint(20, 150)
    trip = Trip(
        creator_name=creator.username,
        destination=f"{place['name']}, {place['country']}",
        description=place['desc'],
        start_date=date.today() + timedelta(days=start_in),
        end_date=date.today() + timedelta(days=start_in + random.randint(7,14)),
        budget_level=random.randint(2,4),
        vibe=place['activities'],
        max_people=random.randint(4,8),
        current_people=random.randint(1,3)
    )
    db.add(trip)
db.commit()
db.close()
print("DONE! Your 10 beautiful photos + 55 Africans are now in the app! 🎉")