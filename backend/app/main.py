from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.db import get_mongo_db, get_pg_pool


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pg_pool = await get_pg_pool()
    async with app.state.pg_pool.acquire() as conn:
        await conn.execute(
            "CREATE TABLE IF NOT EXISTS items (id SERIAL PRIMARY KEY, name TEXT NOT NULL)"
        )
    yield
    await app.state.pg_pool.close()


app = FastAPI(title="cicdlearn-api", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/items")
async def list_items():
    pool = app.state.pg_pool
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT id, name FROM items ORDER BY id")
    return [{"id": r["id"], "name": r["name"]} for r in rows]


@app.post("/items")
async def create_item(name: str):
    pool = app.state.pg_pool
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "INSERT INTO items (name) VALUES ($1) RETURNING id, name",
            name,
        )
    return {"id": row["id"], "name": row["name"]}


@app.get("/events")
async def list_events():
    db = get_mongo_db()
    cursor = db.events.find().sort("_id", -1).limit(100)
    events = await cursor.to_list(length=100)
    return [
        {"id": str(e["_id"]), "message": e.get("message", "")}
        for e in events
    ]


@app.post("/events")
async def create_event(message: str):
    db = get_mongo_db()
    result = await db.events.insert_one({"message": message})
    return {"id": str(result.inserted_id), "message": message}
