import database

if __name__ == '__main__':
  name="test_event_"
  date="2015-10-1"
  start_time="00:00:0"
  end_time="00:00:02"
  description="hello"
  image=None
  org_name="org_"
  building=None
  room=None
  buildings = ['Mudd', 'IAB', 'Schermerhorn', 'Math', 'Havemeyer', 'Fayerweather', 'Schapiro', 'Wien', 'CSB', 'Fake Building']
  categories = ['Speaker', 'Stress Buster', 'Review Session', 'Food', 'Music', 'Meet and Greet', 'Study Session', 'Squash Practice', 'Concert', 'Yoga']
  for item in categories:
    database.create_category(item)
