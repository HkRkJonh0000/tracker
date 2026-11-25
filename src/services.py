from dataclasses import dataclass
from datetime import date, timedelta

import pandas as pd

from src.repository import (
    Habit,
    get_all_habits,
    get_checkin_dates_by_habit,
    get_completed_habit_ids_on_date,
    get_daily_completion_counts,
)


@dataclass(frozen=True)
class HabitDailyItem:
    habit: Habit
    completed: bool
    streak: int


def calculate_streak(
    completed_dates: set[date], reference_date: date | None = None
) -> int:
    """
    Tính số ngày liên tiếp hoàn thành thói quen.
    Nếu hôm nay chưa check-in, sẽ bắt đầu tính ngược từ hôm qua
    để không bị mất chuỗi trong ngày.
    """
    today = reference_date or date.today()
    yesterday = today - timedelta(days=1)

    if today in completed_dates:
        cursor = today
    elif yesterday in completed_dates:
        cursor = yesterday
    else:
        return 0

    streak = 0
    while cursor in completed_dates:
        streak += 1
        cursor -= timedelta(days=1)

    return streak


def get_daily_habit_items(selected_date: date) -> list[HabitDailyItem]:
    """Tổng hợp danh sách thói quen kèm trạng thái check-in theo ngày chọn và streak hiện tại."""
    habits = get_all_habits()
    completed_today_ids = get_completed_habit_ids_on_date(selected_date)
    all_dates_map = get_checkin_dates_by_habit()

    items: list[HabitDailyItem] = []
    for habit in habits:
        habit_dates = all_dates_map.get(habit.id, set())
        items.append(
            HabitDailyItem(
                habit=habit,
                completed=habit.id in completed_today_ids,
                streak=calculate_streak(habit_dates),
            )
        )
    return items


def build_last_n_days_dataframe(
    days: int = 30, end_date: date | None = None
) -> pd.DataFrame:
    """Tạo DataFrame đầy đủ n ngày gần nhất (kể cả ngày có 0 check-in) để vẽ biểu đồ."""
    end = end_date or date.today()
    start = end - timedelta(days=days - 1)

    counts_map = get_daily_completion_counts(start, end)

    records = []
    for offset in range(days):
        current_day = start + timedelta(days=offset)
        records.append(
            {
                "Ngày": current_day,
                "Hoàn thành": counts_map.get(current_day, 0),
            }
        )

    return pd.DataFrame(records)
