import streamlit as st
from datetime import date, timedelta
from firebase_config import init_firebase
from firebase_admin import auth, firestore

db = init_firebase()

if "user_id" not in st.session_state:
    st.session_state["user_id"] = None

st.title("🔥 Agentic AI Streak Tracker")

st.subheader("Login / Register")
email = st.text_input("Email")
password = st.text_input("Password", type = "password")

if st.button("Login or Register"):
    try: 
        user = auth.get_user_by_email(email)
        st.success(f"Logged in as {user.email}")
        st.session_state["user_id"] = user.uid

    except:
        try:
            user = auth.create_user(email = email, password = password)
            st.success(f"Registered and logged in as {user.email}")
            st.session_state["user_id"] = user.uid
        except Exception as e:
            st.error(f"Error: {str(e)}")

user_id = st.session_state["user_id"]

if user_id:
    st.subheader("➕ Add a New Streak")
    streak_name = st.text_input("Streak Name")
    if st.button("Add Streak"):
        if user_id and streak_name:
            db.collection("users").document(user_id).collection("streaks").document(streak_name).set({
                "name": streak_name,
                "createdAt": date.today().isoformat(),
                "lastCompletedDate": None,
                "streakCount": 0,
                "completedDates": []
            })
            st.success(f"✅ Streak '{streak_name}' added!")

    # View and Update Streaks
    st.subheader("📅 Your Streaks")
    if user_id:
        streaks_ref = db.collection("users").document(user_id).collection("streaks").stream()
        for streak in streaks_ref:
            s = streak.to_dict()
            st.markdown(f"**{s['name']}** – 🔥 {s['streakCount']} day(s)")

            if st.button(f"✅ Mark Done Today ({s['name']})"):
                today = date.today().isoformat()
                if s["lastCompletedDate"] != today:
                    updated_count = s["streakCount"] + 1 if s["lastCompletedDate"] == (date.today() - timedelta(days=1)).isoformat() else 1
                    db.collection("users").document(user_id).collection("streaks").document(s['name']).update({
                        "lastCompletedDate": today,
                        "streakCount": updated_count,
                        "completedDates": firestore.ArrayUnion([today])
                    })
                    st.rerun()
                else:
                    st.info("Already marked as done today!")
else:
    st.warning("Please log in to view and manage your streaks")