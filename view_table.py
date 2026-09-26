"""Табличний вигляд: область / статус / тип тривоги / триває з."""
from __future__ import annotations

from rich.table import Table

from status import (
    ALERT_TYPE_UK,
    RegionStatus,
    STATUS_COLOR,
    STATUS_LABEL_UK,
    STATUS_FULL,
    STATUS_PARTIAL,
)


def _status_sort_key(rs: RegionStatus) -> tuple:
    order = {STATUS_FULL: 0, STATUS_PARTIAL: 1}
    return (order.get(rs.status, 2), rs.region.api_title)


def render_table(statuses: dict[str, RegionStatus]) -> Table:
    table = Table(title="Мапа тривог — Україна", expand=True)
    table.add_column("Область", ratio=3)
    table.add_column("Статус", ratio=2)
    table.add_column("Тип тривоги", ratio=2)
    table.add_column("Триває з", ratio=2)
    table.add_column("Деталі", ratio=3)

    for rs in sorted(statuses.values(), key=_status_sort_key):
        color = STATUS_COLOR[rs.status]
        alert_type_uk = ALERT_TYPE_UK.get(rs.alert_type, rs.alert_type or "—")
        details = ", ".join(rs.details[:3]) + ("…" if len(rs.details) > 3 else "")
        table.add_row(
            rs.region.api_title,
            f"[{color}]{STATUS_LABEL_UK[rs.status]}[/{color}]",
            alert_type_uk if rs.status != "none" else "—",
            (rs.started_at or "—") if rs.status != "none" else "—",
            details or "—",
        )

    return table
