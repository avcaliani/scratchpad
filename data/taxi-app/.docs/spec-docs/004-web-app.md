---
status: done
created: 2026-05-12
updated: 2026-05-14
---

# 4. Web App

**Stack:** HTML · Alpine.js (CDN) · TailwindCSS (CDN)  
**Purpose:** Single HTML file. No build step. Served as a static asset by FastAPI.

---

## Search Screen

- Text input for `trip_id`
- Search button
- On submit: call `GET /api/trips/{trip_id}`
- Show loading state while request is in flight

---

## Results View

Display all 16 response fields. Format:
- Timestamps: human-readable local datetime
- Fare and distance: 2 decimal places
- Quality flags: colored badges — `false` = green, `true` = red
- `record_quality_status`: prominent badge — `VALID` = green, `INVALID` = red

---

## Error States

| Scenario | Message |
|---|---|
| `404` | "Trip not found." |
| `400` | "Invalid trip ID format." |
| `503` | "Service unavailable. Try again shortly." |
| Network failure | "Could not reach the API." |
