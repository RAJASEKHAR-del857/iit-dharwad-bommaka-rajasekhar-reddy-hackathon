import json
import sqlite3
from pathlib import Path
from typing import Iterable
from ..schemas import RiskSignal

class SignalRepository:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS signals (
                signal_id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                source_type TEXT NOT NULL,
                event_type TEXT NOT NULL,
                impact_score INTEGER NOT NULL,
                sentiment_score REAL NOT NULL,
                payload TEXT NOT NULL
            )""")

    def _connect(self):
        return sqlite3.connect(self.path)

    def save_many(self, signals: Iterable[RiskSignal]) -> int:
        count = 0
        with self._connect() as conn:
            for signal in signals:
                payload = signal.model_dump_json()
                conn.execute("""INSERT OR REPLACE INTO signals
                    (signal_id, timestamp, source_type, event_type, impact_score, sentiment_score, payload)
                    VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (signal.signal_id, signal.timestamp.isoformat(), signal.source_type,
                     signal.event_type, signal.impact_score, signal.sentiment_score, payload))
                count += 1
        return count

    def list_signals(self, limit: int = 200) -> list[dict]:
        with self._connect() as conn:
            rows = conn.execute("SELECT payload FROM signals ORDER BY timestamp DESC LIMIT ?", (limit,)).fetchall()
        return [json.loads(row[0]) for row in rows]

    def clear(self):
        with self._connect() as conn:
            conn.execute("DELETE FROM signals")
