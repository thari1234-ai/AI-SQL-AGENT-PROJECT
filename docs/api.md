# API Documentation (v1)

Base URL: `/api/v1`

## Auth
- `POST /auth/signup`
- `POST /auth/login`
- `GET /auth/me`

## Chat
- `POST /chat` -> returns SQL, explanations, insights, rows, chart metadata

## Query History
- `GET /history`
- `GET /history/{history_id}`
- `GET /history/{history_id}/export/csv`
- `GET /history/{history_id}/export/xlsx`

## Data Explorer
- `GET /explorer/tables`
- `GET /explorer/tables/{table_name}`

## Dashboards
- `GET /dashboards`
- `POST /dashboards`
- `POST /dashboards/{dashboard_id}/widgets`
