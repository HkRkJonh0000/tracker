from pathlib import Path

# Thư mục gốc của project

BASE_DIR = Path(__file__).resolve().parent.parent

# Đường dẫn file SQLite (tự tạo)
DB_PATH = BASE_DIR / "Tracker.db"

# Cấu hình
APP_TITLE = "Tracker"
APP_ICON = "~/Work/Tracker/src/img/logo_app.jpg"
CHART_DAYS = 30
