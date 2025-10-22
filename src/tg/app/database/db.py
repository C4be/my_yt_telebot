import aiosqlite

DB = "bot_users.db"


async def init_db():
    async with aiosqlite.connect(DB) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tg_id INTEGER NOT NULL UNIQUE,
            username TEXT,
            full_name TEXT,
            birthday DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP
        )
        """)
        await db.execute(
            "CREATE INDEX IF NOT EXISTS idx_users_birthday ON users(birthday)"
        )
        await db.commit()


async def upsert_user(
    db,
    tg_id: int,
    username: str | None,
    full_name: str | None,
    birthday: str | None,
    expires_at: str | None = None,
):
    await db.execute(
        """
    INSERT INTO users (tg_id, username, full_name, birthday, expires_at)
    VALUES (?, ?, ?, ?, ?)
    ON CONFLICT(tg_id) DO UPDATE SET
        username = excluded.username,
        full_name = excluded.full_name,
        birthday = excluded.birthday,
        expires_at = excluded.expires_at
    """,
        (tg_id, username, full_name, birthday, expires_at),
    )
    await db.commit()
