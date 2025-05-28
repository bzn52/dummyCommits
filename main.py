import os
import subprocess
import random
from datetime import datetime, timedelta

def make_commit(commit_message: str, commit_date: str):
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = commit_date
    env["GIT_COMMITTER_DATE"] = commit_date

    with open("dummy.txt", "a") as f:
        f.write(f"{commit_message} - {commit_date}\n")

    subprocess.run(["git", "add", "dummy.txt"], check=True)
    subprocess.run(["git", "commit", "-m", commit_message], check=True, env=env)
    print(f"✅ Commit: '{commit_message}' at {commit_date}")

def generate_random_dates(start_date: datetime, end_date: datetime):
    current = start_date
    all_dates = []
    while current <= end_date:
        commits_today = random.randint(1, 6)
        for _ in range(commits_today):
            random_time = timedelta(
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59),
                seconds=random.randint(0, 59)
            )
            commit_time = current + random_time
            all_dates.append(commit_time)
        current += timedelta(days=1)
    return sorted(all_dates)

def main():
    print("🚀 Bulk Random Commit Generator")
    
    # Input format
    date_format = "%Y-%m-%d"

    start_str = input("Start date (YYYY-MM-DD): ")
    end_str = input("End date (YYYY-MM-DD): ")

    try:
        start_date = datetime.strptime(start_str, date_format)
        end_date = datetime.strptime(end_str, date_format)
        if end_date < start_date:
            raise ValueError("End date must be after start date.")
    except ValueError as e:
        print(f"❌ Error: {e}")
        return

    print("⏳ Generating commit schedule...")
    dates = generate_random_dates(start_date, end_date)

    for i, dt in enumerate(dates, start=1):
        message = f"Auto-commit #{i}"
        iso_time = dt.strftime("%Y-%m-%d %H:%M:%S")
        make_commit(message, iso_time)

    print(f"\n🎉 Done. {len(dates)} commits generated between {start_str} and {end_str}.")

if __name__ == "__main__":
    main()
