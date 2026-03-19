# User Access Reporting Tool
# This script read a log file with all users login and logout events, and generates a report of which users were logged in on each machine in a given time

from collections import defaultdict
import csv
import datetime
import argparse
import os

# Represents a single login or logout event
class Event:
  def __init__(self, event_date, event_type, machine_name, user):
    self.date = event_date
    self.type = event_type
    self.machine = machine_name
    self.user = user

# Main class that handles reading the log file, processing the events, and generating the report
class UserAccessReport:
  # Reads the log file and returns a list of all event objects
  def read_log_file(self, filename):
    try:
      with open(filename, "r") as logs:
        event_file = csv.DictReader(logs, skipinitialspace=True)

        events = [
          Event(
            datetime.datetime.strptime(event["event_date"], "%Y-%m-%d %H:%M:%S"), 
            event["event_type"], 
            event["machine_name"], 
            event["user"]
            )
          for event in event_file
        ]

        print("Successfully read log file.")
        return events
    except FileNotFoundError:
      print("Error: File not found.")
      return []

  # Takes a list of events and returns a distionary of machines and users that are logged in at the given access time
  def current_users(self, events, start_time, end_time):
    if not events:
      return {}
    
    start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

    events.sort(key=lambda event : event.date)

    current_state = defaultdict(set)
    report_set = defaultdict(set)

    for event in events:
      if event.date > end_time:
        break

      if event.type.lower() == "login":
        current_state[event.machine].add(event.user)
      elif event.type.lower() == "logout":
        current_state[event.machine].discard(event.user)

      if event.date >= start_time:
        for user in current_state[event.machine]:
          report_set[event.machine].add(user)

    return report_set

  # Track login time
  def login_duration(self, events, user, machine):
    login_time = None
    total_duration = datetime.timedelta()


  def generate_report(self, machines, filename):
    if len(machines) == 0:
      print("No machines with logged in users found.")
      return

    if os.path.exists(filename):
      print("Warning: Report file already exists and will be overwritten.")

    with open(filename, "w") as report:
      for machine, users in sorted(machines.items()):
        if len(users) > 0:
          user_list = ", ".join(sorted(users))
          report.write("{}: {}\n".format(machine, user_list))
    print("Report generated successfully: {}".format(filename))


# Controls the flow of the program
def run_report():
  report = UserAccessReport()
  
  events = report.read_log_file("events.csv")
  users = report.current_users(events, "2024-01-01 00:00:00", "2024-12-31 23:59:59")
  report.generate_report(users, "user_access_report_test.txt")

# Entry point of the program
if __name__ == "__main__":
  run_report()