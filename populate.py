import database
from random import randint

if __name__ == '__main__':
  name="test_event_"
  date="2015-10-1"
  start_time="00:00:0"
  end_time="00:00:02"
  description="hello"
  image=None
  org_name="org_"
  user_name="test_last_"
  building=None
  room=None
  buildings = ['Mudd', 'IAB', 'Schermerhorn', 'Math', 'Havemeyer', 'Fayerweather', 'Schapiro', 'Wien', 'CSB', 'Fake Building']
  categories = ['Food', 'Music', 'Meet and Greet']
  for i in range(20):
    database.create_invitation(user_name+str(randint(0,20)), org_name+"8", 24)


