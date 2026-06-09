import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.database import (
    engine,
    Base
)
# Đảm bảo các model được import để Base.metadata có thể nhận diện cấu trúc bảng khi khởi tạo
from app.models.student import Student
from app.routers.dashboard import (
    router as dashboard_router
)
from app.routers.lesson import (
    router as lesson_router
)
from app.routers.report import (
    router as report_router
)
from app.routers.schedule import (
    router as schedule_router
)
from app.routers.student import router as student_router
from app.routers.tuition import (
    router as tuition_router
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Tự động khởi tạo cấu trúc bảng nếu chưa tồn tại
    Base.metadata.create_all(bind=engine)

    # 2. Logic tự động nạp Seed Data
    try:
        # Sử dụng một connection trực tiếp từ engine để kiểm tra và thực thi SQL thuần
        with engine.connect() as connection:
            # Kiểm tra xem bảng students đã có dữ liệu chưa để tránh ghi đè/trùng lặp khi restart server
            result = connection.execute(text("SELECT COUNT(*) FROM students;")).scalar()
            
            if result == 0:
                print("--- 🗄️ Database trống. Đang tự động nạp dữ liệu khởi tạo (Seed Data)... ---")
                
                # Định vị đường dẫn chuẩn xác đến file seed.sql của bạn trong cấu trúc app/scripts/seed.sql
                current_dir = os.path.dirname(os.path.abspath(__file__))
                seed_file_path = os.path.join(current_dir, "scripts", "seed.sql")
                
                if os.path.exists(seed_file_path):
                    with open(seed_file_path, "r", encoding="utf-8") as f:
                        sql_script = f.read()
                    
                    # Thực thi toàn bộ script chứa nhiều câu lệnh SQL chèn dữ liệu
                    connection.execute(text(sql_script))
                    connection.commit()  # Xác nhận lưu thay đổi xuống Database
                    print("--- 🚀 Nạp dữ liệu khởi tạo thành công! ---")
                else:
                    print(f"⚠️ Cảnh báo: Không tìm thấy file script SQL tại đường dẫn: {seed_file_path}")
            else:
                print(f"--- 💡 Database hiện đã có {result} học sinh. Bỏ qua bước nạp Seed Data. ---")
                
    except Exception as e:
        print(f"❌ Có lỗi xảy ra trong quá trình nạp Seed Data: {e}")

    yield


app = FastAPI(
    lifespan=lifespan
)

# Tích hợp các hệ thống Router chức năng
app.include_router(student_router)
app.include_router(tuition_router)
app.include_router(lesson_router)
app.include_router(schedule_router)
app.include_router(report_router)
app.include_router(dashboard_router)

# Cấu hình CORS cho phép Frontend kết nối chéo cổng công khai
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "Tutor Management API"
    }