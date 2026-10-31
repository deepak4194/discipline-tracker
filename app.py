import streamlit as st
from datetime import date
from supabase import create_client, Client

st.set_page_config(page_title="30-Day Discipline Tracker", page_icon="🎯", layout="centered")

START_DATE = date(2026, 11, 1)
END_DATE = date(2026, 11, 30)

GOALS = [
    "Wake up by 6:30 AM",
    "Complete morning warm-up / activity",
    "Eat planned breakfast (oats + egg/soya omelette)",
    "Complete morning study session",
    "Have lunch and take proper rest",
    "Complete gym workout",
    "Have post-workout protein and dinner",
    "Complete evening study session",
    "Read for 10 minutes",
    "Sleep by 11:00 PM",
]

@st.cache_resource
def get_supabase() -> Client:
    return create_client(
        st.secrets["supabase"]["url"],
        st.secrets["supabase"]["key"],
    )

try:
    supabase = get_supabase()
except Exception as exc:
    st.error("Supabase connection is not configured. Check your Streamlit Secrets.")
    st.caption("Required secrets: [supabase] url and key.")
    st.stop()

def load_day(day: date) -> dict:
    response = (
        supabase.table("daily_progress")
        .select("goal_id, completed")
        .eq("date", day.isoformat())
        .execute()
    )
    return {int(row["goal_id"]): bool(row["completed"]) for row in response.data}

def save_goal(day: str, goal_id: int, state_key: str):
    supabase.table("daily_progress").upsert(
        {
            "date": day,
            "goal_id": goal_id,
            "completed": bool(st.session_state[state_key]),
        },
        on_conflict="date,goal_id",
    ).execute()

st.title("🎯 30-Day Discipline Tracker")
st.caption("Your simple daily tracker · November 1–30, 2026")

selected_day = st.date_input(
    "Choose a day",
    value=START_DATE,
    min_value=START_DATE,
    max_value=END_DATE,
)

day_key = selected_day.isoformat()
st.subheader(selected_day.strftime("%A, %d %B %Y"))

try:
    saved = load_day(selected_day)
except Exception:
    st.error(
        "Couldn't read your progress from Supabase. Check that the SQL access policies "
        "have been added and your Streamlit Secrets are correct."
    )
    st.stop()

for i, goal in enumerate(GOALS):
    widget_key = f"{day_key}_{i}"
    if widget_key not in st.session_state:
        st.session_state[widget_key] = saved.get(i, False)

    st.checkbox(
        goal,
        key=widget_key,
        on_change=save_goal,
        args=(day_key, i, widget_key),
    )

completed = sum(bool(st.session_state.get(f"{day_key}_{i}", False)) for i in range(len(GOALS)))
total = len(GOALS)
progress = completed / total

st.progress(progress)
st.write(f"**{completed} / {total} goals completed · {round(progress * 100)}%**")

st.divider()
st.subheader("Your November overview")

try:
    response = (
        supabase.table("daily_progress")
        .select("date, goal_id, completed")
        .gte("date", START_DATE.isoformat())
        .lte("date", END_DATE.isoformat())
        .execute()
    )
    records = response.data
except Exception:
    st.error("Couldn't load the monthly overview from Supabase.")
    st.stop()

by_day = {}
for row in records:
    if row["completed"]:
        by_day[row["date"]] = by_day.get(row["date"], 0) + 1

completed_total = sum(by_day.values())
perfect_days = sum(1 for count in by_day.values() if count == total)
overall = completed_total / (total * 30)

c1, c2, c3 = st.columns(3)
c1.metric("Overall progress", f"{overall:.0%}")
c2.metric("Perfect days", perfect_days)
c3.metric("Goals completed", f"{completed_total}/{total * 30}")

st.caption("Daily completed goals")
for day_text in sorted(by_day):
    st.write(f"{date.fromisoformat(day_text).strftime('%d %b')} · {by_day[day_text]}/{total}")

st.caption("Your progress is saved automatically to Supabase whenever you tick or untick a goal.")
