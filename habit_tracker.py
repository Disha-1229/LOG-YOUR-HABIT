"""
Habit Tracker - Console Version
-------------------------------
Track your daily habits with monthly dashboard, streaks, weekly summary, 
top habits, and quick logging.

Run: python habit_tracker.py
Requirements: Python 3.x (standard library only)
"""

import calendar
from datetime import datetime, timedelta

HABITS = ["Exercise", "Reading", "Meditation", "Study", "Sleep Early"]
history = {}

def show_calendar(year, month):
    today = datetime.now()
    cal = calendar.monthcalendar(year, month)
    print(f"\n{calendar.month_name[month]} - {year}")
    print("Mo Tu We Th Fr Sa Su")
    for week in cal:
        line = ""
        for day in week:
            if day == 0:
                line += "   "
            elif day == today.day and month == today.month and year == today.year:
                line += f"[{day:2}]"
            else:
                line += f" {day:2} "
        print(line)

def days_in_month(year, month):
    return calendar.monthrange(year, month)[1]

def habit_streak(habit):
    if not history:
        return 0
    dates = sorted([datetime.strptime(d, "%d-%m-%Y") for d in history if habit in history[d]])
    if not dates:
        return 0
    max_streak = 0
    current_streak = 1
    for i in range(1, len(dates)):
        if (dates[i] - dates[i-1]).days == 1:
            current_streak += 1
        else:
            current_streak = 1
        max_streak = max(max_streak, current_streak)
    return max(max_streak, current_streak)

def show_dashboard(year, month):
    today = datetime.now()
    show_calendar(year, month)

    print("\n--- Habit Summary ---")
    count = {h: 0 for h in HABITS}
    for date, done in history.items():
        d, m, y = map(int, date.split("-"))
        if m == month and y == year:
            for h in done:
                count[h] += 1

    for h, c in count.items():
        percent = c / days_in_month(year, month) * 100
        print(f"{h}: {c} day(s), {percent:.1f}% completion, Longest Streak: {habit_streak(h)} day(s)")

    print("\n--- Weekly Summary (last 7 days) ---")
    last_week = [today - timedelta(days=i) for i in range(7)]
    for day in reversed(last_week):
        key = f"{day.day}-{day.month}-{day.year}"
        done = history.get(key, [])
        print(f"{day.day}-{day.month}-{day.year}: {', '.join(done) if done else 'No habits done'}")

    if count:
        top = max(count, key=lambda h: count[h])
        print(f"\nMost consistent habit: {top} ({count[top]} days)")

    today_key = f"{today.day}-{today.month}-{today.year}"
    pending = [h for h in HABITS if today_key not in history or h not in history[today_key]]
    print("\nPending Habits Today:")
    print(", ".join(pending) if pending else "All habits done today! ✅")

def record_habits():
    today = datetime.now()
    print("\n1. Quick log today")
    print("2. Log for another day")
    choice = input("Enter choice: ")
    if choice == '1':
        day, month, year = today.day, today.month, today.year
    else:
        day = int(input("Enter day of month: "))
        month = int(input("Enter month: "))
        year = int(input("Enter year: "))

    date_key = f"{day}-{month}-{year}"
    print(f"\nLogging habits for {date_key}:")
    selected = []
    for h in HABITS:
        ans = input(f"Did you do '{h}'? (y/n): ").lower()
        if ans == 'y':
            selected.append(h)
    history[date_key] = selected
    print("Saved!\n")

def show_day():
    day = int(input("\nEnter day of month: "))
    month = int(input("Enter month: "))
    year = int(input("Enter year: "))
    key = f"{day}-{month}-{year}"
    if key in history:
        print(f"Habits done on {key}: {', '.join(history[key])}")
    else:
        print(f"No habits logged for {key}")

def reset_month():
    month = int(input("\nEnter month to reset: "))
    year = int(input("Enter year: "))
    keys_to_delete = [k for k in history if int(k.split('-')[1]) == month and int(k.split('-')[2]) == year]
    for k in keys_to_delete:
        del history[k]
    print(f"All habits for {calendar.month_name[month]} {year} have been reset!")

if __name__ == "__main__":
    while True:
        print("\nOptions:")
        print("1. Show dashboard")
        print("2. Log habits")
        print("3. Show habits for a day")
        print("4. Reset month data")
        print("5. Exit")
        choice = input("Enter choice: ")
        if choice == '1':
            show_dashboard(datetime.now().year, datetime.now().month)
        elif choice == '2':
            record_habits()
        elif choice == '3':
            show_day()
        elif choice == '4':
            reset_month()
        elif choice == '5':
            break
        else:
            print("Invalid choice!")
