from script import UserAccessReport, Event
import datetime

report = UserAccessReport()
events = [
    Event(datetime.datetime(2024, 1, 1, 10, 0, 0), "login", "machine1", "user1"),
    Event(datetime.datetime(2024, 1, 1, 11, 0, 0), "logout", "machine1", "user1")
  ]

def test_users_basic(self):
  users = report(events, "2024-01-01 00:00:00", "2024-01-02 00:00:00")
  assert users == {"machine1":{"user1"}}

def test_duration_basic(self):
   duration = report.login_duration(events, "user1", "machine1")
   assert duration.total_seconds() == 3600
