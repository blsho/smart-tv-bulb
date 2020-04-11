#!/usr/bin/env python3

from crontab import CronTab
import datetime
import pytz
from dateutil import tz
import requests
import config
import os

_cron_comment_ = "Auto-generated job for TV lighting"
_sunset_url_   = "https://api.sunrise-sunset.org/json"

def get_sunset():
    resp = requests.get(
        url = _sunset_url_,
        params = config.location
    )
    sunset_str = resp.json()['results']['sunset']
    today = datetime.date.today()
    sunset_dt = pytz.utc.localize(datetime.datetime.strptime(sunset_str, '%I:%M:%S %p'))
    return sunset_dt.replace(
        year=today.year,
        month=today.month,
        day=today.day,
    ).astimezone(tz.tzlocal())

def set_cron(sunset):
    with CronTab(user=True) as cron:
        create_job = True
        for job in cron.find_comment(_cron_comment_):
            job.setall(sunset)
            create_job = False
        if create_job:
            #create the job
            base_dir = os.path.dirname(os.path.realpath(__file__))
            py_bin = f"{base_dir}/venv/bin/python"
            light_script = f"{base_dir}/tv_light_action.py"
            job_sufix = "> /dev/null 2>&1"
            job = cron.new(
                command=f"{py_bin} {light_script} {job_sufix}",
                comment=_cron_comment_
            )
            job.setall(sunset)

def main():
    print(get_sunset())
    set_cron(get_sunset())

main()
