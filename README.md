# E-Ink Dashboard

A wall-mounted information and photo display built around a **Raspberry Pi Zero 2 W** and a **Waveshare 13.3" Spectra 6 (E) e-paper display**.

The goal is to combine useful everyday information with a digital photo frame in a clean, visually appealing dashboard.

## Features

The dashboard is planned to display:

* 📅 Current date and time
* 🌤️ Current weather
* 🌡️ Weather forecast
* 🌅 Sunrise and sunset
* 🚆 Public transport departures from the closest station
* 🏠 Room temperature
* 💧 Room humidity
* 📷 Random photo from a local photo collection
* ✈️ Countdown to the next holiday
* 🌙 Moon phase
* 📅 Upcoming calendar events
* 📸 Photo metadata such as location and camera

The color-capable Spectra 6 display allows weather icons, transport lines, photos, and other information to be displayed in color.

---

## Hardware

### Main components

* Raspberry Pi Zero 2 W
* Waveshare 13.3" e-Paper HAT+ (E) – Spectra 6
* Suitable power supply
* Temperature/humidity sensor
* Wall frame

### Display

The display is a **13.3" color e-paper display** with a resolution of:

```text
1600 × 1200 pixels
```

The display is intended to be mounted in a frame and used as a wall-mounted information display.

---

## Software Architecture

The application is written in **Python** and is separated into three main layers:

```text
┌──────────────────────────┐
│          DATA            │
│                          │
│ Weather                  │
│ Public transport         │
│ Sensors                  │
│ Holidays                 │
│ Photos                   │
│ Calendar                 │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│         LAYOUT           │
│                          │
│ Dashboard                │
│ Weather widget           │
│ Transport widget         │
│ Photo widget             │
│ Sensor widget            │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│        DISPLAY           │
│                          │
│ Waveshare Spectra 6      │
│ e-paper driver           │
└──────────────────────────┘
```

This separation keeps the application maintainable and makes it possible to change individual components without rewriting the entire application.

---

## Project Structure

```text
e-ink-dashboard/
│
├── main.py
├── config.py
├── requirements.txt
│
├── data/
│   ├── __init__.py
│   ├── weather.py
│   ├── transport.py
│   ├── sensors.py
│   ├── sun.py
│   ├── holidays.py
│   ├── calendar.py
│   └── photos.py
│
├── layout/
│   ├── __init__.py
│   ├── dashboard.py
│   ├── weather.py
│   ├── transport.py
│   ├── room.py
│   ├── sun.py
│   ├── holiday.py
│   ├── calendar.py
│   └── photo.py
│
├── display/
│   ├── __init__.py
│   └── driver.py
│
├── utils/
│   ├── __init__.py
│   ├── cache.py
│   ├── logger.py
│   └── time.py
│
├── assets/
│   ├── fonts/
│   ├── icons/
│   └── photos/
│
├── cache/
│
├── logs/
│
└── tests/
    ├── test_weather.py
    ├── test_transport.py
    └── test_layout.py
```

### `main.py`

The main application entry point.

It coordinates the different components:

```text
Get data
   ↓
Create dashboard
   ↓
Send image to display
```

### `data/`

Contains modules responsible for obtaining information.

Examples:

* `weather.py` → weather API
* `transport.py` → public transport data
* `sensors.py` → room temperature and humidity
* `sun.py` → sunrise/sunset and other solar information
* `holidays.py` → next holiday and countdown
* `calendar.py` → upcoming events
* `photos.py` → photo selection and metadata

### `layout/`

Contains the visual design of the dashboard.

Each widget is responsible for drawing one part of the screen.

### `display/`

Contains the hardware-specific code for the Waveshare display.

The rest of the application should not need to know how the Spectra 6 is controlled.

### `utils/`

Contains shared functionality such as:

* Caching
* Logging
* Time/date handling

### `assets/`

Contains static resources:

* Fonts
* Icons
* Photos

---

## Development

Development is primarily performed on a laptop using **Visual Studio Code**.

The Raspberry Pi is accessed remotely using **SSH / VS Code Remote SSH**.

Recommended workflow:

```text
Laptop
   │
   │ Development
   ▼
GitHub
   │
   │ Git
   ▼
Raspberry Pi Zero 2 W
   │
   ▼
Spectra 6 Display
```

The dashboard renderer should also be capable of generating a normal image file during development.

For example:

```text
Python
  ↓
Pillow
  ↓
dashboard.png
```

This allows the layout to be tested on the laptop without constantly refreshing the physical e-paper display.

On the Raspberry Pi:

```text
Python
  ↓
Pillow
  ↓
Waveshare driver
  ↓
Spectra 6
```

---

## Display Rendering

The dashboard is rendered using **Pillow**.

The target display resolution is:

```text
1600 × 1200
```

The renderer creates a complete image in memory before sending it to the e-paper display.

A simplified rendering process:

```python
weather = get_weather()
transport = get_departures()
room = get_room_data()
holiday = get_next_holiday()
photo = get_random_photo()

image = create_dashboard(
    weather,
    transport,
    room,
    holiday,
    photo
)

update_display(image)
```

---

## Data Update Strategy

Because e-paper displays consume significant time during a refresh and do not need constant updates, different information should be updated at different intervals.

| Information       | Suggested update |
| ----------------- | ---------------: |
| Current time      |      1–5 minutes |
| Public transport  |      1–2 minutes |
| Room temperature  |        5 minutes |
| Weather           |    15–30 minutes |
| Weather forecast  |    30–60 minutes |
| Sunrise/sunset    |     Once per day |
| Holiday countdown |     Once per day |
| Photo             |     Once per day |

The application should avoid refreshing the physical display when there has been no meaningful change.

---

## Caching

The dashboard should continue working when the internet connection is temporarily unavailable.

Data can be cached locally:

```text
cache/
├── weather.json
├── transport.json
├── sensors.json
└── sun.json
```

If an API request fails, the application can use the most recently cached information.

Example:

```text
Internet available
        │
        ▼
   Fetch new data
        │
        ▼
    Save cache
        │
        ▼
     Display
```

If the internet is unavailable:

```text
Internet unavailable
        │
        ▼
   Load cache
        │
        ▼
     Display
```

---

## Photo System

Photos are stored locally and selected automatically.

Possible organization:

```text
assets/photos/
├── landscape/
├── animals/
├── people/
└── travel/
```

The application can select a random photo or implement more advanced selection rules.

Possible future features:

* Random photo every morning
* Photo of the day
* Photo taken on this date in previous years
* Seasonal photos
* Travel photos when a holiday is approaching
* Photo metadata

Example metadata:

```text
Lauterbrunnen, Switzerland
Sony A7 IV
35 mm
f/8
1/250 s
ISO 100
```

---

## Configuration

User-specific settings should be stored in `config.py`.

Example:

```python
STATION = "Winterthur"

DISPLAY_WIDTH = 1600
DISPLAY_HEIGHT = 1200

WEATHER_UPDATE_MINUTES = 15
TRANSPORT_UPDATE_MINUTES = 2
SENSOR_UPDATE_MINUTES = 5

PHOTO_FOLDER = "assets/photos"
```

This prevents configuration values from being scattered throughout the application.

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd e-ink-dashboard
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

The Raspberry Pi also needs the Waveshare display library and the required system packages.

---

## Running the Dashboard

Run the application manually:

```bash
python3 main.py
```

During development, it can also be useful to generate a preview instead of updating the physical display.

Example:

```bash
python3 main.py --preview
```

This can generate:

```text
preview.png
```

which can be inspected directly on the development computer.

---

## Automatic Startup

Once the dashboard is stable, it should start automatically when the Raspberry Pi boots.

A `systemd` service can be used:

```text
Raspberry Pi boots
       ↓
systemd starts dashboard
       ↓
main.py
       ↓
collect data
       ↓
render dashboard
       ↓
update display
```

This allows the Raspberry Pi to run completely independently after installation.

---

## Future Ideas

Possible future additions include:

* 🌙 Moon phase and moonrise/moonset
* 🌧️ Rain radar
* 🌬️ Wind information
* 🌍 Air quality
* 🏠 CO₂ sensor
* 📅 Google Calendar integration
* ✈️ Flight information
* 🗺️ Travel destination weather
* 📸 Advanced photo selection
* 📰 News headlines
* 🏃 Fitness information
* 💤 Sleep information
* 🔔 Important notifications
* 🚨 Public transport disruptions
* 📊 Electricity/energy consumption
* 🌱 Plant information
* 📡 Internet connection status

---

## Design Principles

The project follows a few basic principles:

### Keep data separate from presentation

The weather module should provide weather data. It should not decide where the weather is displayed.

### Keep hardware-specific code isolated

Only the display driver should know about the Waveshare hardware.

### Optimize for e-paper

Avoid unnecessary full-screen refreshes.

### Design for offline operation

Temporary network failures should not break the dashboard.

### Develop on the laptop

The layout should be testable without requiring the physical Raspberry Pi.

### Keep the interface visually clean

The display is intended to function as both an information dashboard and a piece of wall art.

---

## Current Hardware

```text
Raspberry Pi Zero 2 W
        │
        │ SPI
        ▼
Waveshare 13.3" Spectra 6 HAT+ (E)
        │
        ▼
1600 × 1200 Color E-Paper Display
```

The finished system is intended to be mounted in a frame and permanently installed on a wall.

---

## Project Status

🚧 **In development**

Current focus:

1. Get the basic dashboard renderer working
2. Implement the Spectra 6 display driver
3. Create the static dashboard layout
4. Add weather
5. Add public transport
6. Add room temperature/humidity
7. Add photos
8. Add sunrise/sunset
9. Add holiday countdown
10. Add caching and automatic startup
