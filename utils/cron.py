import schedule
import time
import subprocess

def run_daily_job_check():
    subprocess.run(["python", "utils/fetch.py", "--page", "10"])



if __name__ == "__main__":
    schedule.every().day.at("09:00").do(run_daily_job_check)

    print("Scheduler started for daily_job_check.py")
    while True:
        schedule.run_pending()
        time.sleep(1)