from typing import List
from uuid import UUID
from zoneinfo import ZoneInfo

from pydantic import AwareDatetime
from src.event.domain.models.availability import Availability
from src.event.domain.models.event import Event
from datetime import date, datetime, timedelta
from src.event.domain.models.event import SpotAvailability


class SpotsService:
    def __init__(self, availability: Availability, event: Event):
        self.availability = availability
        self.event = event

    def generate_spots(
        self,
        booked_spots: dict[AwareDatetime, bool],
        start_date: date,
        end_date: date,
        timezone: str,
        booking_by: UUID,
    ):
        # 1. convert the start_date, end_date to the timezone of the event
        # 2. find the intersection between events window and query window
        # 3. generate spots for a given date
        # 4. check if the spot is already booked
        # 4. convert spot duration back to query timezone
        event_tzinfo = ZoneInfo(self.availability.timezone)
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
            year=self.event.starts_from.year,
            month=self.event.starts_from.month,
            day=self.event.starts_from.day,
            tzinfo=event_tzinfo,
        )

        event_end = datetime(
            year=self.event.ends_at.year,
            month=self.event.ends_at.month,
            day=self.event.ends_at.day,
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
        availability_by_day = {
            a["day"]: a["intervals"] for a in self.availability.rules
        }

        calendar = []
        for dt in date_list:
            day_name = dt.strftime("%a").lower()
            intervals = availability_by_day.get(day_name, [])

            total_durations = []

            for interval in intervals:
                start = _parse_time(interval["from"])
                end = _parse_time(interval["to"])

                start_dt = dt.replace(hour=start.hour, minute=start.minute)
                end_dt = dt.replace(hour=end.hour, minute=end.minute)

                total_durations += _generate_time_range(
                    start_dt, end_dt, self.event.duration, query_tzinfo
                )

            spots = [
                {
                    "status": SpotAvailability.available,
                    "start_time": dt,
                }
                for dt in total_durations
                if dt not in booked_spots
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


def _generate_time_range(
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


def _parse_time(time: str) -> datetime:
    return datetime.strptime(time, "%H:%M")
