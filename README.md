# 🚨 Карта Тривог — CLI



![Python](https://img.shields.io/badge/python-3.10%2B-blue)




![License](https://img.shields.io/badge/license-MIT-green)




![Status](https://img.shields.io/badge/status-active-brightgreen)



Консольний застосунок для Linux, що показує актуальні повітряні тривоги по
областях України в реальному часі, використовуючи
[API alerts.in.ua](https://dev.alerts.in.ua/).

Два вигляди на вибір:

| `map` — ASCII-карта | `table` — таблиця |
|---|---|
| Області підсвічені кольором прямо на умовній карті України | Область, тип тривоги, час початку, деталі — все в одному рядку |

Обидва працюють у **live-режимі з автооновленням**, як `htop`.

<!-- Сюди можна вставити скриншот/GIF з реальним запуском:


![demo](docs/demo.gif)


-->

## Зміст

- [Встановлення](#встановлення)
- [Токен](#токен)
- [Запуск](#запуск)
- [Структура проєкту](#структура-проєкту)
- [Розробка](#розробка)
- [Плани на майбутнє](#плани-на-майбутнє)
- [Contributing](#contributing)
- [Подяки](#подяки)
- [Ліцензія](#ліцензія)

## Встановлення

```bash
git clone https://github.com/HACKERGROUPS/CLI-Map-Alerts
cd CLI-Map-Alerts
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
