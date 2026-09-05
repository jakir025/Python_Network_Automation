import schedule
import time 
import datetime

def SECONDS():
    TNOW = datetime.datetime.now().replace(microsecond=0)
    print( str(TNOW) + " This prints every 5 seconds interval for 3 times")

def MINUTE():
    TNOW = datetime.datetime.now().replace(microsecond=0)
    print( str(TNOW) + " This prints every minute")
     
schedule.every(1).minutes.do(MINUTE)
schedule.every().minute.at(":05").do(SECONDS)
schedule.every().minute.at(":10").do(SECONDS)
schedule.every().minute.at(":15").do(SECONDS)

while True:
    schedule.run_pending()
    time.sleep(1)    
