"""
Клієнт для роботи з API alerts.in.ua.
Документація API: https://devportal.alerts.in.ua/
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import requests

API_BASE_URL = "https://api.alerts.in.ua/v1"


class AlertsApiError(Exception):
    """Помилка звернення до API тривог."""


@dataclass
class Alert:
    location_title: str          # напр. "Львівська область" або "Бориспільська громада"
    location_type: str           # "oblast" | "raion" | "city" | "hromada" ...
    alert_type: str              # "air_raid" | "artillery_shelling" | ...
    started_at: str              # ISO-час початку тривоги
    location_oblast: Optional[str] = None  # область-"батько" для неповних тривог


class AlertsClient:
    """Тонкий клієнт над /v1/alerts/active.json"""

    def __init__(self, token: str, timeout: float = 10.0):
        if not token:
            raise AlertsApiError(
                "Не знайдено токен alerts.in.ua. Задайте змінну середовища "
                "ALERTS_IN_UA_TOKEN або передайте --token ВАШ_ТОКЕН."
            )
        self.token = token
        self.timeout = timeout
        self._session = requests.Session()

    def fetch_active_alerts(self) -> list[Alert]:
        """Повертає список активних тривог по всій Україні."""
        url = f"{API_BASE_URL}/alerts/active.json"
        try:
            resp = self._session.get(
                url, params={"token": self.token}, timeout=self.timeout
            )
        except requests.RequestException as exc:
            raise AlertsApiError(f"Немає з'єднання з API: {exc}") from exc

        if resp.status_code == 401:
            raise AlertsApiError("Невірний токен alerts.in.ua (401 Unauthorized).")
        if resp.status_code == 429:
            raise AlertsApiError("Перевищено ліміт запитів до API (429 Too Many Requests).")
        if not resp.ok:
            raise AlertsApiError(
                f"API повернуло помилку {resp.status_code}: {resp.text[:200]}"
            )

        try:
            data = resp.json()
        except ValueError as exc:
            raise AlertsApiError("Некоректна відповідь API (очікувався JSON).") from exc

        raw_alerts = data.get("alerts", [])
        alerts: list[Alert] = []
        for item in raw_alerts:
            alerts.append(
                Alert(
                    location_title=item.get("location_title", "?"),
                    location_type=item.get("location_type", "?"),
                    alert_type=item.get("alert_type", "?"),
                    started_at=item.get("started_at", "?"),
                    location_oblast=item.get("location_oblast"),
                )
            )
        return alerts
