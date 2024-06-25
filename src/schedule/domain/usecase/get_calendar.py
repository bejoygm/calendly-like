from datetime import date, datetime, timedelta
from typing import List
from uuid import UUID
from zoneinfo import ZoneInfo

from src.schedule.domain.models.event import SpotAvailability
from src.schedule.domain.repos.availability import AvailabilityRepo
from src.schedule.domain.repos.event import EventRepo


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

        # convert the start_date, end_date to the timezone of the event
        # find the intersection between events window and query window
        # then generate all durations
        # then convert back to users timezone

        event_tzinfo = ZoneInfo(availability.timezone)
        query_tzinfo = ZoneInfo(timezone)

        query_start = datetime(
            year=start_date.year,
            month=start_date.month,
            day=start_date.day,
            tzinfo=event_tzinfo,
        )
        query_end = datetime(
            year=end_date.year,
            month=end_date.month,
            day=end_date.day,
            tzinfo=event_tzinfo,
        )

        event_start = datetime(
            year=event.starts_from.year,
            month=event.starts_from.month,
            day=event.starts_from.day,
            tzinfo=event_tzinfo,
        )

        event_end = datetime(
            year=event.ends_at.year,
            month=event.ends_at.month,
            day=event.ends_at.day,
            tzinfo=event_tzinfo,
        )

        # find intersection between these two dates
        start = max(query_start, event_start)
        end = min(query_end, event_end)

        # a valid intersection wasn't found
        if start > end:
            return {
                "timezone": timezone,
                "days": [],
            }

        num_days = (end - start).days + 1

        date_list = [start + timedelta(days=x) for x in range(num_days)]

        availability_by_day = {a["day"]: a["intervals"] for a in availability.rules}

        calendar = []
        for dt in date_list:
            day_name = dt.strftime("%a").lower()
            intervals = availability_by_day.get(day_name, [])

            print(intervals, day_name, dt)

            total_durations = []

            for interval in intervals:
                start = parse_time(interval["from"])
                end = parse_time(interval["to"])

                start_dt = dt.replace(hour=start.hour, minute=start.minute)
                end_dt = dt.replace(hour=end.hour, minute=end.minute)

                total_durations += generate_time_range(
                    start_dt, end_dt, event.duration, query_tzinfo
                )

            spots = [
                {
                    "status": SpotAvailability.available,
                    "start_time": dt,
                }
                for dt in total_durations
            ]

            calendar.append(
                {
                    "date": dt.date(),
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


def generate_time_range(
    start: datetime,
    end: datetime,
    duration: int,
    tz: ZoneInfo,
) -> List[datetime]:
    times = []
    current = start
    while current < end:
        times.append(current.astimezone(tz))
        current += timedelta(minutes=duration)
    return times
