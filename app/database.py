import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Lấy DATABASE_URL từ biến môi trường của hệ thống (Render sẽ cấp biến này)
# Nếu không tìm thấy (khi chạy ở máy cá nhân), sẽ tự động dùng chuỗi localhost hiện tại của bạn.
DATABASE_URL = os.getenv(
    "postgresql://tutor:aFGlg9tRzFqxQeWf5zjeGMqnLtqlwnYU@dpg-d8k44sf7f7vs73btgg90-a.singapore-postgres.render.com/tutor_management_6z9i",
    "postgresql+psycopg2://tutor:tutor123@localhost:5432/tutor_management"
)

# 2. Xử lý sửa đổi nhỏ cho PostgreSQL trên một số môi trường Cloud
# Một số nền tảng (như Render/Heroku) thường cấp URL bắt đầu bằng "postgres://".
# Nhưng SQLAlchemy chuẩn mới yêu cầu phải là "postgresql://". Đoạn này giúp chuẩn hóa nó.
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Nếu bạn muốn sử dụng driver psycopg2 một cách tường minh trên Cloud:
if DATABASE_URL and not DATABASE_URL.startswith("postgresql+psycopg2://") and DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)


# 3. Khởi tạo Engine và Session như cấu hình ban đầu của bạn
engine = create_engine(
    DATABASE_URL
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()