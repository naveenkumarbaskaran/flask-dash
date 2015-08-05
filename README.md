# flask-dash

Lightweight analytics dashboard built with Flask and Chart.js.

## Features
- Real-time visitor tracking
- Page view charts with Chart.js
- Top pages breakdown
- SQLite backend — zero config
- Bootstrap responsive UI
- Docker support

## Quick Start
```bash
pip install -r requirements.txt
python app.py
```

## Docker
```bash
docker build -t flask-dash .
docker run -p 5000:5000 flask-dash
```

## API
- `POST /api/track` — Record a page view
- `GET /api/stats` — Daily page view counts (last 30 days)
- `GET /api/top-pages` — Top 10 pages by views

## License
MIT
