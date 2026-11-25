import sqlite3
from dataclasses import dataclass
from datetime import date

from src.database import get_connection


@dataclass(frozen=True)
class Habit:
    id: int
    name: str
    created_at: str


def get_all_habits() -> list[Habit]:
    """Lấy danh sách tất cả thói quen theo thứ tự tạo."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, name, created_at FROM habits ORDER BY id ASC"
        ).fetchall()
    return [Habit(id=r["id"], name=r["name"], created_at=r["created_at"]) for r in rows]


def add_habit(name: str) -> tuple[bool, str]:
    """Thêm thói quen mới. Trả về (thành_công, thông_báo)."""
    cleaned_name = name.strip()
    if not cleaned_name:
        return False, "Tên thói quen không được để trống."

    try:
        with get_connection() as conn:
            conn.execute("INSERT INTO habits (name) VALUES (?)", (cleaned_name,))
        return True, f"Đã thêm thói quen '{cleaned_name}'."
    except sqlite3.IntegrityError:
        return False, f"Thói quen '{cleaned_name}' đã tồn tại."


def delete_habit(habit_id: int) -> None:
    """Xóa thói quen và toàn bộ lịch sử check-in liên quan (ON DELETE CASCADE)."""
    with get_connection() as conn:
        conn.execute("DELETE FROM habits WHERE id = ?", (habit_id,))


def get_completed_habit_ids_on_date(target_date: date) -> set[int]:
    """Trả về tập ID các thói quen đã hoàn thành trong một ngày cụ thể."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT habit_id FROM checkins WHERE checkin_date = ?",
            (target_date.isoformat(),),
        ).fetchall()
    return {row["habit_id"] for row in rows}


def set_checkin(habit_id: int, target_date: date, completed: bool) -> None:
    """Cập nhật trạng thái check-in cho một thói quen vào ngày chỉ định."""
    date_str = target_date.isoformat()
    with get_connection() as conn:
        if completed:
            conn.execute(
                "INSERT OR IGNORE INTO checkins (habit_id, checkin_date) VALUES (?, ?)",
                (habit_id, date_str),
            )
        else:
            conn.execute(
                "DELETE FROM checkins WHERE habit_id = ? AND checkin_date = ?",
                (habit_id, date_str),
            )


def get_checkin_dates_by_habit() -> dict[int, set[date]]:
    """Lấy toàn bộ ngày đã check-in, gom nhóm theo từng habit_id."""
    result: dict[int, set[date]] = {}
    with get_connection() as conn:
        rows = conn.execute("SELECT habit_id, checkin_date FROM checkins").fetchall()

    for row in rows:
        habit_id = row["habit_id"]
        checkin_date = date.fromisoformat(row["checkin_date"])
        result.setdefault(habit_id, set()).add(checkin_date)
    return result


def get_daily_completion_counts(start_date: date, end_date: date) -> dict[date, int]:
    """Đếm số lượng thói quen hoàn thành theo từng ngày trong khoảng [start_date, end_date]."""
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT checkin_date, COUNT(*) AS total
            FROM checkins
            WHERE checkin_date BETWEEN ? AND ?
            GROUP BY checkin_date
            """,
            (start_date.isoformat(), end_date.isoformat()),
        ).fetchall()

    return {date.fromisoformat(row["checkin_date"]): row["total"] for row in rows}
