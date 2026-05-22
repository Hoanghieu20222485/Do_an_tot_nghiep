# Do_an_tot_nghiep

## 📌 Giới thiệu đề tài

Đồ án tốt nghiệp:

> **Phát triển hệ thống trực quan hóa kết quả học tập và rèn luyện của sinh viên Trường Đại học Công nghệ Đông Á sử dụng Power BI và SQL Server nhằm hỗ trợ công tác quản lý và định hướng sinh viên**

Hệ thống được xây dựng nhằm hỗ trợ:
- Phân tích kết quả học tập sinh viên
- Theo dõi điểm rèn luyện
- Cảnh báo học tập
- Hỗ trợ nhà trường trong công tác quản lý và định hướng sinh viên


# 🏗️ Kiến trúc hệ thống

Python Faker
    ↓
Generate Fake Dataset
    ↓
SQL Server Data Warehouse
    ↓
Views / ETL / SQL Query
    ↓
Power BI Dashboard

⚙️ Công nghệ sử dụng
Công nghệ	Mục đích
Python	Sinh dữ liệu mô phỏng
Faker	Fake dữ liệu sinh viên
Pandas	Xử lý dữ liệu
SQL Server	Lưu trữ dữ liệu
SSMS	Quản lý database
Power BI	Dashboard trực quan
SQL	Truy vấn dữ liệu
Data Warehouse	Phân tích dữ liệu

📂 Cấu trúc project
student-analytics-powerbi/
│
├── faker/
│   ├── generate_students.py
│   ├── generate_scores.py
│
├── dataset/
│   ├── students.csv
│   ├── scores.csv
│
├── sql/
│   ├── create_tables.sql
│   ├── views.sql
│
├── powerbi/
│   ├── StudentDashboard.pbix
│
├── images/
│   ├── dashboard.png
│
├── report/
│   ├── DoAnTotNghiep.pdf
│
├── requirements.txt
│
└── README.md
🗄️ Data Warehouse

Hệ thống sử dụng mô hình:

Star Schema
Fact Table
Dimension Table
Dimension Tables
Dim_SinhVien
Dim_Khoa
Dim_Nganh
Dim_Lop
Dim_MonHoc
Dim_HocKy
Dim_ThoiGian
Fact Tables
Fact_KetQuaHocTap
Fact_RenLuyen

📊 Dashboard Features
Hệ thống dashboard hỗ trợ:
KPI tổng quan
GPA trung bình
Tỷ lệ sinh viên yếu/kém
Tỷ lệ cảnh báo học tập

Phân tích theo:
Khoa
Ngành
Lớp
Khóa học
Học kỳ
Drill Down dữ liệu
Filter tương tác
Dashboard trực quan

📈 Các biểu đồ sử dụng
KPI Card
Bar Chart
Line Chart
Pie Chart
Matrix
Slicer Filter

🧠 Các chức năng phân tích
Hệ thống hỗ trợ:
Phân tích xu hướng học tập
Theo dõi sinh viên có nguy cơ học lực yếu
So sánh kết quả giữa các khoa/ngành
Phân tích kết quả rèn luyện
Hỗ trợ quản lý đào tạo

📌 Dữ liệu sử dụng
Dataset được sinh tự động bằng:
Python Faker
Pandas

Dữ liệu mô phỏng:
Sinh viên
Môn học
Học kỳ
Điểm học tập
Điểm rèn luyện
trong nhiều năm học khác nhau.

📷 Dashboard Demo
Executive Overview
GPA trung bình
Tổng số sinh viên
Tỷ lệ cảnh báo học tập
Academic Analysis
Phân tích theo khoa/ngành/lớp
Xu hướng GPA theo thời gian
Training Analysis
Điểm rèn luyện
Xếp loại rèn luyện

📚 Kiến thức áp dụng
Business Intelligence (BI)
Data Warehouse
ETL
SQL Server
Power BI
Data Visualization
SQL Query Optimization

👨‍🎓 Sinh viên thực hiện
Hoàng Văn Hiếu
Trường Đại học Công nghệ Đông Á
Ngành Công nghệ thông tin

📄 License: Project phục vụ mục đích học tập và nghiên cứu.
