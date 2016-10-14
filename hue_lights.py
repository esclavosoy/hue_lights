from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import time, logging, os, signal
from phue import Bridge
from astral import Astral
#logging.basicConfig(level=logging.DEBUG)

#Scheduler
scheduler = BackgroundScheduler()

#Hue Stuff
b = Bridge('10.0.1.3')
b.connect()

#Sunset stuff
city_name = 'Los Angeles'
a = Astral()
a.solar_depression = 'civil'
city = a[city_name]
timezone = city.timezone
sun = city.sun(date=datetime.now(), local=True)



def turn_on():
	try:
                b.set_light(3,'on', True)
                print('Lights On')
	except:
                print('Exception raised')
		pass

def turn_off():
	try:
		b.set_light(3,'on', False)
	except:
                print('Exeception raised')
		pass




scheduler.start()

while True:
    scheduler.add_job(func=turn_on, trigger='date', next_run_time=(str(sun['sunset'] - timedelta(minutes=45))))
    scheduler.add_job(func=turn_off, trigger='date',
            next_run_time=(str(sun['sunrise'] + timedelta(hours=25))))
    time.sleep(60)
