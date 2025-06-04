from __future__ import annotations

from typing import Callable

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


def start(hour_utc: int, job: Callable[[], None]) -> BackgroundScheduler:
    sched = BackgroundScheduler(timezone="UTC")
    sched.add_job(job, CronTrigger(hour=hour_utc, minute=0))
    sched.start()
    return sched
