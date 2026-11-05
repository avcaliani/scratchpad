# Web Sockets

The Dunder Mifflin PA System: an intercom chat and a Schrute Bucks ticker over FastAPI WebSockets.

### How to run

```bash
cd back-end/fast-api/web-sockets
uv run uvicorn main:app --reload
```

Then open the page in your browser (the API only serves the sockets):

```bash
open client/index.html
```

### Endpoints

```bash
/ws/intercom    # send a line, get a JSON reply from a random employee. Send `close` to hang up.
/ws/ticker      # a `check-in` or `redeem` JSON event every 1, 3 or 5 seconds.
```

---

[FastAPI: WebSockets](https://fastapi.tiangolo.com/advanced/websockets/) / [Starlette: WebSockets](https://www.starlette.dev/websockets/)
