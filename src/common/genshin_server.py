import dataclasses
from datetime import timezone, timedelta, time, datetime

import genshin

utc_offset = lambda hour_offset: timezone(timedelta(seconds=hour_offset * 3600))

# This applies to all regions.
SERVER_RESET_TIME = time(hour=4)


@dataclasses.dataclass
class Server:
    region: str
    tzoffset: timezone

    @property
    def last_daily_reset(self):
        now = datetime.now(tz=self.tzoffset)
        return datetime.combine(now, SERVER_RESET_TIME).replace(tzinfo=self.tzoffset)

    @property
    def last_weekly_reset(self):
        return self.last_daily_reset - timedelta(days=self.last_daily_reset.weekday())


class ServerEnum:
    NORTH_AMERICA = Server("os_usa", utc_offset(-5))
    ASIA = Server("os_asia", utc_offset(+8))
    EUROPE = Server("os_euro", utc_offset(+1))

    @staticmethod
    def from_uid(uid: int):
        region = genshin.utils.recognize_server(uid)
        for e in ServerEnum.__dict__.values():
            if isinstance(e, Server) and e.region == region:
                return e