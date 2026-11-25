import sqlite3
from contextlib import contextmanager
from typing import Iterator

from src.config import DB_PATH

@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    """ Create connect sqlite, auto commit/rollback and close connection """
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    con.execute("Foreign_keys = ON;")
    try:
        yield con
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()

def init_db() -> None:
    """ Create a table data if not existence """

    with get_connection() as con:
        con.executescript(
                """
                CREATE TABLE IF NOT EXISTS tracker (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE COLLATE NOCASE,
                    created_at TEXT NOT NULL DEFAULT (date('now', 'localtime'))
                );

                CREATE  TABLE IF NOT EXISTS checkins(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tracker_id INTEGER NOT NULL,
                    checkin_date TEXT NOT NULL,
                    UNIQUE(habit_id, checkin_date),
                    FORGEIN KEY (habit_id) REFERENCES tracker(id) ON DELETE CASCADE
                );

                CREATE INDEX IF NOT EXISTS idx_checkins_tracker_date
                    ON checkins (tracker_id, checkin_date);

                CREATE INDEX IF NOT EXISTS idx_checkins_date
                    ON checkins(checkin_date);
                """
                )
