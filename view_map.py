"""ASCII-карта: області розташовані на умовній сітці, колір = статус."""
from __future__ import annotations

from rich.console import Group
from rich.table import Table
from rich.text import Text

from regions import REGIONS, GRID_ROWS, GRID_COLS
from status import RegionStatus, STATUS_COLOR, STATUS_LABEL_UK, STATUS_NONE


def render_map(statuses: dict[str, RegionStatus]) -> Group:
    grid = Table.grid(padding=(0, 1))
    for _ in range(GRID_COLS):
        grid.add_column(justify="center", width=8)

    cells = [["" for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
    for region in REGIONS:
        rs = statuses[region.code]
        color = STATUS_COLOR[rs.status]
        cells[region.row][region.col] = Text(region.abbr, style=color)

    for row in cells:
        grid.add_row(*[c if c != "" else Text("") for c in row])

    active_full = sum(1 for rs in statuses.values() if rs.status == "full")
    active_partial = sum(1 for rs in statuses.values() if rs.status == "partial")
    legend = Text.assemble(
        ("■ ", STATUS_COLOR["full"]), (f"тривога ({active_full})   ", ""),
        ("■ ", STATUS_COLOR["partial"]), (f"частково ({active_partial})   ", ""),
        ("■ ", STATUS_COLOR[STATUS_NONE]), ("спокійно", ""),
    )

    return Group(grid, Text(""), legend)
