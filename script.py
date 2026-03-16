# User Access Reporting Tool
# This script read a log file with all users login and logout events, and generates a report of which users were logged in on each machine in a given time

import csv
import datetime

# Represents a single login or logout event
class Event:
  def __init__(self, event_date, event_type, machine_name, user):
    self.date = event_date
    self.type = event_type
    self.machine = machine_name
    self.user = user

class UserAccessReport:
  def __init__(self):
    pass

  # Reads the log file and returns a list of all event objects
  def read_log_file(self, filename):
    try:
      with open(filename, "r") as logs:
        events = csv.DictReader(logs, skipinitialspace=True)

        return [
          Event(
            datetime.datetime.strptime(event["event_date"], "%Y-%m-%d %H:%M:%S"), 
            event["event_type"], 
            event["machine_name"], 
            event["user"]
            )
          for event in events
        ]
    except FileNotFoundError:
      print("Error: File not found.")
      return []

  # Takes a list of events and returns a distionary of machines and users that are logged in at the given access time
  def current_users(self, events, start_time, end_time):
    if not events:
      return {}
    
    #start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    #end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

    events.sort(key=lambda event: event.date)
    #new_events = [event for event in events if (start_time <= event.date and event.date <= end_time)]

    machines = {}
    for event in events:
      if event.machine not in machines:
        machines[event.machine] = set()
      if event.type == "login":
        machines[event.machine].add(event.user)
      elif event.type == "logout":
        if event.user in machines[event.machine]:
          machines[event.machine].remove(event.user)
    
    return machines

  # Track login time

  def generate_report(self, machines, filename):
    with open(filename, "w") as report:
      for machine, users in machines.items():
        if len(users) > 0:
          user_list = ", ".join(users)
          report.write("{}: {}\n".format(machine, user_list))


def run_report():
  report = UserAccessReport()
  
  events = report.read_log_file("events.csv")
  users = report.current_users(events, "2024-01-01 00:00:00", "2024-12-31 23:59:59")
  report.generate_report(users, "user_access_report.txt")

if __name__ == "__main__":
  run_report()