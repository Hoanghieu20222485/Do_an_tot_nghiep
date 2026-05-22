# -*- coding: utf-8 -*-
"""
Sinh dữ liệu giả lập Data Warehouse cho đề tài:
Phát triển hệ thống trực quan hóa kết quả học tập và rèn luyện của sinh viên
Trường Đại học Công nghệ Đông Á sử dụng Power BI và SQL Server.

Cài đặt:
    pip install faker pandas numpy

Chạy:
    python generate_eaut_student_dw_v9_dim_hocky.py

Kết quả:
    Thư mục output_dw/ chứa các file CSV UTF-8-SIG.
    Sau đó chạy import_dw_to_sqlserver_v8_model_moi.py để import vào SQL Server.
"""

from __future__ import annotations

import os
import random
from datetime import date
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from faker import Faker

# =====================================================
# 0. THIẾT LẬP CHUNG
# =====================================================

fake = Faker("vi_VN")
Faker.seed(2026)
random.seed(2026)
np.random.seed(2026)

OUTPUT_DIR = "output_dw"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# =====================================================
# 1. CẤU HÌNH KỊCH BẢN THEO BẢN CHỐT
# =====================================================

KHOA_DATA = [
    (1, "KTCN", "Khoa Công nghệ thông tin"),
    (2, "XD", "Khoa Xây dựng"),
    (3, "DL", "Khoa Du lịch"),
    (4, "LUAT", "Khoa Luật"),
    (5, "DUOC", "Khoa Dược"),
]

NGANH_DATA = [
    (1, "CNTT", "Công nghệ thông tin", 1),
    (2, "TKDH", "Thiết kế đồ họa", 1),
    (3, "AIUD", "Trí tuệ nhân tạo ứng dụng", 1),
    (4, "KT", "Kiến trúc", 2),
    (5, "KTNT", "Kiến trúc nội thất", 2),
    (6, "KTXD", "Kỹ thuật xây dựng", 2),
    (7, "QTKS", "Quản trị khách sạn", 3),
    (8, "QTDL", "Quản trị du lịch và lữ hành", 3),
    (9, "LUAT", "Luật", 4),
    (10, "DUOC", "Dược học", 5),
]

# Theo kịch bản: khóa 13 năm 4, khóa 14 năm 3, khóa 15 năm 2, khóa 16 năm 1.
# Mỗi phần tử là tuple: (HocKyKey thực tế trong Dim_HocKy, HocKyDuKien trong CTĐT).
# Cách ánh xạ này giúp sinh viên khóa sau có điểm đúng theo năm học thực tế,
# tránh tình trạng dashboard lọc năm học hiện tại nhưng sinh viên mới bị “hồ sơ rỗng”.
KHOA_HOC_TO_HK = {
    13: [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8)],
    14: [(3, 1), (4, 2), (5, 3), (6, 4), (7, 5), (8, 6)],
    15: [(5, 1), (6, 2), (7, 3), (8, 4)],
    16: [(7, 1), (8, 2)],
}
KHOA_HOC_TO_NAM_SV = {13: 4, 14: 3, 15: 2, 16: 1}

# Có thêm NgayBatDauHocKy / NgayKetThucHocKy kiểu date để Power BI tính theo năm,
# ví dụ: tổng sinh viên năm trước, YoY, filter theo Date Table.
# Mốc ngày giữ đúng logic 4 năm học, mỗi năm 2 kỳ:
# - Học kỳ 1: 01/09 đến 15/01 năm sau
# - Học kỳ 2: 01/02 đến 30/06 cùng năm kết thúc năm học
HOC_KY_DATA = [
    (1, "HK01", "2022-2023", "Học kỳ 1", "2022-2023 - Học kỳ 1", date(2022, 9, 1), date(2023, 1, 15)),
    (2, "HK02", "2022-2023", "Học kỳ 2", "2022-2023 - Học kỳ 2", date(2023, 2, 1), date(2023, 6, 30)),
    (3, "HK03", "2023-2024", "Học kỳ 1", "2023-2024 - Học kỳ 1", date(2023, 9, 1), date(2024, 1, 15)),
    (4, "HK04", "2023-2024", "Học kỳ 2", "2023-2024 - Học kỳ 2", date(2024, 2, 1), date(2024, 6, 30)),
    (5, "HK05", "2024-2025", "Học kỳ 1", "2024-2025 - Học kỳ 1", date(2024, 9, 1), date(2025, 1, 15)),
    (6, "HK06", "2024-2025", "Học kỳ 2", "2024-2025 - Học kỳ 2", date(2025, 2, 1), date(2025, 6, 30)),
    (7, "HK07", "2025-2026", "Học kỳ 1", "2025-2026 - Học kỳ 1", date(2025, 9, 1), date(2026, 1, 15)),
    (8, "HK08", "2025-2026", "Học kỳ 2", "2025-2026 - Học kỳ 2", date(2026, 2, 1), date(2026, 6, 30)),
]

# Tỷ lệ giới tính theo khoa đúng kịch bản thực tế
GENDER_BY_KHOA = {
    1: {"Nam": 0.73, "Nữ": 0.27},
    2: {"Nam": 0.70, "Nữ": 0.30},
    3: {"Nam": 0.45, "Nữ": 0.55},
    4: {"Nam": 0.60, "Nữ": 0.40},
    5: {"Nam": 0.33, "Nữ": 0.67},
}

# Hồ sơ ngành: GPA, tỷ lệ đạt, điểm rèn luyện cộng/trừ
NGANH_PROFILE = {
    "CNTT": dict(mean=3.02, pass_rate=0.91, rl_bonus=0, risk_bonus=0.00),
    "TKDH": dict(mean=3.05, pass_rate=0.90, rl_bonus=2, risk_bonus=-0.02),
    "AIUD": dict(mean=2.95, pass_rate=0.88, rl_bonus=0, risk_bonus=0.025),
    "KT": dict(mean=2.90, pass_rate=0.86, rl_bonus=0, risk_bonus=0.025),
    "KTNT": dict(mean=2.94, pass_rate=0.88, rl_bonus=1, risk_bonus=0.02),
    "KTXD": dict(mean=2.78, pass_rate=0.86, rl_bonus=-1, risk_bonus=0.04),
    "QTKS": dict(mean=2.92, pass_rate=0.87, rl_bonus=6, risk_bonus=-0.02),
    "QTDL": dict(mean=2.88, pass_rate=0.86, rl_bonus=7, risk_bonus=-0.02),
    "LUAT": dict(mean=2.98, pass_rate=0.89, rl_bonus=1, risk_bonus=0.02),
    "DUOC": dict(mean=3.04, pass_rate=0.93, rl_bonus=-1, risk_bonus=0.05),
}

CLASS_LEVELS = {
    "Tốt": dict(gpa_bonus=0.25, warning_rate=0.06),
    "Trung bình": dict(gpa_bonus=0.00, warning_rate=0.11),
    "Yếu": dict(gpa_bonus=-0.35, warning_rate=0.17),
}

ABILITY_BONUS = {
    # Cân lại để tỷ lệ học lực toàn trường gần kịch bản:
    # Xuất sắc 5-8%, Giỏi 12-18%, Khá 35-45%, Trung bình 25-35%, Yếu 6-12%.
    # Không để nhóm "Yếu" kéo điểm quá thấp, vì kịch bản yêu cầu tỷ lệ yếu chỉ 5-15%.
    "Xuất sắc": 0.04,
    "Giỏi": 0.09,
    "Khá": 0.03,
    "Trung bình": -0.12,
    "Yếu": -0.38,
}

ABILITY_WEIGHTS = [6, 14, 43, 29, 8]

# GPA theo tiến trình: năm 3 khó nhất, năm 4 tăng nhẹ với SV khá/giỏi nhưng vẫn có nhóm chậm tiến độ
SEMESTER_EFFECT = {1: 0.10, 2: 0.06, 3: -0.01, 4: -0.04, 5: -0.08, 6: -0.05, 7: 0.04, 8: 0.08}

# =====================================================
# 2. CHƯƠNG TRÌNH ĐÀO TẠO 10 NGÀNH, 8 HỌC KỲ
#    Cấu trúc tuple: (Tên môn, Số tín chỉ, Loại môn)
# =====================================================

COURSE_PLAN: Dict[str, Dict[int, List[Tuple[str, int, str]]]] = {
    "CNTT": {
        1: [("Nhập môn Công nghệ thông tin", 3, "Cơ sở ngành"), ("Tin học cơ sở", 3, "Kiến thức chung"), ("Toán rời rạc", 3, "Cơ sở ngành"), ("Kỹ năng học đại học", 2, "Kiến thức chung")],
        2: [("Lập trình C", 3, "Cơ sở ngành"), ("Cấu trúc dữ liệu và giải thuật", 3, "Cơ sở ngành"), ("Cơ sở dữ liệu", 3, "Cơ sở ngành"), ("Mạng máy tính cơ bản", 3, "Cơ sở ngành")],
        3: [("Lập trình hướng đối tượng", 3, "Chuyên ngành"), ("Hệ điều hành", 3, "Chuyên ngành"), ("Phân tích thiết kế hệ thống", 3, "Chuyên ngành"), ("Thiết kế Web", 3, "Chuyên ngành")],
        4: [("SQL Server", 3, "Chuyên ngành"), ("Lập trình Web nâng cao", 3, "Chuyên ngành"), ("Java Programming", 3, "Chuyên ngành"), ("Quản trị mạng", 3, "Chuyên ngành")],
        5: [("Công nghệ phần mềm", 3, "Chuyên ngành"), ("Lập trình .NET", 3, "Chuyên ngành"), ("An toàn bảo mật thông tin", 3, "Chuyên ngành"), ("Điện toán đám mây", 3, "Chuyên ngành")],
        6: [("Phát triển ứng dụng di động", 3, "Chuyên ngành"), ("Kho dữ liệu và BI", 3, "Chuyên ngành"), ("Power BI và trực quan hóa dữ liệu", 3, "Chuyên ngành"), ("Kiểm thử phần mềm", 2, "Chuyên ngành")],
        7: [("Machine Learning cơ bản", 3, "Chuyên ngành"), ("DevOps cơ bản", 2, "Chuyên ngành"), ("Thực tập doanh nghiệp", 4, "Thực tập"), ("Chuyên đề công nghệ mới", 2, "Chuyên ngành")],
        8: [("Đồ án tốt nghiệp", 6, "Đồ án"), ("Kỹ năng khởi nghiệp CNTT", 2, "Chuyên ngành")],
    },
    "TKDH": {
        1: [("Nhập môn Thiết kế đồ họa", 3, "Cơ sở ngành"), ("Mỹ thuật cơ bản", 3, "Cơ sở ngành"), ("Nguyên lý thị giác", 2, "Cơ sở ngành"), ("Tin học ứng dụng", 2, "Kiến thức chung")],
        2: [("Adobe Photoshop", 3, "Cơ sở ngành"), ("Adobe Illustrator", 3, "Cơ sở ngành"), ("Typography", 2, "Cơ sở ngành"), ("Thiết kế bố cục", 3, "Cơ sở ngành")],
        3: [("Thiết kế nhận diện thương hiệu", 3, "Chuyên ngành"), ("Adobe InDesign", 3, "Chuyên ngành"), ("Thiết kế UI/UX", 3, "Chuyên ngành"), ("Thiết kế Banner và Poster", 2, "Chuyên ngành")],
        4: [("Thiết kế Website", 3, "Chuyên ngành"), ("Dựng video cơ bản", 3, "Chuyên ngành"), ("Motion Graphics", 3, "Chuyên ngành"), ("Nhiếp ảnh kỹ thuật số", 2, "Chuyên ngành")],
        5: [("Thiết kế 3D cơ bản", 3, "Chuyên ngành"), ("Dựng phim và hậu kỳ", 3, "Chuyên ngành"), ("Thiết kế quảng cáo số", 3, "Chuyên ngành"), ("Thiết kế bao bì sản phẩm", 2, "Chuyên ngành")],
        6: [("Thiết kế App Mobile", 3, "Chuyên ngành"), ("UX Research", 2, "Chuyên ngành"), ("Thiết kế truyền thông đa phương tiện", 3, "Chuyên ngành"), ("Digital Marketing cơ bản", 2, "Chuyên ngành")],
        7: [("Portfolio cá nhân", 3, "Đồ án"), ("Chuyên đề thiết kế sáng tạo", 2, "Chuyên ngành"), ("Thực tập doanh nghiệp", 4, "Thực tập"), ("Thiết kế dự án thực tế", 3, "Đồ án")],
        8: [("Đồ án tốt nghiệp", 6, "Đồ án"), ("Khởi nghiệp ngành sáng tạo", 2, "Chuyên ngành")],
    },
    "AIUD": {
        1: [("Nhập môn Trí tuệ nhân tạo", 3, "Cơ sở ngành"), ("Python cơ bản", 3, "Cơ sở ngành"), ("Toán cho AI", 3, "Cơ sở ngành"), ("Kỹ năng học đại học", 2, "Kiến thức chung")],
        2: [("Python nâng cao", 3, "Cơ sở ngành"), ("Cấu trúc dữ liệu và giải thuật", 3, "Cơ sở ngành"), ("Xác suất thống kê", 3, "Cơ sở ngành"), ("Cơ sở dữ liệu", 3, "Cơ sở ngành")],
        3: [("Machine Learning", 3, "Chuyên ngành"), ("Deep Learning cơ bản", 3, "Chuyên ngành"), ("Xử lý dữ liệu", 3, "Chuyên ngành"), ("Trực quan hóa dữ liệu", 2, "Chuyên ngành")],
        4: [("Computer Vision", 3, "Chuyên ngành"), ("Xử lý ngôn ngữ tự nhiên", 3, "Chuyên ngành"), ("Khai phá dữ liệu", 3, "Chuyên ngành"), ("Mạng nơ-ron nhân tạo", 3, "Chuyên ngành")],
        5: [("Big Data cơ bản", 3, "Chuyên ngành"), ("AI trong doanh nghiệp", 3, "Chuyên ngành"), ("Hệ chuyên gia", 2, "Chuyên ngành"), ("Điện toán đám mây cho AI", 3, "Chuyên ngành")],
        6: [("MLOps cơ bản", 3, "Chuyên ngành"), ("Phân tích dữ liệu với Power BI", 3, "Chuyên ngành"), ("AIoT cơ bản", 2, "Chuyên ngành"), ("An toàn dữ liệu AI", 2, "Chuyên ngành")],
        7: [("Generative AI", 3, "Chuyên ngành"), ("Chuyên đề AI hiện đại", 2, "Chuyên ngành"), ("Thực tập doanh nghiệp", 4, "Thực tập"), ("Dự án AI thực tế", 3, "Đồ án")],
        8: [("Đồ án tốt nghiệp", 6, "Đồ án"), ("Khởi nghiệp công nghệ AI", 2, "Chuyên ngành")],
    },
    "KT": {
        1: [("Nhập môn Kiến trúc", 3, "Cơ sở ngành"), ("Mỹ thuật cơ bản", 3, "Cơ sở ngành"), ("Hình họa kiến trúc", 3, "Cơ sở ngành"), ("Kỹ năng học đại học", 2, "Kiến thức chung")],
        2: [("Vẽ kỹ thuật xây dựng", 3, "Cơ sở ngành"), ("AutoCAD cơ bản", 3, "Cơ sở ngành"), ("Cơ sở tạo hình kiến trúc", 3, "Cơ sở ngành"), ("Lịch sử kiến trúc", 2, "Cơ sở ngành")],
        3: [("Thiết kế kiến trúc nhà ở", 3, "Chuyên ngành"), ("Vật liệu xây dựng", 3, "Cơ sở ngành"), ("Kết cấu công trình cơ bản", 3, "Cơ sở ngành"), ("SketchUp và 3D Modeling", 2, "Chuyên ngành")],
        4: [("Thiết kế công trình công cộng", 3, "Chuyên ngành"), ("Quy hoạch đô thị", 3, "Chuyên ngành"), ("Kiến trúc cảnh quan", 3, "Chuyên ngành"), ("Revit Architecture", 3, "Chuyên ngành")],
        5: [("Thiết kế kiến trúc nâng cao", 3, "Chuyên ngành"), ("BIM trong xây dựng", 3, "Chuyên ngành"), ("Kỹ thuật thi công công trình", 3, "Chuyên ngành"), ("Thiết kế chiếu sáng kiến trúc", 2, "Chuyên ngành")],
        6: [("Hồ sơ kỹ thuật kiến trúc", 3, "Chuyên ngành"), ("Quản lý dự án xây dựng", 3, "Chuyên ngành"), ("Thiết kế xanh và bền vững", 2, "Chuyên ngành"), ("Pháp luật xây dựng", 2, "Chuyên ngành")],
        7: [("Chuyên đề kiến trúc hiện đại", 3, "Chuyên ngành"), ("Thực tập doanh nghiệp", 4, "Thực tập"), ("Thiết kế đồ án kiến trúc tổng hợp", 3, "Đồ án"), ("Khởi nghiệp ngành xây dựng", 2, "Chuyên ngành")],
        8: [("Đồ án tốt nghiệp", 6, "Đồ án"), ("Chuyên đề công trình thực tế", 2, "Chuyên ngành")],
    },
    "KTNT": {
        1: [("Nhập môn Kiến trúc nội thất", 3, "Cơ sở ngành"), ("Mỹ thuật cơ bản", 3, "Cơ sở ngành"), ("Nguyên lý thiết kế nội thất", 3, "Cơ sở ngành"), ("Tin học ứng dụng", 2, "Kiến thức chung")],
        2: [("Vẽ kỹ thuật nội thất", 3, "Cơ sở ngành"), ("AutoCAD nội thất", 3, "Cơ sở ngành"), ("Màu sắc và ánh sáng", 2, "Cơ sở ngành"), ("Lịch sử nội thất", 2, "Cơ sở ngành")],
        3: [("Thiết kế nội thất nhà ở", 3, "Chuyên ngành"), ("Vật liệu nội thất", 3, "Chuyên ngành"), ("SketchUp nội thất", 3, "Chuyên ngành"), ("Trang trí không gian", 2, "Chuyên ngành")],
        4: [("Thiết kế nội thất văn phòng", 3, "Chuyên ngành"), ("Thiết kế nội thất thương mại", 3, "Chuyên ngành"), ("3Ds Max cơ bản", 3, "Chuyên ngành"), ("Revit Interior", 2, "Chuyên ngành")],
        5: [("Thiết kế ánh sáng nội thất", 3, "Chuyên ngành"), ("Thiết kế đồ nội thất", 3, "Chuyên ngành"), ("Dựng phối cảnh 3D", 3, "Chuyên ngành"), ("Thiết kế không gian xanh", 2, "Chuyên ngành")],
        6: [("BIM nội thất", 3, "Chuyên ngành"), ("Quản lý dự án nội thất", 3, "Chuyên ngành"), ("Thiết kế showroom", 2, "Chuyên ngành"), ("Pháp luật xây dựng và nội thất", 2, "Chuyên ngành")],
        7: [("Chuyên đề thiết kế nội thất hiện đại", 3, "Chuyên ngành"), ("Thực tập doanh nghiệp", 4, "Thực tập"), ("Dự án nội thất thực tế", 3, "Đồ án"), ("Khởi nghiệp ngành sáng tạo", 2, "Chuyên ngành")],
        8: [("Đồ án tốt nghiệp", 6, "Đồ án"), ("Portfolio thiết kế nội thất", 2, "Đồ án")],
    },
    "KTXD": {
        1: [("Nhập môn Kỹ thuật xây dựng", 3, "Cơ sở ngành"), ("Toán kỹ thuật", 3, "Cơ sở ngành"), ("Vật lý xây dựng", 3, "Cơ sở ngành"), ("Kỹ năng học đại học", 2, "Kiến thức chung")],
        2: [("Cơ học kỹ thuật", 3, "Cơ sở ngành"), ("Vẽ kỹ thuật xây dựng", 3, "Cơ sở ngành"), ("AutoCAD xây dựng", 3, "Cơ sở ngành"), ("Vật liệu xây dựng", 3, "Cơ sở ngành")],
        3: [("Sức bền vật liệu", 3, "Chuyên ngành"), ("Kết cấu bê tông cốt thép", 3, "Chuyên ngành"), ("Trắc địa công trình", 3, "Chuyên ngành"), ("Địa chất công trình", 2, "Chuyên ngành")],
        4: [("Kỹ thuật thi công", 3, "Chuyên ngành"), ("Kết cấu thép", 3, "Chuyên ngành"), ("Nền móng công trình", 3, "Chuyên ngành"), ("Revit Structure", 2, "Chuyên ngành")],
        5: [("Dự toán xây dựng", 3, "Chuyên ngành"), ("Quản lý chất lượng công trình", 3, "Chuyên ngành"), ("BIM trong xây dựng", 3, "Chuyên ngành"), ("An toàn lao động xây dựng", 2, "Chuyên ngành")],
        6: [("Quản lý dự án xây dựng", 3, "Chuyên ngành"), ("Kỹ thuật cầu đường cơ bản", 3, "Chuyên ngành"), ("Giám sát thi công", 3, "Chuyên ngành"), ("Pháp luật xây dựng", 2, "Chuyên ngành")],
        7: [("Chuyên đề công nghệ xây dựng mới", 3, "Chuyên ngành"), ("Thực tập doanh nghiệp", 4, "Thực tập"), ("Thiết kế công trình thực tế", 3, "Đồ án"), ("Khởi nghiệp ngành xây dựng", 2, "Chuyên ngành")],
        8: [("Đồ án tốt nghiệp", 6, "Đồ án"), ("Chuyên đề công trình xanh", 2, "Chuyên ngành")],
    },
    "QTKS": {
        1: [("Nhập môn Quản trị khách sạn", 3, "Cơ sở ngành"), ("Tổng quan du lịch và dịch vụ", 3, "Cơ sở ngành"), ("Kỹ năng giao tiếp", 2, "Kiến thức chung"), ("Tin học ứng dụng", 2, "Kiến thức chung")],
        2: [("Nghiệp vụ lễ tân", 3, "Cơ sở ngành"), ("Nghiệp vụ buồng phòng", 3, "Cơ sở ngành"), ("Tâm lý khách hàng", 2, "Cơ sở ngành"), ("Tiếng Anh chuyên ngành khách sạn 1", 3, "Cơ sở ngành")],
        3: [("Quản trị nhà hàng", 3, "Chuyên ngành"), ("Nghiệp vụ phục vụ bàn", 3, "Chuyên ngành"), ("Quản trị nhân sự khách sạn", 3, "Chuyên ngành"), ("Marketing du lịch", 2, "Chuyên ngành")],
        4: [("Quản trị chất lượng dịch vụ", 3, "Chuyên ngành"), ("Quản trị sự kiện", 3, "Chuyên ngành"), ("Kế toán khách sạn", 3, "Chuyên ngành"), ("Tiếng Anh chuyên ngành khách sạn 2", 3, "Chuyên ngành")],
        5: [("Quản trị resort và spa", 3, "Chuyên ngành"), ("Quản trị doanh thu khách sạn", 3, "Chuyên ngành"), ("Văn hóa ẩm thực", 2, "Chuyên ngành"), ("Phần mềm quản lý khách sạn", 2, "Chuyên ngành")],
        6: [("Quản trị chiến lược khách sạn", 3, "Chuyên ngành"), ("Chăm sóc khách hàng cao cấp", 2, "Chuyên ngành"), ("Quản trị tài chính khách sạn", 3, "Chuyên ngành"), ("Pháp luật du lịch và khách sạn", 2, "Chuyên ngành")],
        7: [("Thực tập khách sạn", 4, "Thực tập"), ("Chuyên đề quản trị khách sạn hiện đại", 3, "Chuyên ngành"), ("Quản lý vận hành khách sạn thực tế", 3, "Đồ án"), ("Khởi nghiệp ngành dịch vụ", 2, "Chuyên ngành")],
        8: [("Đồ án tốt nghiệp", 6, "Đồ án"), ("Kỹ năng quản lý và lãnh đạo", 2, "Chuyên ngành")],
    },
    "QTDL": {
        1: [("Nhập môn Quản trị du lịch và lữ hành", 3, "Cơ sở ngành"), ("Tổng quan du lịch Việt Nam", 3, "Cơ sở ngành"), ("Kỹ năng giao tiếp và thuyết trình", 2, "Kiến thức chung"), ("Tin học ứng dụng", 2, "Kiến thức chung")],
        2: [("Địa lý du lịch", 3, "Cơ sở ngành"), ("Văn hóa du lịch", 3, "Cơ sở ngành"), ("Tâm lý khách du lịch", 2, "Cơ sở ngành"), ("Tiếng Anh chuyên ngành du lịch 1", 3, "Cơ sở ngành")],
        3: [("Nghiệp vụ hướng dẫn du lịch", 3, "Chuyên ngành"), ("Thiết kế và điều hành tour", 3, "Chuyên ngành"), ("Marketing du lịch", 3, "Chuyên ngành"), ("Kỹ năng tổ chức sự kiện", 2, "Chuyên ngành")],
        4: [("Quản trị doanh nghiệp lữ hành", 3, "Chuyên ngành"), ("Quản trị nhân sự du lịch", 3, "Chuyên ngành"), ("Du lịch bền vững", 2, "Chuyên ngành"), ("Tiếng Anh chuyên ngành du lịch 2", 3, "Chuyên ngành")],
        5: [("Du lịch quốc tế", 3, "Chuyên ngành"), ("Quản trị điểm đến du lịch", 3, "Chuyên ngành"), ("Nghiệp vụ thanh toán và vé máy bay", 2, "Chuyên ngành"), ("Phần mềm quản lý tour", 2, "Chuyên ngành")],
        6: [("Quản trị chất lượng dịch vụ du lịch", 3, "Chuyên ngành"), ("Tổ chức sự kiện du lịch", 3, "Chuyên ngành"), ("Pháp luật du lịch", 2, "Chuyên ngành"), ("Chăm sóc khách hàng du lịch", 2, "Chuyên ngành")],
        7: [("Thực tập doanh nghiệp du lịch", 4, "Thực tập"), ("Chuyên đề du lịch hiện đại", 3, "Chuyên ngành"), ("Điều hành tour thực tế", 3, "Đồ án"), ("Khởi nghiệp ngành du lịch", 2, "Chuyên ngành")],
        8: [("Đồ án tốt nghiệp", 6, "Đồ án"), ("Kỹ năng quản lý và lãnh đạo", 2, "Chuyên ngành")],
    },
    "LUAT": {
        1: [("Nhập môn ngành Luật", 3, "Cơ sở ngành"), ("Lý luận Nhà nước và Pháp luật", 3, "Cơ sở ngành"), ("Hiến pháp Việt Nam", 3, "Cơ sở ngành"), ("Kỹ năng học đại học", 2, "Kiến thức chung")],
        2: [("Luật Dân sự 1", 3, "Cơ sở ngành"), ("Luật Hành chính", 3, "Cơ sở ngành"), ("Luật Hình sự 1", 3, "Cơ sở ngành"), ("Logic học pháp lý", 2, "Cơ sở ngành")],
        3: [("Luật Dân sự 2", 3, "Chuyên ngành"), ("Luật Hình sự 2", 3, "Chuyên ngành"), ("Luật Lao động", 3, "Chuyên ngành"), ("Kỹ năng tranh tụng cơ bản", 2, "Chuyên ngành")],
        4: [("Luật Thương mại", 3, "Chuyên ngành"), ("Luật Tố tụng dân sự", 3, "Chuyên ngành"), ("Luật Đất đai", 3, "Chuyên ngành"), ("Tiếng Anh pháp lý", 2, "Chuyên ngành")],
        5: [("Luật Doanh nghiệp", 3, "Chuyên ngành"), ("Luật Quốc tế", 3, "Chuyên ngành"), ("Luật Sở hữu trí tuệ", 2, "Chuyên ngành"), ("Pháp luật hợp đồng", 2, "Chuyên ngành")],
        6: [("Luật Tố tụng hình sự", 3, "Chuyên ngành"), ("Luật Hôn nhân và gia đình", 3, "Chuyên ngành"), ("Pháp luật tài chính ngân hàng", 2, "Chuyên ngành"), ("Kỹ năng tư vấn pháp luật", 2, "Chuyên ngành")],
        7: [("Chuyên đề pháp luật hiện đại", 3, "Chuyên ngành"), ("Thực tập nghề luật", 4, "Thực tập"), ("Giải quyết tranh chấp thương mại", 3, "Chuyên ngành"), ("Đạo đức nghề nghiệp luật", 2, "Chuyên ngành")],
        8: [("Đồ án / Khóa luận tốt nghiệp", 6, "Đồ án"), ("Kỹ năng hành nghề luật sư", 2, "Chuyên ngành")],
    },
    "DUOC": {
        1: [("Nhập môn Dược học", 3, "Cơ sở ngành"), ("Hóa đại cương", 3, "Cơ sở ngành"), ("Sinh học đại cương", 3, "Cơ sở ngành"), ("Kỹ năng học đại học", 2, "Kiến thức chung")],
        2: [("Hóa hữu cơ", 3, "Cơ sở ngành"), ("Giải phẫu sinh lý", 3, "Cơ sở ngành"), ("Thực vật dược", 2, "Cơ sở ngành"), ("Tin học ứng dụng trong y dược", 2, "Kiến thức chung")],
        3: [("Hóa phân tích", 3, "Chuyên ngành"), ("Vi sinh ký sinh trùng", 3, "Chuyên ngành"), ("Dược liệu học", 3, "Chuyên ngành"), ("Sinh hóa", 2, "Chuyên ngành")],
        4: [("Dược lý học 1", 3, "Chuyên ngành"), ("Bào chế học", 3, "Chuyên ngành"), ("Kiểm nghiệm thuốc", 3, "Chuyên ngành"), ("Tiếng Anh chuyên ngành dược", 2, "Chuyên ngành")],
        5: [("Dược lý học 2", 3, "Chuyên ngành"), ("Quản lý tồn trữ thuốc", 2, "Chuyên ngành"), ("Pháp chế dược", 2, "Chuyên ngành"), ("Dược lâm sàng cơ bản", 3, "Chuyên ngành")],
        6: [("Công nghệ sản xuất thuốc", 3, "Chuyên ngành"), ("Kiểm soát chất lượng thuốc", 3, "Chuyên ngành"), ("Marketing dược phẩm", 2, "Chuyên ngành"), ("Quản trị nhà thuốc", 2, "Chuyên ngành")],
        7: [("Thực tập bệnh viện và nhà thuốc", 4, "Thực tập"), ("Chuyên đề dược hiện đại", 3, "Chuyên ngành"), ("Tư vấn sử dụng thuốc an toàn", 2, "Chuyên ngành"), ("Khởi nghiệp ngành dược", 2, "Chuyên ngành")],
        8: [("Đồ án / Khóa luận tốt nghiệp", 6, "Đồ án"), ("Đạo đức nghề nghiệp dược", 2, "Chuyên ngành")],
    },
}

HARD_KEYWORDS = [
    "Cấu trúc dữ liệu", "Cơ sở dữ liệu", "Lập trình hướng đối tượng", "SQL Server",
    "Machine Learning", "Deep Learning", "Xử lý ngôn ngữ tự nhiên", "Mạng nơ-ron", "Computer Vision",
    "Sức bền vật liệu", "Kết cấu bê tông cốt thép", "Nền móng", "Kết cấu thép",
    "Dược lý", "Kiểm nghiệm thuốc", "Hóa phân tích", "Hóa hữu cơ", "Kiểm soát chất lượng thuốc",
    "Kỹ năng tranh tụng", "Luật Tố tụng dân sự", "Luật Tố tụng hình sự",
]

EASY_KEYWORDS = [
    "Kỹ năng", "Nhập môn", "Tin học", "Tiếng Anh", "Thực tập", "Đồ án", "Khóa luận",
    "Portfolio", "Khởi nghiệp", "Chuyên đề", "Tổng quan",
]

# =====================================================
# 2.1. CHUẨN HÓA MÔN HỌC TƯƠNG ĐƯƠNG
# =====================================================
# Mục tiêu: các môn giống nhau về bản chất dùng chung 1 MonHocKey trong Dim_MonHoc,
# còn Dim_ChuongTrinhDaoTao vẫn giữ quan hệ ngành - môn - học kỳ như cũ.
# Chỉ gom các môn có cùng bản chất và cùng số tín chỉ phổ biến để không làm sai logic CTĐT.


def normalize_course_name(ten_mon: str) -> str:
    """Quy chuyển tên môn tương đương về tên chuẩn dùng chung trong Dim_MonHoc."""
    name = ten_mon.strip()
    lower = name.lower()

    # Nhóm tốt nghiệp: Đồ án / Khóa luận tốt nghiệp đều xem chung là Đồ án tốt nghiệp.
    if "tốt nghiệp" in lower and ("đồ án" in lower or "khóa luận" in lower):
        return "Đồ án tốt nghiệp"

    # Nhóm thực tập: tên theo ngành khác nhau nhưng bản chất là thực tập cuối khóa/doanh nghiệp.
    if lower.startswith("thực tập"):
        return "Thực tập doanh nghiệp"

    # Nhóm khởi nghiệp: cùng là học phần khởi nghiệp theo ngành.
    if "khởi nghiệp" in lower:
        return "Khởi nghiệp"

    # Nhóm kỹ năng chung.
    if lower in {"kỹ năng giao tiếp", "kỹ năng giao tiếp và thuyết trình"}:
        return "Kỹ năng giao tiếp"

    # Nhóm tin học ứng dụng 2 tín chỉ. Không gộp Tin học cơ sở 3 tín chỉ vì khác khối lượng.
    if lower in {"tin học ứng dụng", "tin học ứng dụng trong y dược"}:
        return "Tin học ứng dụng"

    # Nhóm tiếng Anh chuyên ngành theo lĩnh vực.
    if lower.startswith("tiếng anh chuyên ngành"):
        return "Tiếng Anh chuyên ngành"

    # Nhóm pháp luật chuyên ngành 2 tín chỉ.
    if lower in {
        "pháp luật xây dựng",
        "pháp luật xây dựng và nội thất",
        "pháp luật du lịch",
        "pháp luật du lịch và khách sạn",
    }:
        return "Pháp luật chuyên ngành"

    # Nhóm quản lý dự án 3 tín chỉ.
    if lower in {"quản lý dự án xây dựng", "quản lý dự án nội thất"}:
        return "Quản lý dự án"

    # Nhóm BIM 3 tín chỉ.
    if lower in {"bim trong xây dựng", "bim nội thất"}:
        return "BIM"

    # Nhóm AutoCAD 3 tín chỉ.
    if lower in {"autocad cơ bản", "autocad nội thất", "autocad xây dựng"}:
        return "AutoCAD"

    # Nhóm vẽ kỹ thuật 3 tín chỉ.
    if lower in {"vẽ kỹ thuật xây dựng", "vẽ kỹ thuật nội thất"}:
        return "Vẽ kỹ thuật"

    # Nhóm vật liệu 3 tín chỉ.
    if lower in {"vật liệu xây dựng", "vật liệu nội thất"}:
        return "Vật liệu chuyên ngành"

    # Nhóm phần mềm quản lý trong du lịch/khách sạn 2 tín chỉ.
    if lower in {"phần mềm quản lý khách sạn", "phần mềm quản lý tour"}:
        return "Phần mềm quản lý dịch vụ"

    # Nhóm chăm sóc khách hàng 2 tín chỉ.
    if lower in {"chăm sóc khách hàng cao cấp", "chăm sóc khách hàng du lịch"}:
        return "Chăm sóc khách hàng"

    return name

QUE_QUAN = [
    "Hà Nội", "Hải Phòng", "Bắc Ninh", "Hải Dương", "Nam Định", "Thái Bình",
    "Ninh Bình", "Thanh Hóa", "Nghệ An", "Phú Thọ", "Hưng Yên", "Quảng Ninh",
    "Vĩnh Phúc", "Bắc Giang", "Hà Nam", "Thái Nguyên",
]


# Năm nhập học theo khóa, khớp với Dim_HocKy:
# Khóa 13 bắt đầu năm học 2022-2023, khóa 14 bắt đầu 2023-2024,
# khóa 15 bắt đầu 2024-2025, khóa 16 bắt đầu 2025-2026.
KHOA_HOC_TO_NAM_NHAP_HOC = {13: 2022, 14: 2023, 15: 2024, 16: 2025}


def ngay_nhap_hoc_theo_khoa(khoa_hoc_num: int) -> date:
    """Sinh ngày nhập học phù hợp với khóa, trong khoảng 01/08 - 30/09.

    Khoảng này đảm bảo ngày nhập học không sau quá 2 tháng so với mốc bắt đầu
    học kỳ 1 (01/09) và phù hợp để tạo bảng thời gian trong Power BI.
    """
    nam = KHOA_HOC_TO_NAM_NHAP_HOC[khoa_hoc_num]
    return fake.date_between_dates(date(nam, 8, 1), date(nam, 9, 30))

# =====================================================
# 3. HÀM PHỤ TRỢ
# =====================================================

def clamp(x: float, low: float, high: float) -> float:
    return max(low, min(high, x))


def weighted_gender(khoa_key: int) -> str:
    ratios = GENDER_BY_KHOA[khoa_key]
    return random.choices(["Nam", "Nữ"], weights=[ratios["Nam"], ratios["Nữ"]])[0]


def diem_to_letter(score: float) -> Tuple[str, float, str]:
    if score >= 8.5:
        return "A", 4.0, "Đạt"
    if score >= 7.0:
        return "B", 3.0, "Đạt"
    if score >= 5.5:
        return "C", 2.0, "Đạt"
    if score >= 4.0:
        return "D", 1.0, "Đạt"
    return "F", 0.0, "Không đạt"


def xep_loai_hoc_tap(gpa: float) -> int:
    if gpa >= 3.6:
        return 1
    if gpa >= 3.2:
        return 2
    if gpa >= 2.5:
        return 3
    if gpa >= 2.0:
        return 4
    return 5


def xep_loai_ren_luyen(score: int) -> int:
    if score >= 90:
        return 1
    if score >= 80:
        return 2
    if score >= 65:
        return 3
    if score >= 50:
        return 4
    return 5


def canh_bao(gpa_hk: float, gpa_tich_luy: float, tc_khong_dat: int, diem_rl: int) -> str:
    if gpa_hk < 1.5 or tc_khong_dat > 9 or diem_rl < 50:
        return "Cảnh báo nghiêm trọng"
    if gpa_hk < 1.8 or tc_khong_dat >= 6:
        return "Cảnh báo trung bình"
    if gpa_hk < 2.0 or tc_khong_dat >= 3 or gpa_tich_luy < 2.0:
        return "Cảnh báo nhẹ"
    return "Không cảnh báo"


def course_difficulty(course_name: str, loai_mon: str) -> str:
    name = course_name.lower()
    if any(k.lower() in name for k in HARD_KEYWORDS):
        return "Khó"
    if loai_mon in ["Thực tập", "Đồ án"] or any(k.lower() in name for k in EASY_KEYWORDS):
        return "Dễ"
    return "Trung bình"


def score_from_target_gpa(target_gpa: float, difficulty: str, nganh_pass_rate: float) -> float:
    """Tạo điểm hệ 10 theo GPA mục tiêu, độ khó môn, và tỷ lệ đạt đặc thù ngành."""
    # Quy đổi GPA mục tiêu sang thang 10 ở mức thực tế hơn.
    # Nếu để base quá cao, dữ liệu sẽ bị "đẹp" bất thường và thiếu nhóm cảnh báo.
    # Công thức mới nâng nhẹ nền điểm để tỷ lệ học lực yếu không vượt kịch bản 5-15%.
    # Với GPA mục tiêu khoảng 2.5-3.0, điểm hệ 10 thường rơi vào 6.8-7.8.
    base10 = 3.78 + target_gpa * 1.25
    pass_adjust = (nganh_pass_rate - 0.82) * 1.6
    base10 += pass_adjust

    if difficulty == "Dễ":
        base10 += 0.25
        sd = 0.70
    elif difficulty == "Khó":
        base10 -= 0.55
        sd = 1.05
    else:
        sd = 0.90

    # Tạo đuôi điểm thấp để có nợ môn/học lại thực tế, nhất là môn khó
    if difficulty == "Khó" and random.random() < 0.045:
        base10 -= random.uniform(0.8, 1.8)
    elif difficulty == "Trung bình" and random.random() < 0.020:
        base10 -= random.uniform(0.5, 1.2)

    return round(clamp(np.random.normal(base10, sd), 0, 10), 1)



def fail_probability(difficulty: str, ability: str, class_level: str, nganh_pass_rate: float, nam_dao_tao: int, loai_mon: str) -> float:
    """Xác suất trượt môn theo độ khó, năng lực SV, chất lượng lớp và đặc thù ngành.

    Hàm này giúp dữ liệu không bị quá đẹp:
    - Môn dễ vẫn có một tỷ lệ nhỏ sinh viên rớt do vắng thi/lý do cá nhân.
    - Môn trung bình có một phần sinh viên phải thi lại/học lại.
    - Môn khó tạo ra nợ tín chỉ rõ hơn, nhất là ở năm 2-3 và nhóm học lực yếu.
    """
    base = {"Dễ": 0.020, "Trung bình": 0.070, "Khó": 0.200}.get(difficulty, 0.070)

    ability_adj = {
        "Xuất sắc": -0.020,
        "Giỏi": -0.018,
        "Khá": -0.010,
        "Trung bình": 0.020,
        "Yếu": 0.090,
    }.get(ability, 0.0)

    class_adj = {
        "Tốt": -0.012,
        "Trung bình": 0.000,
        "Yếu": 0.025,
    }.get(class_level, 0.0)

    # Ngành có pass_rate thấp hơn 0.82 sẽ bị tăng xác suất trượt.
    nganh_adj = (0.82 - nganh_pass_rate) * 0.25

    # Năm 3 thường là giai đoạn chuyên ngành khó nhất; năm 1 nhẹ hơn.
    year_adj = -0.012 if nam_dao_tao == 1 else (0.020 if nam_dao_tao == 3 else 0.0)

    # Thực tập/đồ án thường dễ đạt hơn nhưng vẫn có nhóm chậm tiến độ.
    loai_adj = -0.018 if loai_mon in ["Thực tập", "Đồ án"] else 0.0

    return clamp(base + ability_adj + class_adj + nganh_adj + year_adj + loai_adj, 0.005, 0.42)


def score_from_failure(difficulty: str, ability: str) -> float:
    """Sinh điểm rớt môn có chủ đích, tránh tất cả điểm F dồn sát 3.9."""
    center = {"Dễ": 3.3, "Trung bình": 3.0, "Khó": 2.6}.get(difficulty, 3.0)
    if ability in ["Trung bình", "Yếu"]:
        center -= 0.25
    return round(clamp(np.random.normal(center, 0.75), 0.0, 3.9), 1)


def recovered_debt_credits(current_debt: int, ability: str, hoc_ky_du_kien: int) -> int:
    """Mô phỏng sinh viên thi lại/học lại để giảm số tín chỉ nợ lũy kế.

    Fact_KetQuaHocTap vẫn giữ grain 1 SV - 1 môn - 1 học kỳ chính khóa.
    Phần phục hồi nợ được phản ánh ở Fact_TongKetHocKy.SoTinChiNoLuyKe để dashboard
    không hiểu sai rằng tất cả môn từng rớt đều còn nợ đến cuối khóa.
    """
    if current_debt <= 0:
        return 0

    base_prob = {
        "Xuất sắc": 0.75,
        "Giỏi": 0.68,
        "Khá": 0.58,
        "Trung bình": 0.42,
        "Yếu": 0.25,
    }.get(ability, 0.45)

    # Năm cuối sinh viên thường tập trung trả nợ môn để xét tốt nghiệp.
    if hoc_ky_du_kien in [7, 8]:
        base_prob += 0.18
    elif hoc_ky_du_kien in [5, 6]:
        base_prob += 0.06

    if random.random() > clamp(base_prob, 0.05, 0.92):
        return 0

    max_recover = 6 if hoc_ky_du_kien >= 5 else 4
    possible = [tc for tc in [2, 3, 4, 6] if tc <= current_debt and tc <= max_recover]
    if not possible:
        return min(current_debt, max_recover)

    return random.choice(possible)

def split_score(total: float) -> Tuple[float, float, float, float]:
    cc = clamp(np.random.normal(total + 0.5, 0.75), 0, 10)
    gk = clamp(np.random.normal(total + 0.1, 0.95), 0, 10)
    ck_center = (total - cc * 0.1 - gk * 0.2) / 0.7
    ck = clamp(np.random.normal(ck_center, 0.35), 0, 10)
    final = round(cc * 0.1 + gk * 0.2 + ck * 0.7, 1)
    return round(cc, 1), round(gk, 1), round(ck, 1), final


def ma_mon_from_name(mon_key: int, ten_mon: str) -> str:
    prefix = "MH"
    if "luật" in ten_mon.lower():
        prefix = "LAW"
    elif any(x in ten_mon.lower() for x in ["dược", "hóa", "thuốc", "sinh"]):
        prefix = "PHA"
    elif any(x in ten_mon.lower() for x in ["xây", "kiến", "bim", "autocad", "revit"]):
        prefix = "CON"
    elif any(x in ten_mon.lower() for x in ["du lịch", "khách sạn", "tour", "lữ hành"]):
        prefix = "TOU"
    elif any(x in ten_mon.lower() for x in ["python", "lập trình", "data", "ai", "web", "sql", "power bi"]):
        prefix = "IT"
    return f"{prefix}{mon_key:04d}"

# =====================================================
# 4. TẠO DIMENSION
# =====================================================

dim_khoa = pd.DataFrame(KHOA_DATA, columns=["KhoaKey", "MaKhoa", "TenKhoa"])
dim_nganh = pd.DataFrame(NGANH_DATA, columns=["NganhKey", "MaNganh", "TenNganh", "KhoaKey"])
dim_hocky = pd.DataFrame(
    HOC_KY_DATA,
    columns=[
        "HocKyKey", "MaHocKy", "NamHoc", "HocKy", "TenHocKy",
        "NgayBatDauHocKy", "NgayKetThucHocKy",
    ],
)

# Dim_HocKy là bảng thời gian chính của mô hình.
# Tất cả fact đều nối trực tiếp bằng HocKyKey để tránh blank và tránh filter năm làm mất dữ liệu.
def date_to_key(d: date) -> int:
    return int(pd.Timestamp(d).strftime("%Y%m%d"))

# =====================================================
# Dim_HocKy tối ưu, dùng chung cho tất cả bảng fact
# -----------------------------------------------------
# Chỉ giữ các cột thực sự cần cho Power BI:
# - HocKyKey: khóa chính nối với mọi fact.
# - NamHoc / HocKyLabel: dùng làm slicer, trục biểu đồ.
# - ThuTuHocKy: dùng Sort by column và tính kỳ trước.
# - NgayBatDauHocKy / NgayKetThucHocKy: dùng phân tích theo thời gian.
# - NamKetThucHocKy: dùng lọc năm, tính YoY theo năm kết thúc học kỳ.
# =====================================================
dim_hocky["NgayBatDauHocKy"] = pd.to_datetime(dim_hocky["NgayBatDauHocKy"])
dim_hocky["NgayKetThucHocKy"] = pd.to_datetime(dim_hocky["NgayKetThucHocKy"])

dim_hocky["HocKySo"] = dim_hocky["HocKy"].str.extract(r"(\d+)").astype(int)
dim_hocky["HocKyLabel"] = dim_hocky["NamHoc"] + " - HK" + dim_hocky["HocKySo"].astype(str)
dim_hocky["ThuTuHocKy"] = dim_hocky["HocKyKey"].astype(int)
dim_hocky["NamKetThucHocKy"] = dim_hocky["NgayKetThucHocKy"].dt.year
dim_hocky["IsHocKyMoiNhat"] = dim_hocky["HocKyKey"].eq(dim_hocky["HocKyKey"].max()).astype(int)

# Bảng học kỳ gọn nhất để tránh chọn nhầm cột trong Power BI.
dim_hocky = dim_hocky[[
    "HocKyKey",
    "MaHocKy",
    "NamHoc",
    "HocKySo",
    "TenHocKy",
    "HocKyLabel",
    "ThuTuHocKy",
    "NgayBatDauHocKy",
    "NgayKetThucHocKy",
    "NamKetThucHocKy",
    "IsHocKyMoiNhat",
]]

dim_canhbao = pd.DataFrame([
    (1, "Không cảnh báo", 0, "Sinh viên không có dấu hiệu rủi ro học vụ"),
    (2, "Cảnh báo nhẹ", 1, "GPA hoặc tín chỉ nợ bắt đầu dưới ngưỡng an toàn"),
    (3, "Cảnh báo trung bình", 2, "GPA thấp hoặc nợ tín chỉ ở mức cần can thiệp"),
    (4, "Cảnh báo nghiêm trọng", 3, "Nguy cơ cao do GPA rất thấp, nợ tín chỉ nhiều hoặc rèn luyện yếu"),
], columns=["CanhBaoKey", "TenCanhBao", "MucDo", "MoTa"])

CANH_BAO_KEY = {row.TenCanhBao: int(row.CanhBaoKey) for row in dim_canhbao.itertuples(index=False)}

dim_xl_ht = pd.DataFrame([
    (1, "Xuất sắc", 3.60, 4.00),
    (2, "Giỏi", 3.20, 3.59),
    (3, "Khá", 2.50, 3.19),
    (4, "Trung bình", 2.00, 2.49),
    (5, "Yếu", 0.00, 1.99),
], columns=["XepLoaiHocTapKey", "TenXepLoai", "DiemTu", "DiemDen"])

dim_xl_rl = pd.DataFrame([
    (1, "Xuất sắc", 90, 100),
    (2, "Tốt", 80, 89),
    (3, "Khá", 65, 79),
    (4, "Trung bình", 50, 64),
    (5, "Yếu", 0, 49),
], columns=["XepLoaiRenLuyenKey", "TenXepLoai", "DiemTu", "DiemDen"])

# Giảng viên: mỗi khoa 12 giảng viên, một giảng viên có thể dạy nhiều lớp/môn
hoc_vi = ["ThS", "ThS", "ThS", "TS", "TS", "PGS.TS"]
gv_rows = []
gv_key = 1
for khoa_key, ma_khoa, _ in KHOA_DATA:
    for _i in range(12):
        gv_rows.append((gv_key, f"GV{gv_key:04d}", fake.name(), random.choice(hoc_vi), khoa_key))
        gv_key += 1
dim_giangvien = pd.DataFrame(gv_rows, columns=["GiangVienKey", "MaGiangVien", "HoTenGiangVien", "HocVi", "KhoaKey"])

# Môn học và chương trình đào tạo
# Môn trùng tên dùng chung một MonHocKey để Dim_MonHoc không bị lặp vô nghĩa.
monhoc_map: Dict[str, int] = {}
monhoc_rows = []
ctdt_rows = []
mon_key = 1
ctdt_key = 1

for nganh_key, ma_nganh, _ten_nganh, _khoa_key in NGANH_DATA:
    for hoc_ky_du_kien in range(1, 9):
        for ten_mon, tin_chi, loai_mon in COURSE_PLAN[ma_nganh][hoc_ky_du_kien]:
            ten_mon_chuan = normalize_course_name(ten_mon)
            normalized = ten_mon_chuan.strip().lower()
            if normalized not in monhoc_map:
                monhoc_map[normalized] = mon_key
                do_kho = course_difficulty(ten_mon_chuan, loai_mon)
                ma_mon = ma_mon_from_name(mon_key, ten_mon_chuan)
                monhoc_rows.append((mon_key, ma_mon, ten_mon_chuan, tin_chi, loai_mon, loai_mon, do_kho))
                mon_key += 1

            ctdt_rows.append((
                ctdt_key,
                nganh_key,
                monhoc_map[normalized],
                (hoc_ky_du_kien + 1) // 2,
                hoc_ky_du_kien,
                "Bắt buộc",
                loai_mon,
            ))
            ctdt_key += 1

dim_monhoc = pd.DataFrame(monhoc_rows, columns=[
    "MonHocKey", "MaMonHoc", "TenMonHoc", "SoTinChi", "LoaiMonHoc", "KhoiKienThuc", "DoKho"
])
dim_ctdt = pd.DataFrame(ctdt_rows, columns=[
    "CTDTKey", "NganhKey", "MonHocKey", "NamDaoTao", "HocKyDuKien", "BatBuocTuChon", "LoaiMonHoc"
])

# Lớp: mỗi ngành có 4 khóa, mỗi ngành 4-5 lớp, tổng khoảng 40-50 lớp.
lop_rows = []
lop_key = 1
for nganh_key, ma_nganh, ten_nganh, khoa_key in NGANH_DATA:
    # Mỗi ngành mặc định 1 lớp/khóa. Một số ngành đông hơn có thêm 1 lớp ở khóa sau.
    extra_khoa = random.choice([None, 15, 16])
    class_levels = ["Tốt", "Trung bình", "Yếu", "Trung bình", "Tốt"]
    level_idx = 0

    for khoa_hoc in [13, 14, 15, 16]:
        so_lop = 2 if khoa_hoc == extra_khoa else 1

        for stt in range(1, so_lop + 1):
            # Đảm bảo mỗi ngành có lớp tốt, lớp trung bình và lớp yếu để dashboard phân tích có ý nghĩa.
            if level_idx < len(class_levels):
                level = class_levels[level_idx]
            else:
                level = random.choices(["Tốt", "Trung bình", "Yếu"], weights=[0.25, 0.55, 0.20])[0]
            level_idx += 1

            ma_lop = f"{ma_nganh}{khoa_hoc}A{stt}"
            ten_lop = f"{ten_nganh} {khoa_hoc}A{stt}"
            nam_sv = KHOA_HOC_TO_NAM_SV[khoa_hoc]
            lop_rows.append((lop_key, ma_lop, ten_lop, f"Khóa {khoa_hoc}", nam_sv, fake.name(), nganh_key, khoa_key, level))
            lop_key += 1

dim_lop = pd.DataFrame(lop_rows, columns=[
    "LopKey", "MaLop", "TenLop", "KhoaHoc", "NamSinhVien", "CoVanHocTap", "NganhKey", "KhoaKey", "MucLop"
])

# Sinh viên: tăng quy mô xấp xỉ gấp đôi so với bản cũ, vẫn giữ khóa sau đông hơn khóa trước.
sv_rows = []
sv_key = 1
for _, lop in dim_lop.iterrows():
    khoa_hoc_num = int(str(lop["KhoaHoc"]).replace("Khóa ", ""))
    # Bản v7: tăng sĩ số mỗi lớp xấp xỉ gấp đôi để tổng sinh viên khoảng 3.300 - 4.400.
    # Vẫn giữ logic thực tế: khóa sau đông hơn khóa trước.
    if khoa_hoc_num == 16:
        so_sv = random.randint(72, 80)
    elif khoa_hoc_num == 15:
        so_sv = random.randint(68, 78)
    elif khoa_hoc_num == 14:
        so_sv = random.randint(64, 74)
    else:
        so_sv = random.randint(60, 70)

    for i in range(1, so_sv + 1):
        gioi_tinh = weighted_gender(int(lop["KhoaKey"]))
        ho_ten = fake.name_male() if gioi_tinh == "Nam" else fake.name_female()
        # Khóa sau kém tuổi khóa trước: khóa 13 lớn tuổi hơn khóa 16.
        birth_year = 1991 + khoa_hoc_num
        ngay_sinh = fake.date_between_dates(date(birth_year, 1, 1), date(birth_year, 12, 31))
        ma_sv = f"SV{khoa_hoc_num}{int(lop['LopKey']):03d}{i:03d}"
        ngay_nhap_hoc = ngay_nhap_hoc_theo_khoa(khoa_hoc_num)
        ability = random.choices(["Xuất sắc", "Giỏi", "Khá", "Trung bình", "Yếu"], weights=ABILITY_WEIGHTS)[0]
        sv_rows.append((
            sv_key,
            ma_sv,
            ho_ten,
            gioi_tinh,
            ngay_sinh,
            random.choice(QUE_QUAN),
            ngay_nhap_hoc,
            lop["KhoaHoc"],
            int(lop["NamSinhVien"]),
            "Đang học",
            int(lop["LopKey"]),
            int(lop["NganhKey"]),
            int(lop["KhoaKey"]),
            ability,
        ))
        sv_key += 1

dim_sinhvien = pd.DataFrame(sv_rows, columns=[
    "SinhVienKey", "MaSinhVien", "HoTen", "GioiTinh", "NgaySinh", "QueQuan", "NgayNhapHoc",
    "KhoaHoc", "NamSinhVien", "TrangThaiHocTap", "LopKey", "NganhKey", "KhoaKey", "NhomNangLuc"
])

# =====================================================
# 5. TẠO FACT: KẾT QUẢ HỌC TẬP, RÈN LUYỆN, TỔNG KẾT
# =====================================================

# Tối ưu tốc độ: gom sẵn dữ liệu tra cứu thay vì lọc DataFrame lặp lại nhiều lần.
nganh_by_key = {int(r.NganhKey): r for r in dim_nganh.itertuples(index=False)}
lop_by_key = {int(r.LopKey): r for r in dim_lop.itertuples(index=False)}
mon_by_key = {int(r.MonHocKey): r for r in dim_monhoc.itertuples(index=False)}
gv_keys_by_khoa = {
    int(khoa_key): [int(x) for x in dim_giangvien.loc[dim_giangvien.KhoaKey == khoa_key, "GiangVienKey"].tolist()]
    for khoa_key, _, _ in KHOA_DATA
}
ctdt_by_nganh_sem = {}
for r in dim_ctdt.itertuples(index=False):
    ctdt_by_nganh_sem.setdefault((int(r.NganhKey), int(r.HocKyDuKien)), []).append(r)

fact_kq = []
fact_rl = []
fact_tk = []

kq_key = 1
rl_key = 1
tk_key = 1

for sv in dim_sinhvien.itertuples(index=False):
    nganh = nganh_by_key[int(sv.NganhKey)]
    lop = lop_by_key[int(sv.LopKey)]
    profile = NGANH_PROFILE[nganh.MaNganh]
    class_profile = CLASS_LEVELS[lop.MucLop]
    khoa_num = int(str(sv.KhoaHoc).replace("Khóa ", ""))
    available_hks = KHOA_HOC_TO_HK[khoa_num]

    total_weighted = 0.0
    total_credits_registered = 0
    total_credits_passed = 0
    consecutive_warning = 0
    gpa_tich_luy = 0.0
    so_tin_chi_no_luy_ke = 0

    for hoc_ky_key, hoc_ky_du_kien in available_hks:
        courses = ctdt_by_nganh_sem.get((int(sv.NganhKey), hoc_ky_du_kien), [])
        if not courses:
            continue

        hk_weighted = 0.0
        hk_credits = 0
        hk_passed = 0
        hk_failed = 0

        for ctdt in courses:
            mon = mon_by_key[int(ctdt.MonHocKey)]
            giang_vien_key = random.choice(gv_keys_by_khoa[int(sv.KhoaKey)])

            year = int(ctdt.NamDaoTao)
            ability = sv.NhomNangLuc
            target_gpa = (
                profile["mean"]
                + class_profile["gpa_bonus"]
                + ABILITY_BONUS[ability]
                + SEMESTER_EFFECT.get(hoc_ky_du_kien, 0)
            )
            if year == 4 and ability in ["Xuất sắc", "Giỏi", "Khá"]:
                target_gpa += 0.06
            target_gpa = clamp(target_gpa, 0.8, 4.0)

            # Sinh điểm theo 2 tầng:
            # 1) Quyết định xác suất trượt theo kịch bản thực tế.
            # 2) Nếu không trượt thì sinh điểm theo năng lực/GPA mục tiêu.
            # Cách này giúp môn dễ, trung bình, khó có tỷ lệ đạt khác nhau rõ ràng,
            # thay vì điểm bị đẹp quá và gần như không có sinh viên nợ môn.
            p_fail = fail_probability(
                str(mon.DoKho),
                ability,
                str(lop.MucLop),
                float(profile["pass_rate"]),
                year,
                str(mon.LoaiMonHoc),
            )
            if random.random() < p_fail:
                total_score = score_from_failure(str(mon.DoKho), ability)
            else:
                total_score = max(4.0, score_from_target_gpa(target_gpa, str(mon.DoKho), float(profile["pass_rate"])))

            cc, gk, ck, final = split_score(total_score)

            # Bảo toàn quyết định rớt/đạt sau khi tách điểm thành chuyên cần, giữa kỳ, cuối kỳ.
            # Nếu đã xác định rớt thì điểm tổng kết không được vượt ngưỡng đạt.
            if total_score < 4.0 and final >= 4.0:
                final = round(random.uniform(2.0, 3.9), 1)
                cc, gk, ck = split_score(final)[:3]
            elif total_score >= 4.0 and final < 4.0:
                final = round(random.uniform(4.0, 5.4), 1)
                cc, gk, ck = split_score(final)[:3]

            letter, he4, ket_qua = diem_to_letter(final)

            tc = int(mon.SoTinChi)
            tc_dat = tc if ket_qua == "Đạt" else 0
            tc_khong_dat = 0 if ket_qua == "Đạt" else tc

            fact_kq.append((
                kq_key, int(sv.SinhVienKey), int(sv.KhoaKey), int(sv.NganhKey), int(sv.LopKey),
                int(mon.MonHocKey), int(hoc_ky_key), giang_vien_key,
                cc, gk, ck, final, he4, letter, ket_qua,
                tc, tc_dat, tc_khong_dat, 1,
            ))
            kq_key += 1

            hk_weighted += he4 * tc
            hk_credits += tc
            hk_passed += tc_dat
            hk_failed += tc_khong_dat

        gpa_hk = round(hk_weighted / hk_credits, 2) if hk_credits else 0
        total_weighted += hk_weighted
        total_credits_registered += hk_credits
        total_credits_passed += hk_passed
        gpa_tich_luy = round(total_weighted / total_credits_registered, 2) if total_credits_registered else 0
        # Nợ tín chỉ lũy kế không nên hiểu là tổng tất cả tín chỉ từng rớt,
        # vì thực tế sinh viên có thể thi lại/học lại để trả nợ môn.
        recovered_tc = recovered_debt_credits(so_tin_chi_no_luy_ke, sv.NhomNangLuc, hoc_ky_du_kien)
        so_tin_chi_no_luy_ke = max(0, so_tin_chi_no_luy_ke + hk_failed - recovered_tc)
        no_tc_luy_ke = so_tin_chi_no_luy_ke

        year = (hoc_ky_du_kien + 1) // 2
        base_rl = 75.5 + float(profile["rl_bonus"]) + (4 if year == 1 else 0) + (-3 if year == 4 else 0)
        if sv.NhomNangLuc == "Yếu":
            base_rl -= 4
        if nganh.MaNganh in ["QTKS", "QTDL"]:
            base_rl += 3
        rl_from_gpa = (gpa_hk - 2.5) * 5.0
        noise = np.random.normal(0, 7)
        rl_total = int(round(clamp(base_rl + rl_from_gpa + noise, 30, 100)))

        y_thuc = int(round(clamp(rl_total * 0.30 + np.random.normal(0, 2), 0, 30)))
        noi_quy = int(round(clamp(rl_total * 0.25 + np.random.normal(0, 2), 0, 25)))
        phong_trao = int(round(clamp(rl_total * 0.25 + np.random.normal(0, 3), 0, 25)))
        cong_dong = int(round(clamp(rl_total - y_thuc - noi_quy - phong_trao, 0, 20)))
        rl_total = int(y_thuc + noi_quy + phong_trao + cong_dong)
        xl_rl_key = xep_loai_ren_luyen(rl_total)

        fact_rl.append((
            rl_key, int(sv.SinhVienKey), int(sv.KhoaKey), int(sv.NganhKey), int(sv.LopKey),
            int(hoc_ky_key), y_thuc, noi_quy, phong_trao, cong_dong, rl_total, xl_rl_key,
        ))
        rl_key += 1

        cb = canh_bao(gpa_hk, gpa_tich_luy, hk_failed, rl_total)
        consecutive_warning = consecutive_warning + 1 if cb != "Không cảnh báo" else 0

        if gpa_tich_luy < 2.0 or no_tc_luy_ke > 6 or rl_total < 50 or consecutive_warning >= 2:
            nguy_co = "Cao"
        elif gpa_tich_luy < 2.5 or no_tc_luy_ke >= 3 or rl_total < 70 or cb == "Cảnh báo nhẹ":
            nguy_co = "Trung bình"
        else:
            nguy_co = "Thấp"

        fact_tk.append((
            tk_key, int(sv.SinhVienKey), int(sv.KhoaKey), int(sv.NganhKey), int(sv.LopKey),
            int(hoc_ky_key), hk_credits, hk_passed, hk_failed, gpa_hk, gpa_tich_luy, rl_total,
            xep_loai_hoc_tap(gpa_hk), xl_rl_key, CANH_BAO_KEY[cb],
            cb, nguy_co, no_tc_luy_ke, consecutive_warning,
        ))
        tk_key += 1

    sv_idx = dim_sinhvien.index[dim_sinhvien.SinhVienKey == sv.SinhVienKey][0]
    no_tc = so_tin_chi_no_luy_ke
    if khoa_num == 13:
        # Khóa cuối theo kịch bản: tốt nghiệp đúng hạn khoảng 80% - 90%.
        # Điều kiện chính vẫn dựa trên GPA và số tín chỉ nợ sau khi đã mô phỏng trả nợ môn.
        if gpa_tich_luy >= 2.0 and no_tc <= 3:
            status = random.choices(["Tốt nghiệp", "Chậm tiến độ"], weights=[0.92, 0.08])[0]
        elif gpa_tich_luy >= 2.0 and no_tc <= 6:
            status = random.choices(["Tốt nghiệp", "Chậm tiến độ"], weights=[0.45, 0.55])[0]
        elif no_tc > 9 or gpa_tich_luy < 1.8:
            status = random.choices(["Cảnh báo học vụ", "Chậm tiến độ", "Thôi học"], weights=[0.45, 0.45, 0.10])[0]
        else:
            status = "Chậm tiến độ"
    else:
        if gpa_tich_luy < 1.8 or no_tc > 9:
            status = random.choices(["Cảnh báo học vụ", "Đang học", "Bảo lưu"], weights=[0.65, 0.25, 0.10])[0]
        elif no_tc >= 6:
            status = random.choices(["Đang học", "Cảnh báo học vụ", "Bảo lưu"], weights=[0.68, 0.27, 0.05])[0]
        else:
            status = random.choices(["Đang học", "Cảnh báo học vụ", "Bảo lưu"], weights=[0.90, 0.07, 0.03])[0]
    dim_sinhvien.at[sv_idx, "TrangThaiHocTap"] = status

fact_ketqua = pd.DataFrame(fact_kq, columns=[
    "KetQuaHocTapKey", "SinhVienKey", "KhoaKey", "NganhKey", "LopKey",
    "MonHocKey", "HocKyKey", "GiangVienKey",
    "DiemChuyenCan", "DiemGiuaKy", "DiemCuoiKy", "DiemTongKet", "DiemHe4",
    "DiemChu", "KetQua", "SoTinChiDangKy", "SoTinChiDat", "SoTinChiKhongDat", "LanHoc",
])

fact_drl = pd.DataFrame(fact_rl, columns=[
    "DiemRenLuyenKey", "SinhVienKey", "KhoaKey", "NganhKey", "LopKey",
    "HocKyKey", "DiemYThucHocTap", "DiemChapHanhNoiQuy",
    "DiemHoatDongPhongTrao", "DiemCongDong", "DiemTongRenLuyen", "XepLoaiRenLuyenKey",
])

fact_tongket = pd.DataFrame(fact_tk, columns=[
    "TongKetHocKyKey", "SinhVienKey", "KhoaKey", "NganhKey", "LopKey",
    "HocKyKey", "TongSoTinChiDangKy", "TongSoTinChiDat",
    "TongSoTinChiKhongDat", "DiemTrungBinhHocKy", "DiemTrungBinhTichLuy", "DiemRenLuyen",
    "XepLoaiHocTapKey", "XepLoaiRenLuyenKey", "CanhBaoKey", "TrangThaiCanhBao", "MucNguyCo",
    "SoTinChiNoLuyKe", "SoHocKyCanhBaoLienTiep",
])

# Fact_HoSoSinhVienHienTai: snapshot 1 sinh viên = 1 dòng, dùng cho KPI hiện tại.
latest_tk_snapshot = fact_tongket.sort_values("HocKyKey").groupby("SinhVienKey").tail(1).copy()
so_lan_canh_bao = (
    fact_tongket.assign(IsCanhBao=fact_tongket["CanhBaoKey"].ne(1))
    .groupby("SinhVienKey")["IsCanhBao"].sum()
    .astype(int)
    .reset_index(name="SoLanCanhBao")
)
mon_rot = (
    fact_ketqua.assign(IsRot=fact_ketqua["KetQua"].eq("Không đạt"))
    .groupby("SinhVienKey")["IsRot"].sum()
    .astype(int)
    .reset_index(name="TongSoMonRot")
)

ho_so = (
    latest_tk_snapshot.merge(so_lan_canh_bao, on="SinhVienKey", how="left")
    .merge(mon_rot, on="SinhVienKey", how="left")
    .merge(dim_sinhvien[["SinhVienKey", "TrangThaiHocTap"]], on="SinhVienKey", how="left")
)
ho_so["SoLanCanhBao"] = ho_so["SoLanCanhBao"].fillna(0).astype(int)
ho_so["TongSoMonRot"] = ho_so["TongSoMonRot"].fillna(0).astype(int)
ho_so = ho_so.reset_index(drop=True)
ho_so["HoSoKey"] = ho_so.index + 1

fact_hoso = ho_so[[
    "HoSoKey", "SinhVienKey", "KhoaKey", "NganhKey", "LopKey",
    "HocKyKey", "DiemTrungBinhTichLuy", "DiemRenLuyen",
    "TongSoTinChiDangKy", "TongSoTinChiDat", "SoTinChiNoLuyKe", "TongSoMonRot",
    "SoLanCanhBao", "XepLoaiHocTapKey", "XepLoaiRenLuyenKey", "CanhBaoKey",
    "MucNguyCo", "TrangThaiHocTap"
]].rename(columns={
    "HocKyKey": "HocKyGanNhatKey",
    "DiemTrungBinhTichLuy": "GPATichLuyHienTai",
    "DiemRenLuyen": "DiemRenLuyenGanNhat",
    "TongSoTinChiDangKy": "TongTinChiDangKy",
    "TongSoTinChiDat": "TongTinChiDat",
    "SoTinChiNoLuyKe": "TongTinChiNo",
    "MucNguyCo": "NhomNguyCo",
    "TrangThaiHocTap": "TrangThaiTotNghiep",
})
fact_hoso["SoMonHocLai"] = fact_hoso["TongSoMonRot"]
fact_hoso["SoHocKyDaHoc"] = fact_hoso["SinhVienKey"].map(fact_tongket.groupby("SinhVienKey").size()).astype(int)
fact_hoso = fact_hoso[[
    "HoSoKey", "SinhVienKey", "KhoaKey", "NganhKey", "LopKey",
    "HocKyGanNhatKey", "SoHocKyDaHoc",
    "GPATichLuyHienTai", "DiemRenLuyenGanNhat", "TongTinChiDangKy", "TongTinChiDat",
    "TongTinChiNo", "TongSoMonRot", "SoMonHocLai", "SoLanCanhBao",
    "XepLoaiHocTapKey", "XepLoaiRenLuyenKey", "CanhBaoKey", "NhomNguyCo", "TrangThaiTotNghiep"
]]

# =====================================================
# 6. XUẤT FILE CSV
# =====================================================

tables = {
    "Dim_Khoa.csv": dim_khoa,
    "Dim_Nganh.csv": dim_nganh,
    "Dim_Lop.csv": dim_lop,
    "Dim_SinhVien.csv": dim_sinhvien,
    "Dim_MonHoc.csv": dim_monhoc,
    "Dim_HocKy.csv": dim_hocky,
    "Dim_GiangVien.csv": dim_giangvien,
    "Dim_CanhBaoHocVu.csv": dim_canhbao,
    "Dim_ChuongTrinhDaoTao.csv": dim_ctdt,
    "Dim_XepLoaiHocTap.csv": dim_xl_ht,
    "Dim_XepLoaiRenLuyen.csv": dim_xl_rl,
    "Fact_KetQuaHocTap.csv": fact_ketqua,
    "Fact_DiemRenLuyen.csv": fact_drl,
    "Fact_TongKetHocKy.csv": fact_tongket,
    "Fact_HoSoSinhVienHienTai.csv": fact_hoso,
}

for filename, df in tables.items():
    df.to_csv(os.path.join(OUTPUT_DIR, filename), index=False, encoding="utf-8-sig")

print("ĐÃ SINH DỮ LIỆU THÀNH CÔNG")
print(f"Thư mục xuất file: {OUTPUT_DIR}")
for filename, df in tables.items():
    print(f"{filename}: {len(df):,} dòng")

print("\nKiểm tra nhanh:")
print(f"- Số khoa: {len(dim_khoa)}")
print(f"- Số ngành: {len(dim_nganh)}")
print(f"- Số lớp: {len(dim_lop)}")
print(f"- Số sinh viên: {len(dim_sinhvien):,}")
print(f"- Số môn học duy nhất: {len(dim_monhoc)}")
print(f"- Số CTĐT: {len(dim_ctdt)}")
print(f"- Fact_KetQuaHocTap: {len(fact_ketqua):,}")
print(f"- Fact_TongKetHocKy: {len(fact_tongket):,}")
print(f"- Fact_HoSoSinhVienHienTai: {len(fact_hoso):,}")
# =====================================================
# 7. KIỂM TRA TỶ LỆ THEO KỊCH BẢN
# =====================================================
try:
    latest_tk = fact_tongket.sort_values('HocKyKey').groupby('SinhVienKey').tail(1)
    latest_tk = latest_tk.merge(dim_xl_ht[['XepLoaiHocTapKey', 'TenXepLoai']], on='XepLoaiHocTapKey', how='left')
    latest_tk = latest_tk.merge(dim_khoa[['KhoaKey', 'TenKhoa']], on='KhoaKey', how='left')

    print('\nKiểm tra tỷ lệ học lực học kỳ gần nhất:')
    print(latest_tk['TenXepLoai'].value_counts(normalize=True).mul(100).round(2).to_string())

    print('\nTỷ lệ sinh viên yếu theo khoa ở học kỳ gần nhất:')
    weak_by_khoa = latest_tk.assign(IsYeu=latest_tk['TenXepLoai'].eq('Yếu')) \
        .groupby('TenKhoa')['IsYeu'].mean().mul(100).round(2)
    print(weak_by_khoa.to_string())

    print('\nTỷ lệ cảnh báo học vụ học kỳ gần nhất:')
    print(latest_tk['TrangThaiCanhBao'].value_counts(normalize=True).mul(100).round(2).to_string())

    print('\nTỷ lệ trạng thái sinh viên khóa 13:')
    print(dim_sinhvien.loc[dim_sinhvien['KhoaHoc'].eq('Khóa 13'), 'TrangThaiHocTap']
          .value_counts(normalize=True).mul(100).round(2).to_string())
except Exception as e:
    print(f'Không thể in phần kiểm tra tỷ lệ: {e}')
