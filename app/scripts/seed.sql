-- 1. Xóa dữ liệu cũ nếu có để tránh trùng lặp khi chạy lại file
TRUNCATE TABLE tuitions RESTART IDENTITY CASCADE;
TRUNCATE TABLE students RESTART IDENTITY CASCADE;

-- 2. Chèn dữ liệu Students với ID cố định khớp hoàn toàn với bảng tuitions
INSERT INTO students (id, full_name, parent_name, parent_phone, note, session_fee, active) VALUES
(2, 'Linda', NULL, NULL, NULL, 150000, TRUE),
(3, 'Dâu', NULL, NULL, NULL, 150000, TRUE),
(4, 'Alina', NULL, NULL, NULL, 125000, TRUE),
(5, 'Benjamin', NULL, NULL, NULL, 150000, TRUE),
(6, 'Kayla', NULL, NULL, NULL, 150000, TRUE),
(7, 'Isaac', NULL, NULL, NULL, 150000, TRUE),
(8, 'Khang', NULL, NULL, NULL, 150000, TRUE),
(9, 'Gấu', NULL, NULL, NULL, 125000, TRUE),
(10, 'An', NULL, NULL, NULL, 150000, TRUE),
(11, 'Angela', NULL, NULL, NULL, 125000, TRUE),
(12, 'Vincent', NULL, NULL, NULL, 125000, TRUE),
(13, 'Vivian', NULL, NULL, NULL, 150000, TRUE),
(14, 'John', NULL, NULL, NULL, 150000, TRUE),
(15, 'Cici', NULL, NULL, NULL, 125000, TRUE),
(16, 'Dylan', NULL, NULL, NULL, 150000, TRUE),
(18, 'Ruby Luke', NULL, NULL, NULL, 138000, TRUE),
(19, 'Harper', NULL, NULL, NULL, 150000, TRUE),
(20, 'Linh Trúc', NULL, NULL, NULL, 150000, TRUE),
(21, 'Thomas', '', '', '', 150000, TRUE);

-- LƯU Ý CHO POSTGRESQL: Cập nhật lại giá trị sequence của cột ID tự tăng sau khi đã insert cứng
-- Điều này giúp các học sinh thêm mới tiếp theo sẽ nhận ID bắt đầu từ 22 thay vì bị trùng lặp lỗi.
SELECT setval(pg_get_serial_sequence('students', 'id'), COALESCE((SELECT MAX(id) FROM students), 1));

-- 3. Chèn dữ liệu học phí ban đầu
INSERT INTO tuitions (student_id, sessions_added, amount, payment_date, note) VALUES
(2, -1, 0, CURRENT_DATE, 'Initial remaining sessions'),
(3, 5, 0, CURRENT_DATE, 'Initial remaining sessions'),
(4, 11, 0, CURRENT_DATE, 'Initial remaining sessions'),
(5, 15, 0, CURRENT_DATE, 'Initial remaining sessions'),
(6, 3, 0, CURRENT_DATE, 'Initial remaining sessions'),
(7, 40, 0, CURRENT_DATE, 'Initial remaining sessions'),
(8, 14, 0, CURRENT_DATE, 'Initial remaining sessions'),
(9, 30, 0, CURRENT_DATE, 'Initial remaining sessions'),
(10, 23, 0, CURRENT_DATE, 'Initial remaining sessions'),
(11, 31, 0, CURRENT_DATE, 'Initial remaining sessions'),
(12, 17, 0, CURRENT_DATE, 'Initial remaining sessions'),
(13, 14, 0, CURRENT_DATE, 'Initial remaining sessions'),
(14, 5, 0, CURRENT_DATE, 'Initial remaining sessions'),
(15, 2, 0, CURRENT_DATE, 'Initial remaining sessions'),
(16, 14, 0, CURRENT_DATE, 'Initial remaining sessions'),
(18, 4, 0, CURRENT_DATE, 'Initial remaining sessions'),
(19, 23, 0, CURRENT_DATE, 'Initial remaining sessions'),
(20, 13, 0, CURRENT_DATE, 'Initial remaining sessions'),
(21, 0, 0, CURRENT_DATE, 'Initial remaining sessions');