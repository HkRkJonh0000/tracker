# Tracker

Ứng dụng theo dõi thói quen, viết bằng ngôn ngữ **Python** và **Streamlit**. Dữ liệu được lưu cục bộ bằng **SQLite**.


## Tính năng

- Thêm và xóa thói quen
- Check-in theo ngày, có thể chọn lại những ngày trước 
- Đếm số ngày liên tiếp hoàn thành cho từng thói quen
- Biểu đồ số thói quen hoàn thành trong 30 ngày gần nhất
- Dữ liệu được lưu lại, tắt và mở app vẫn còn

## Môi trường sử dụng

| Thành phần | Công nghệ |
| --- | --- |
| Ngôn ngữ | Python 3.14.4 |
| Giao diện | Streamlit |
| Xử lý dữ liệu, biểu đồ | pandas|
| Cơ sở dữ liệu | SQLite (sử dụng thư viện có sẵn trong python "sqlite3") |
