#!/usr/bin/env python3
"""
Карта тривог в CLI — консольний застосунок для alerts.in.ua.

Приклади:
  export ALERTS_IN_UA_TOKEN=xxxxx
  python main.py                       # live ASCII-карта, оновлення кожні 15с
  python main.py --view table          # live-таблиця
  python main.py --once --view table   # один запит і вихід
  python main.py --interval 5          # частіше оновлення
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from datetime import datetime

from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

from api import AlertsClient, AlertsApiError
from status import compute_region_statuses
from view_map import render_map
from view_table import render_table

console = Console()


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Карта тривог в CLI (alerts.in.ua)")
    parser.add_argument(
        "--token",
        default=os.environ.get("ALERTS_IN_UA_TOKEN"),
        help="Токен alerts.in.ua (або задайте ALERTS_IN_UA_TOKEN)",
    )
    parser.add_argument(
        "--view",
        choices=["map", "table"],
        default="map",
        help="Вигляд: ASCII-карта чи таблиця (типово: map)",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=15.0,
        help="Інтервал оновлення в секундах для live-режиму (типово: 15)",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Зробити один запит і вийти, без live-оновлення",
    )
    return parser


def render_frame(view: str, statuses, last_update: datetime, error: str | None) -> Group:
    body = render_map(statuses) if view == "map" else render_table(statuses)
    footer_text = f"Оновлено: {last_update.strftime('%H:%M:%S')}"
    if error:
        footer_text += f"   [red]⚠ {error}[/red]"
    footer = Text.from_markup(footer_text, style="dim")
    return Group(
        Panel(body, title="Карта тривог — Україна", border_style="blue"),
        footer,
    )


def run() -> int:
    args = build_arg_parser().parse_args()

    try:
        client = AlertsClient(token=args.token)
    except AlertsApiError as exc:
        console.print(f"[bold red]Помилка:[/bold red] {exc}")
        return 1

    if args.once:
        try:
            alerts = client.fetch_active_alerts()
        except AlertsApiError as exc:
            console.print(f"[bold red]Помилка:[/bold red] {exc}")
            return 1
        statuses = compute_region_statuses(alerts)
        console.print(render_frame(args.view, statuses, datetime.now(), None))
        return 0

    last_error: str | None = None
    statuses = compute_region_statuses([])

    try:
        with Live(console=console, refresh_per_second=4, screen=False) as live:
            while True:
                try:
                    alerts = client.fetch_active_alerts()
                    statuses = compute_region_statuses(alerts)
                    last_error = None
                except AlertsApiError as exc:
                    last_error = str(exc)

                live.update(render_frame(args.view, statuses, datetime.now(), last_error))
                time.sleep(args.interval)
    except KeyboardInterrupt:
        console.print("\n[dim]Зупинено користувачем.[/dim]")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(run())
