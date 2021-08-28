import time

import schedule
from core import Core
from logger import log

Time = '01:00'

log.info('cdn_cert cron job started, will check at %s every day', Time)

core = Core()

schedule.every().day.at(Time).do(core.do)

while True:
    schedule.run_pending()
    time.sleep(100)
