import sqlite3
from pathlib import Path

from app.models.schemas import AnalyticsSnapshot


class AnalyticsStore:
    def __init__(self, db_path: str) -> None:
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._init_db()

    def _init_db(self) -> None:
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS chat_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                user_message TEXT,
                assistant_message TEXT,
                latency_ms INTEGER,
                model TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.conn.commit()

    def log_chat(self, session_id: str, user_message: str, assistant_message: str, latency_ms: int, model: str) -> None:
        self.conn.execute(
            "INSERT INTO chat_logs(session_id, user_message, assistant_message, latency_ms, model) VALUES (?, ?, ?, ?, ?)",
            (session_id, user_message, assistant_message, latency_ms, model),
        )
        self.conn.commit()

    def snapshot(self) -> AnalyticsSnapshot:
        cur = self.conn.cursor()
        total_requests = cur.execute("SELECT COUNT(*) FROM chat_logs").fetchone()[0]
        avg_latency = cur.execute("SELECT COALESCE(AVG(latency_ms), 0) FROM chat_logs").fetchone()[0]
        top_sessions = [
            {"session_id": row[0], "count": row[1]}
            for row in cur.execute(
                "SELECT session_id, COUNT(*) as cnt FROM chat_logs GROUP BY session_id ORDER BY cnt DESC LIMIT 5"
            ).fetchall()
        ]
        return AnalyticsSnapshot(
            total_requests=total_requests,
            avg_latency_ms=round(float(avg_latency), 2),
            top_sessions=top_sessions,
        )
