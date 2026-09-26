"""
Перетворює "плаский" список тривог з API на статус кожної з 27 областей:
  - "full"    — тривога по всій області
  - "partial" — тривога в частині області (район/громада/місто)
  - "none"    — тривоги немає
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from api import Alert
from regions import Region, REGIONS, REGIONS_BY_TITLE

STATUS_NONE = "none"
STATUS_PARTIAL = "partial"
STATUS_FULL = "full"

ALERT_TYPE_UK = {
    "air_raid": "повітряна тривога",
    "artillery_shelling": "загроза артобстрілу",
    "urban_fights": "вуличні бої",
    "chemical": "хімічна загроза",
    "nuclear": "радіаційна загроза",
}

STATUS_COLOR = {
    STATUS_NONE: "green",
    STATUS_PARTIAL: "yellow",
    STATUS_FULL: "bold red",
}

STATUS_LABEL_UK = {
    STATUS_NONE: "спокійно",
    STATUS_PARTIAL: "частково",
    STATUS_FULL: "тривога",
}


@dataclass
class RegionStatus:
    region: Region
    status: str = STATUS_NONE
    alert_type: Optional[str] = None
    started_at: Optional[str] = None
    # для "partial" — список конкретних місць (районів/громад) під тривогою
    details: list[str] = field(default_factory=list)


def compute_region_statuses(alerts: list[Alert]) -> dict[str, RegionStatus]:
    statuses: dict[str, RegionStatus] = {
        r.code: RegionStatus(region=r) for r in REGIONS
    }

    for alert in alerts:
        if alert.location_type == "oblast":
            region = REGIONS_BY_TITLE.get(alert.location_title)
            if region is None:
                continue
            rs = statuses[region.code]
            rs.status = STATUS_FULL
            rs.alert_type = alert.alert_type
            rs.started_at = alert.started_at
        else:
            # неповна тривога: шукаємо батьківську область
            parent_title = alert.location_oblast
            region = REGIONS_BY_TITLE.get(parent_title) if parent_title else None
            if region is None:
                continue
            rs = statuses[region.code]
            if rs.status != STATUS_FULL:
                rs.status = STATUS_PARTIAL
                rs.alert_type = rs.alert_type or alert.alert_type
                rs.started_at = rs.started_at or alert.started_at
            rs.details.append(alert.location_title)

    return statuses
