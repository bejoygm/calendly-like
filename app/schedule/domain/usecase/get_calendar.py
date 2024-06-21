from datetime import date, datetime, timedelta
from typing import List
from zoneinfo import ZoneInfo
from uuid import UUID

from app.schedule.domain.models.event import SpotAvailability
from app.schedule.domain.repos.availability import AvailabilityRepo
from app.schedule.domain.repos.event import EventRepo


class CreateCalenderUsecase:
    def __init__(
        self,
        availability_repo: AvailabilityRepo,
        event_repo: EventRepo,
    ):
        self.availability_repo = availability_repo
        self.event_repo = event_repo

    def execute(
        self,
        event_id: UUID,
        start_date: date,
        end_date: date,
        timezone: str,
    ):
        event = self.event_repo.get(id=event_id)

        if not event:
            raise AssertionError

        availability = self.availability_repo.get(id=event.availability_id)

        if not availability:
            raise AssertionError

        tzinfo = ZoneInfo(availability.timezone)

        start = datetime(
            year=start_date.year,
            month=start_date.month,
            day=start_date.day,
            tzinfo=tzinfo,
        )
        end = datetime(
            year=end_date.year,
            month=end_date.month,
            day=end_date.day,
            tzinfo=tzinfo,
        )

        num_days = (end - start).days

        date_list = [start + timedelta(days=x) for x in range(num_days)]

        availability_by_day = {a["day"]: a["intervals"] for a in availability.rules}

        calendar = []
        for dt in date_list:

            day_name = dt.strftime("%a").lower()
            intervals = availability_by_day.get(day_name, [])

            total_durations = []

            for interval in intervals:
                start = parse_time(interval["from"])
                end = parse_time(interval["to"])

                start_dt = dt.replace(hour=start.hour, minute=start.minute)
                end_dt = dt.replace(hour=end.hour, minute=end.minute)

                total_durations += generate_time_range(start_dt, end_dt, 30, timezone)

            spots = [
                {
                    "status": SpotAvailability.available,
                    "start_time": dt,
                }
                for dt in total_durations
            ]

            calendar.append(
                {
                    "date": dt,
                    "spots": spots,
                }
            )

        return {
            "timezone": timezone,
            "days": calendar,
        }


def parse_time(time: str) -> datetime:
    return datetime.strptime(time, "%H:%M")


# function to get day name for a datetime object
def get_day_name(dt: datetime) -> str:
    return dt.strftime("%A")


# change hour of a datetime
def change_time(
    dt: datetime,
    hour: int,
    minute: int,
    tz: str,
) -> datetime:
    tzinfo = ZoneInfo(tz)
    return dt.replace(hour=hour, minute=minute).astimezone(tzinfo)


def generate_time_range(
    start: datetime,
    end: datetime,
    duration: int,
    tz: str,
) -> List[datetime]:
    times = []
    current = start
    while current < end:
        times.append(current.astimezone(ZoneInfo(tz)))
        current += timedelta(minutes=duration)
    return times
