import logging
import sched
import time

from apple_price_parser import update_products_data
from migrations.migrate import run_migration

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

def schedule_task(interval_sec: int, scheduler, task):
    scheduler.enter(interval_sec, 1, task)
    scheduler.enter(interval_sec, 1, lambda sch=scheduler: schedule_task(interval_sec, scheduler, task),
                    (scheduler,))


def main():
    scheduler = sched.scheduler(time.time, time.sleep)
    update_products_data(scheduled=True)
    schedule_task(interval_sec=180, scheduler=scheduler, task=lambda: update_products_data(scheduled=True))
    scheduler.run()


if __name__ == "__main__":
    run_migration()
    main()
