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

def test_no_events(self):
    users = report([], "2024-01-01 00:00:00", "2024-01-02 00:00:00")
    assert users == {} 

def test_no_login(self):
   events = [
    Event(datetime.datetime(2024, 1, 1, 10, 0, 0), "logout", "machine1", "user1")
   ]
   duration = report.login_duration(events, "user1", "machine1")
   assert duration.total_seconds() == 0

def test_no_logout(self):
   events = [
    Event(datetime.datetime(2024, 1, 1, 10, 0, 0), "login", "machine1", "user1")
   ]
   duration = report.login_duration(events, "user1", "machine1")
   assert duration.total_seconds() == 0


def test_multiple_logins(self):
    events = [
      Event(datetime.datetime(2024, 1, 1, 10, 0, 0), "login", "machine1", "user1"),
      Event(datetime.datetime(2024, 1, 1, 11, 0, 0), "logout", "machine1", "user1"),
      Event(datetime.datetime(2024, 1, 1, 12, 0, 0), "login", "machine1", "user1"),
      Event(datetime.datetime(2024, 1, 1, 13, 0, 0), "logout", "machine1", "user1")
    ]
    duration = report.login_duration(events, "user1", "machine1")
    assert duration.total_seconds() == 7200

def test_overlapping_logins(self):
    events = [
      Event(datetime.datetime(2024, 1, 1, 10, 0, 0), "login", "machine1", "user1"),
      Event(datetime.datetime(2024, 1, 1, 10, 30, 0), "login", "machine1", "user1"),
      Event(datetime.datetime(2024, 1, 1, 11, 0, 0), "logout", "machine1", "user1")
    ]
    duration = report.login_duration(events, "user1", "machine1")
    assert duration.total_seconds() == 3600

def test_different_users(self):
    events = [
      Event(datetime.datetime(2024, 1, 1, 10, 0, 0), "login", "machine1", "user1"),
      Event(datetime.datetime(2024, 1, 1, 10, 30, 0), "login", "machine1", "user2"),
      Event(datetime.datetime(2024, 1, 1, 11, 0, 0), "logout", "machine1", "user1"),
      Event(datetime.datetime(2024, 1, 1, 11, 30, 0), "logout", "machine1", "user2")
    ]
    duration_user1 = report.login_duration(events, "user1", "machine1")
    duration_user2 = report.login_duration(events, "user2", "machine1")
    assert duration_user1.total_seconds() == 3600
    assert duration_user2.total_seconds() == 3600
