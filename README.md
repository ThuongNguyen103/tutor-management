# Tutor Management System API

Hệ thống API quản lý học sinh và học phí dành cho gia sư, giúp tối ưu hóa việc theo dõi số buổi học, tiến độ đóng tiền và lập lịch dạy học hiệu quả.

---

## 📌 Mục lục

1. [Công nghệ sử dụng](#-công-nghệ-sử-dụng)
2. [Cấu trúc Module dự án](#-cấu-trúc-module-dự-án)
3. [Hướng dẫn cài đặt & Khởi chạy](#-hướng-dẫn-cài-đặt--khởi-chạy)
4. [Tài liệu API (API Documentation)](#-tài-liệu-api-api-documentation)

   * [Students APIs](#1-students-apis)
   * [Tuitions APIs](#2-tuitions-apis)
   * [Lessons APIs](#3-lessons-apis)
   * [Schedules APIs](#4-schedules-apis)
   * [Reports APIs](#5-reports-apis)
   * [Dashboard APIs](#6-dashboard-apis)
5. [Quy tắc Nghiệp vụ (Business Rules)](#-quy-tắc-nghiệp-vụ-business-rules)
6. [Định hướng phát triển (Future Improvements)](#-định-hướng-phát-triển-future-improvements)

---

## 🛠 Công nghệ sử dụng

* **Backend:** FastAPI + SQLAlchemy
* **Database:** PostgreSQL (Chạy trên Docker Container)
* **Frontend:** ReactJS *(Sắp triển khai)*

---

## 🗂 Cấu trúc Module dự án

Hệ thống bao gồm các module cốt lõi sau:

| Module        | Chức năng chính                                                        |
| ------------- | ---------------------------------------------------------------------- |
| **Students**  | Quản lý thông tin học sinh, thông tin phụ huynh.                       |
| **Tuitions**  | Quản lý lịch sử đóng học phí và số buổi học được thêm.                 |
| **Lessons**   | Ghi nhận nội dung, ngày học và trạng thái hoàn thành của từng buổi.    |
| **Schedules** | Quản lý thời khóa biểu, lịch dạy trong tuần.                           |
| **Reports**   | Thống kê, báo cáo tổng doanh thu và số lượng buổi dạy theo tháng.      |
| **Dashboard** | Cung cấp số liệu tổng quan nhanh về trạng thái hoạt động của hệ thống. |

---

## 🚀 Hướng dẫn cài đặt & Khởi chạy

### Base URL mặc định

```text
http://localhost:8000
```

### Tài liệu tương tác (Swagger UI)

Sau khi khởi chạy ứng dụng, bạn có thể truy cập đường dẫn sau để thử nghiệm API trực tiếp:

```text
http://localhost:8000/docs
```

### Các bước khởi chạy nhanh

#### Khởi động Database (PostgreSQL qua Docker)

```bash
docker run --name tutor-postgres \
-e POSTGRES_USER=postgres \
-e POSTGRES_PASSWORD=your_password \
-e POSTGRES_DB=tutor_db \
-p 5432:5432 \
-d postgres
```

#### Cài đặt thư viện Backend

```bash
pip install -r requirements.txt
```

#### Khởi chạy ứng dụng FastAPI

```bash
uvicorn main:app --reload
```

---

# 📑 Tài liệu API (API Documentation)

## 1. Students APIs

### Lấy danh sách toàn bộ học sinh

```http
GET /students
```

### Tạo học sinh mới

```http
POST /students
```

#### Request Body

```json
{
  "full_name": "Linda",
  "parent_name": "Parent",
  "parent_phone": "0900000000",
  "session_fee": 150000,
  "note": ""
}
```

### Lấy thông tin chi tiết học sinh

```http
GET /students/{student_id}
```

### Cập nhật thông tin học sinh

```http
PUT /students/{student_id}
```

### Xóa học sinh

```http
DELETE /students/{student_id}
```

### Tính số buổi còn lại của học sinh

```http
GET /students/{student_id}/remaining-sessions
```

#### Response Example

```json
{
  "student_id": 1,
  "student_name": "Linda",
  "remaining_sessions": 8
}
```

### Danh sách học sinh sắp hết buổi

```http
GET /students/low-balance
```

#### Response Example

```json
[
  {
    "student_name": "Angela",
    "remaining_sessions": 2
  }
]
```

### Lấy lịch sử buổi học của học sinh

```http
GET /students/{student_id}/lessons
```

### Lấy thời khóa biểu của học sinh

```http
GET /students/student/{student_id}
```

### Danh sách học sinh chưa xếp lịch học

```http
GET /students/without-schedule
```

### Danh sách học sinh đã hết hoặc âm buổi

```http
GET /students/out-of-sessions
```

---

## 2. Tuitions APIs

### Lấy toàn bộ lịch sử đóng học phí

```http
GET /tuitions
```

### Thêm bản ghi học phí mới

```http
POST /tuitions
```

#### Request Body

```json
{
  "student_id": 1,
  "sessions_added": 10,
  "amount": 1500000,
  "payment_date": "2026-06-01",
  "note": "June payment"
}
```

### Xem chi tiết một lần đóng học phí

```http
GET /tuitions/{tuition_id}
```

### Cập nhật thông tin học phí

```http
PUT /tuitions/{tuition_id}
```

### Xóa bản ghi học phí

```http
DELETE /tuitions/{tuition_id}
```

### Lấy lịch sử đóng học phí riêng của từng học sinh

```http
GET /tuitions/student/{student_id}
```

---

## 3. Lessons APIs

### Lấy danh sách tất cả các buổi học

```http
GET /lessons
```

### Tạo buổi học mới (Điểm danh / Ghi nhận nội dung)

```http
POST /lessons
```

#### Request Body

```json
{
  "student_id": 1,
  "lesson_date": "2026-06-01",
  "content": "Present Simple",
  "completed": true
}
```

### Lấy thông tin chi tiết buổi học

```http
GET /lessons/{lesson_id}
```

### Cập nhật nội dung buổi học

```http
PUT /lessons/{lesson_id}
```

### Xóa buổi học

```http
DELETE /lessons/{lesson_id}
```

---

## 4. Schedules APIs

### Lấy lịch học của ngày hôm nay

```http
GET /schedules/today
```

### Lấy lịch học theo ngày bất kỳ

(Hệ thống tự động tính toán Thứ trong tuần dựa trên ngày truyền vào)

```http
GET /schedules/by-date?date=2026-06-01
```

### Lấy toàn bộ lịch học tuần (Từ Thứ 2 đến Chủ Nhật)

```http
GET /schedules/week
```

### Lấy danh sách tất cả lịch học

```http
GET /schedules
```

### Tạo lịch học mới

```http
POST /schedules
```

#### Request Body

```json
{
  "student_id": 1,
  "day_of_week": 2,
  "start_time": "15:00",
  "end_time": "16:00"
}
```

### Quy ước day_of_week

| Giá trị | Thứ tương ứng |
| ------- | ------------- |
| 1       | Thứ 2         |
| 2       | Thứ 3         |
| 3       | Thứ 4         |
| 4       | Thứ 5         |
| 5       | Thứ 6         |
| 6       | Thứ 7         |
| 7       | Chủ Nhật      |

### Lấy chi tiết một lịch học

```http
GET /schedules/{schedule_id}
```

### Cập nhật lịch học

```http
PUT /schedules/{schedule_id}
```

### Xóa lịch học

```http
DELETE /schedules/{schedule_id}
```

### Tổng hợp lịch học hôm nay cho Dashboard

```http
GET /schedules/dashboard/today
```

---

## 5. Reports APIs

### Báo cáo doanh thu theo tháng

```http
GET /reports/monthly-revenue?month=6&year=2026
```

#### Response Example

```json
{
  "month": 6,
  "year": 2026,
  "revenue": 5500000
}
```

### Thống kê số lượng buổi học đã dạy trong tháng

```http
GET /reports/monthly-lessons?month=6&year=2026
```

#### Response Example

```json
{
  "month": 6,
  "year": 2026,
  "total_lessons": 87
}
```

---

## 6. Dashboard APIs

### Lấy số liệu tổng quan nhanh

```http
GET /dashboard
```

#### Response Example

```json
{
  "total_students": 19,
  "active_students": 19,
  "today_lessons": 5,
  "students_low_balance": 3,
  "students_out_of_sessions": 2,
  "monthly_revenue": 5500000
}
```

---

# 📋 Quy tắc Nghiệp vụ (Business Rules)

### Tính số buổi còn lại (remaining_sessions)

    $$
    \text{Số buổi còn lại} =
    \text{Tổng số buổi đã mua}
    --------------------------

    \text{Số buổi học đã hoàn thành}
    $$

    ### Cảnh báo sắp hết buổi (Low Balance)

    Trạng thái kích hoạt khi học sinh có số buổi còn lại ít hơn hoặc bằng 3:

    $$
    \text{remaining_sessions} \le 3
    $$

    ### Hết hoặc âm buổi (Out Of Sessions)

    Trạng thái kích hoạt khi số buổi học sinh dùng đã hết hoặc vượt quá số buổi đã đóng tiền:

    $$
    \text{remaining_sessions} \le 0
    $$
