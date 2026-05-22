# -*- coding: utf-8 -*-
"""
Import dữ liệu Data Warehouse model Dim_HocKy vào Microsoft SQL Server.

Chạy sau khi đã chạy:
    python generate_eaut_student_dw_v10_powerbi_hocky.py

Cài đặt:
    pip install pandas pyodbc
"""
from __future__ import annotations

import os
import sys
from typing import Dict, List

import pandas as pd
import pyodbc

# =====================================================
# 1. CẤU HÌNH KẾT NỐI SQL SERVER
# =====================================================

SERVER = r"LAPTOP-687VR24K\SQLEXPRESS"
DATABASE = "EAUT_Student_DW"
DRIVER = "ODBC Driver 17 for SQL Server"
TRUSTED_CONNECTION = True

SQL_USERNAME = "sa"
SQL_PASSWORD = "your_password"

CSV_DIR = "output_dw"
RECREATE_TABLES = True

# =====================================================
# 2. THỨ TỰ IMPORT VÀ CỘT CHUẨN
# =====================================================

IMPORT_ORDER = [
    "Dim_Khoa",
    "Dim_Nganh",
    "Dim_HocKy",
    "Dim_XepLoaiHocTap",
    "Dim_XepLoaiRenLuyen",
    "Dim_CanhBaoHocVu",
    "Dim_Lop",
    "Dim_SinhVien",
    "Dim_MonHoc",
    "Dim_GiangVien",
    "Dim_ChuongTrinhDaoTao",
    "Fact_KetQuaHocTap",
    "Fact_DiemRenLuyen",
    "Fact_TongKetHocKy",
    "Fact_HoSoSinhVienHienTai",
]

EXPECTED_COLUMNS: Dict[str, List[str]] = {
    "Dim_Khoa": ["KhoaKey", "MaKhoa", "TenKhoa"],
    "Dim_Nganh": ["NganhKey", "MaNganh", "TenNganh", "KhoaKey"],
    "Dim_HocKy": [
        "HocKyKey", "MaHocKy", "NamHoc", "HocKySo", "TenHocKy",
        "HocKyLabel", "ThuTuHocKy", "NgayBatDauHocKy",
        "NgayKetThucHocKy", "NamKetThucHocKy", "IsHocKyMoiNhat",
    ],
    "Dim_XepLoaiHocTap": ["XepLoaiHocTapKey", "TenXepLoai", "DiemTu", "DiemDen"],
    "Dim_XepLoaiRenLuyen": ["XepLoaiRenLuyenKey", "TenXepLoai", "DiemTu", "DiemDen"],
    "Dim_CanhBaoHocVu": ["CanhBaoKey", "TenCanhBao", "MucDo", "MoTa"],
    "Dim_Lop": ["LopKey", "MaLop", "TenLop", "KhoaHoc", "NamSinhVien", "CoVanHocTap", "NganhKey", "KhoaKey", "MucLop"],
    "Dim_SinhVien": ["SinhVienKey", "MaSinhVien", "HoTen", "GioiTinh", "NgaySinh", "QueQuan", "NgayNhapHoc", "KhoaHoc", "NamSinhVien", "TrangThaiHocTap", "LopKey", "NganhKey", "KhoaKey", "NhomNangLuc"],
    "Dim_MonHoc": ["MonHocKey", "MaMonHoc", "TenMonHoc", "SoTinChi", "LoaiMonHoc", "KhoiKienThuc", "DoKho"],
    "Dim_GiangVien": ["GiangVienKey", "MaGiangVien", "HoTenGiangVien", "HocVi", "KhoaKey"],
    "Dim_ChuongTrinhDaoTao": ["CTDTKey", "NganhKey", "MonHocKey", "NamDaoTao", "HocKyDuKien", "BatBuocTuChon", "LoaiMonHoc"],
    "Fact_KetQuaHocTap": ["KetQuaHocTapKey", "SinhVienKey", "KhoaKey", "NganhKey", "LopKey", "MonHocKey", "HocKyKey", "GiangVienKey", "DiemChuyenCan", "DiemGiuaKy", "DiemCuoiKy", "DiemTongKet", "DiemHe4", "DiemChu", "KetQua", "SoTinChiDangKy", "SoTinChiDat", "SoTinChiKhongDat", "LanHoc"],
    "Fact_DiemRenLuyen": ["DiemRenLuyenKey", "SinhVienKey", "KhoaKey", "NganhKey", "LopKey", "HocKyKey", "DiemYThucHocTap", "DiemChapHanhNoiQuy", "DiemHoatDongPhongTrao", "DiemCongDong", "DiemTongRenLuyen", "XepLoaiRenLuyenKey"],
    "Fact_TongKetHocKy": ["TongKetHocKyKey", "SinhVienKey", "KhoaKey", "NganhKey", "LopKey", "HocKyKey", "TongSoTinChiDangKy", "TongSoTinChiDat", "TongSoTinChiKhongDat", "DiemTrungBinhHocKy", "DiemTrungBinhTichLuy", "DiemRenLuyen", "XepLoaiHocTapKey", "XepLoaiRenLuyenKey", "CanhBaoKey", "TrangThaiCanhBao", "MucNguyCo", "SoTinChiNoLuyKe", "SoHocKyCanhBaoLienTiep"],
    "Fact_HoSoSinhVienHienTai": ["HoSoKey", "SinhVienKey", "KhoaKey", "NganhKey", "LopKey", "HocKyGanNhatKey", "SoHocKyDaHoc", "GPATichLuyHienTai", "DiemRenLuyenGanNhat", "TongTinChiDangKy", "TongTinChiDat", "TongTinChiNo", "TongSoMonRot", "SoMonHocLai", "SoLanCanhBao", "XepLoaiHocTapKey", "XepLoaiRenLuyenKey", "CanhBaoKey", "NhomNguyCo", "TrangThaiTotNghiep"],
}

# =====================================================
# 3. HÀM KẾT NỐI
# =====================================================

def build_conn_str(database: str) -> str:
    if TRUSTED_CONNECTION:
        return (
            f"DRIVER={{{DRIVER}}};"
            f"SERVER={SERVER};"
            f"DATABASE={database};"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
        )
    return (
        f"DRIVER={{{DRIVER}}};"
        f"SERVER={SERVER};"
        f"DATABASE={database};"
        f"UID={SQL_USERNAME};"
        f"PWD={SQL_PASSWORD};"
        "TrustServerCertificate=yes;"
    )


def connect(database: str):
    try:
        return pyodbc.connect(build_conn_str(database), autocommit=False, timeout=30)
    except pyodbc.Error as e:
        print("Không kết nối được SQL Server.")
        print("Hãy kiểm tra SERVER, DRIVER, tài khoản đăng nhập và SQL Server đã bật chưa.")
        print("Các driver đang có trên máy:", pyodbc.drivers())
        print("Chi tiết lỗi:", e)
        sys.exit(1)


def create_database_if_not_exists() -> None:
    conn = connect("master")
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(f"IF DB_ID(N'{DATABASE}') IS NULL CREATE DATABASE [{DATABASE}];")
    cursor.close()
    conn.close()
    print(f"Đã kiểm tra/tạo database: {DATABASE}")

# =====================================================
# 4. SQL TẠO BẢNG
# =====================================================

DROP_TABLES_SQL = """
IF OBJECT_ID('Fact_HoSoSinhVienHienTai', 'U') IS NOT NULL DROP TABLE Fact_HoSoSinhVienHienTai;
IF OBJECT_ID('Fact_TongKetHocKy', 'U') IS NOT NULL DROP TABLE Fact_TongKetHocKy;
IF OBJECT_ID('Fact_DiemRenLuyen', 'U') IS NOT NULL DROP TABLE Fact_DiemRenLuyen;
IF OBJECT_ID('Fact_KetQuaHocTap', 'U') IS NOT NULL DROP TABLE Fact_KetQuaHocTap;
IF OBJECT_ID('Dim_ChuongTrinhDaoTao', 'U') IS NOT NULL DROP TABLE Dim_ChuongTrinhDaoTao;
IF OBJECT_ID('Dim_SinhVien', 'U') IS NOT NULL DROP TABLE Dim_SinhVien;
IF OBJECT_ID('Dim_Lop', 'U') IS NOT NULL DROP TABLE Dim_Lop;
IF OBJECT_ID('Dim_GiangVien', 'U') IS NOT NULL DROP TABLE Dim_GiangVien;
IF OBJECT_ID('Dim_MonHoc', 'U') IS NOT NULL DROP TABLE Dim_MonHoc;
IF OBJECT_ID('Dim_CanhBaoHocVu', 'U') IS NOT NULL DROP TABLE Dim_CanhBaoHocVu;
IF OBJECT_ID('Dim_ThoiGian', 'U') IS NOT NULL DROP TABLE Dim_ThoiGian;
IF OBJECT_ID('Dim_HocKy', 'U') IS NOT NULL DROP TABLE Dim_HocKy;
IF OBJECT_ID('Dim_XepLoaiHocTap', 'U') IS NOT NULL DROP TABLE Dim_XepLoaiHocTap;
IF OBJECT_ID('Dim_XepLoaiRenLuyen', 'U') IS NOT NULL DROP TABLE Dim_XepLoaiRenLuyen;
IF OBJECT_ID('Dim_Nganh', 'U') IS NOT NULL DROP TABLE Dim_Nganh;
IF OBJECT_ID('Dim_Khoa', 'U') IS NOT NULL DROP TABLE Dim_Khoa;
"""

CREATE_TABLES_SQL = """
CREATE TABLE Dim_Khoa (
    KhoaKey INT NOT NULL PRIMARY KEY,
    MaKhoa NVARCHAR(20) NOT NULL UNIQUE,
    TenKhoa NVARCHAR(100) NOT NULL
);

CREATE TABLE Dim_Nganh (
    NganhKey INT NOT NULL PRIMARY KEY,
    MaNganh NVARCHAR(20) NOT NULL UNIQUE,
    TenNganh NVARCHAR(100) NOT NULL,
    KhoaKey INT NOT NULL
);

CREATE TABLE Dim_HocKy (
    HocKyKey INT NOT NULL PRIMARY KEY,
    MaHocKy NVARCHAR(20) NOT NULL UNIQUE,
    NamHoc NVARCHAR(20) NOT NULL,
    HocKySo INT NOT NULL,
    TenHocKy NVARCHAR(100) NOT NULL,
    HocKyLabel NVARCHAR(50) NOT NULL,
    ThuTuHocKy INT NOT NULL,
    NgayBatDauHocKy DATE NOT NULL,
    NgayKetThucHocKy DATE NOT NULL,
    NamKetThucHocKy INT NOT NULL,
    IsHocKyMoiNhat BIT NOT NULL
);

CREATE TABLE Dim_XepLoaiHocTap (
    XepLoaiHocTapKey INT NOT NULL PRIMARY KEY,
    TenXepLoai NVARCHAR(50) NOT NULL,
    DiemTu DECIMAL(6,2) NOT NULL,
    DiemDen DECIMAL(6,2) NOT NULL
);

CREATE TABLE Dim_XepLoaiRenLuyen (
    XepLoaiRenLuyenKey INT NOT NULL PRIMARY KEY,
    TenXepLoai NVARCHAR(50) NOT NULL,
    DiemTu INT NOT NULL,
    DiemDen INT NOT NULL
);

CREATE TABLE Dim_CanhBaoHocVu (
    CanhBaoKey INT NOT NULL PRIMARY KEY,
    TenCanhBao NVARCHAR(100) NOT NULL,
    MucDo INT NOT NULL,
    MoTa NVARCHAR(255)
);

CREATE TABLE Dim_Lop (
    LopKey INT NOT NULL PRIMARY KEY,
    MaLop NVARCHAR(20) NOT NULL UNIQUE,
    TenLop NVARCHAR(100) NOT NULL,
    KhoaHoc NVARCHAR(20) NOT NULL,
    NamSinhVien INT NOT NULL,
    CoVanHocTap NVARCHAR(100),
    NganhKey INT NOT NULL,
    KhoaKey INT NOT NULL,
    MucLop NVARCHAR(20)
);

CREATE TABLE Dim_SinhVien (
    SinhVienKey INT NOT NULL PRIMARY KEY,
    MaSinhVien NVARCHAR(20) NOT NULL UNIQUE,
    HoTen NVARCHAR(100) NOT NULL,
    GioiTinh NVARCHAR(10),
    NgaySinh DATE,
    QueQuan NVARCHAR(100),
    NgayNhapHoc DATE,
    KhoaHoc NVARCHAR(20),
    NamSinhVien INT,
    TrangThaiHocTap NVARCHAR(50),
    LopKey INT NOT NULL,
    NganhKey INT NOT NULL,
    KhoaKey INT NOT NULL,
    NhomNangLuc NVARCHAR(30)
);

CREATE TABLE Dim_MonHoc (
    MonHocKey INT NOT NULL PRIMARY KEY,
    MaMonHoc NVARCHAR(30) NOT NULL UNIQUE,
    TenMonHoc NVARCHAR(200) NOT NULL,
    SoTinChi INT NOT NULL,
    LoaiMonHoc NVARCHAR(50),
    KhoiKienThuc NVARCHAR(50),
    DoKho NVARCHAR(30)
);

CREATE TABLE Dim_GiangVien (
    GiangVienKey INT NOT NULL PRIMARY KEY,
    MaGiangVien NVARCHAR(20) NOT NULL UNIQUE,
    HoTenGiangVien NVARCHAR(100) NOT NULL,
    HocVi NVARCHAR(30),
    KhoaKey INT NOT NULL
);

CREATE TABLE Dim_ChuongTrinhDaoTao (
    CTDTKey INT NOT NULL PRIMARY KEY,
    NganhKey INT NOT NULL,
    MonHocKey INT NOT NULL,
    NamDaoTao INT NOT NULL,
    HocKyDuKien INT NOT NULL,
    BatBuocTuChon NVARCHAR(30),
    LoaiMonHoc NVARCHAR(50)
);

CREATE TABLE Fact_KetQuaHocTap (
    KetQuaHocTapKey BIGINT NOT NULL PRIMARY KEY,
    SinhVienKey INT NOT NULL,
    KhoaKey INT NOT NULL,
    NganhKey INT NOT NULL,
    LopKey INT NOT NULL,
    MonHocKey INT NOT NULL,
    HocKyKey INT NOT NULL,
    GiangVienKey INT NOT NULL,
    DiemChuyenCan DECIMAL(6,2),
    DiemGiuaKy DECIMAL(6,2),
    DiemCuoiKy DECIMAL(6,2),
    DiemTongKet DECIMAL(6,2),
    DiemHe4 DECIMAL(6,2),
    DiemChu NVARCHAR(5),
    KetQua NVARCHAR(20),
    SoTinChiDangKy INT,
    SoTinChiDat INT,
    SoTinChiKhongDat INT,
    LanHoc INT NOT NULL DEFAULT 1,
    CONSTRAINT FK_Fact_KQ_Dim_SinhVien FOREIGN KEY (SinhVienKey) REFERENCES Dim_SinhVien(SinhVienKey),
    CONSTRAINT FK_Fact_KQ_Dim_Khoa FOREIGN KEY (KhoaKey) REFERENCES Dim_Khoa(KhoaKey),
    CONSTRAINT FK_Fact_KQ_Dim_Nganh FOREIGN KEY (NganhKey) REFERENCES Dim_Nganh(NganhKey),
    CONSTRAINT FK_Fact_KQ_Dim_Lop FOREIGN KEY (LopKey) REFERENCES Dim_Lop(LopKey),
    CONSTRAINT FK_Fact_KQ_Dim_MonHoc FOREIGN KEY (MonHocKey) REFERENCES Dim_MonHoc(MonHocKey),
    CONSTRAINT FK_Fact_KQ_Dim_HocKy FOREIGN KEY (HocKyKey) REFERENCES Dim_HocKy(HocKyKey),
    CONSTRAINT FK_Fact_KQ_Dim_GiangVien FOREIGN KEY (GiangVienKey) REFERENCES Dim_GiangVien(GiangVienKey)
);

CREATE TABLE Fact_DiemRenLuyen (
    DiemRenLuyenKey BIGINT NOT NULL PRIMARY KEY,
    SinhVienKey INT NOT NULL,
    KhoaKey INT NOT NULL,
    NganhKey INT NOT NULL,
    LopKey INT NOT NULL,
    HocKyKey INT NOT NULL,
    DiemYThucHocTap INT,
    DiemChapHanhNoiQuy INT,
    DiemHoatDongPhongTrao INT,
    DiemCongDong INT,
    DiemTongRenLuyen INT,
    XepLoaiRenLuyenKey INT NOT NULL,
    CONSTRAINT FK_Fact_DRL_Dim_SinhVien FOREIGN KEY (SinhVienKey) REFERENCES Dim_SinhVien(SinhVienKey),
    CONSTRAINT FK_Fact_DRL_Dim_Khoa FOREIGN KEY (KhoaKey) REFERENCES Dim_Khoa(KhoaKey),
    CONSTRAINT FK_Fact_DRL_Dim_Nganh FOREIGN KEY (NganhKey) REFERENCES Dim_Nganh(NganhKey),
    CONSTRAINT FK_Fact_DRL_Dim_Lop FOREIGN KEY (LopKey) REFERENCES Dim_Lop(LopKey),
    CONSTRAINT FK_Fact_DRL_Dim_HocKy FOREIGN KEY (HocKyKey) REFERENCES Dim_HocKy(HocKyKey),
    CONSTRAINT FK_Fact_DRL_Dim_XLRL FOREIGN KEY (XepLoaiRenLuyenKey) REFERENCES Dim_XepLoaiRenLuyen(XepLoaiRenLuyenKey)
);

CREATE TABLE Fact_TongKetHocKy (
    TongKetHocKyKey BIGINT NOT NULL PRIMARY KEY,
    SinhVienKey INT NOT NULL,
    KhoaKey INT NOT NULL,
    NganhKey INT NOT NULL,
    LopKey INT NOT NULL,
    HocKyKey INT NOT NULL,
    TongSoTinChiDangKy INT,
    TongSoTinChiDat INT,
    TongSoTinChiKhongDat INT,
    DiemTrungBinhHocKy DECIMAL(6,2),
    DiemTrungBinhTichLuy DECIMAL(6,2),
    DiemRenLuyen INT,
    XepLoaiHocTapKey INT NOT NULL,
    XepLoaiRenLuyenKey INT NOT NULL,
    CanhBaoKey INT NOT NULL,
    TrangThaiCanhBao NVARCHAR(50),
    MucNguyCo NVARCHAR(30),
    SoTinChiNoLuyKe INT,
    SoHocKyCanhBaoLienTiep INT,
    CONSTRAINT FK_Fact_TK_Dim_SinhVien FOREIGN KEY (SinhVienKey) REFERENCES Dim_SinhVien(SinhVienKey),
    CONSTRAINT FK_Fact_TK_Dim_Khoa FOREIGN KEY (KhoaKey) REFERENCES Dim_Khoa(KhoaKey),
    CONSTRAINT FK_Fact_TK_Dim_Nganh FOREIGN KEY (NganhKey) REFERENCES Dim_Nganh(NganhKey),
    CONSTRAINT FK_Fact_TK_Dim_Lop FOREIGN KEY (LopKey) REFERENCES Dim_Lop(LopKey),
    CONSTRAINT FK_Fact_TK_Dim_HocKy FOREIGN KEY (HocKyKey) REFERENCES Dim_HocKy(HocKyKey),
    CONSTRAINT FK_Fact_TK_Dim_XLHT FOREIGN KEY (XepLoaiHocTapKey) REFERENCES Dim_XepLoaiHocTap(XepLoaiHocTapKey),
    CONSTRAINT FK_Fact_TK_Dim_XLRL FOREIGN KEY (XepLoaiRenLuyenKey) REFERENCES Dim_XepLoaiRenLuyen(XepLoaiRenLuyenKey),
    CONSTRAINT FK_Fact_TK_Dim_CanhBao FOREIGN KEY (CanhBaoKey) REFERENCES Dim_CanhBaoHocVu(CanhBaoKey)
);

CREATE TABLE Fact_HoSoSinhVienHienTai (
    HoSoKey BIGINT NOT NULL PRIMARY KEY,
    SinhVienKey INT NOT NULL UNIQUE,
    KhoaKey INT NOT NULL,
    NganhKey INT NOT NULL,
    LopKey INT NOT NULL,
    HocKyGanNhatKey INT NOT NULL,
    SoHocKyDaHoc INT,
    GPATichLuyHienTai DECIMAL(6,2),
    DiemRenLuyenGanNhat INT,
    TongTinChiDangKy INT,
    TongTinChiDat INT,
    TongTinChiNo INT,
    TongSoMonRot INT,
    SoMonHocLai INT,
    SoLanCanhBao INT,
    XepLoaiHocTapKey INT NOT NULL,
    XepLoaiRenLuyenKey INT NOT NULL,
    CanhBaoKey INT NOT NULL,
    NhomNguyCo NVARCHAR(30),
    TrangThaiTotNghiep NVARCHAR(50),
    CONSTRAINT FK_Fact_HoSo_Dim_SinhVien FOREIGN KEY (SinhVienKey) REFERENCES Dim_SinhVien(SinhVienKey),
    CONSTRAINT FK_Fact_HoSo_Dim_Khoa FOREIGN KEY (KhoaKey) REFERENCES Dim_Khoa(KhoaKey),
    CONSTRAINT FK_Fact_HoSo_Dim_Nganh FOREIGN KEY (NganhKey) REFERENCES Dim_Nganh(NganhKey),
    CONSTRAINT FK_Fact_HoSo_Dim_Lop FOREIGN KEY (LopKey) REFERENCES Dim_Lop(LopKey),
    CONSTRAINT FK_Fact_HoSo_Dim_HocKy FOREIGN KEY (HocKyGanNhatKey) REFERENCES Dim_HocKy(HocKyKey),
    CONSTRAINT FK_Fact_HoSo_Dim_XLHT FOREIGN KEY (XepLoaiHocTapKey) REFERENCES Dim_XepLoaiHocTap(XepLoaiHocTapKey),
    CONSTRAINT FK_Fact_HoSo_Dim_XLRL FOREIGN KEY (XepLoaiRenLuyenKey) REFERENCES Dim_XepLoaiRenLuyen(XepLoaiRenLuyenKey),
    CONSTRAINT FK_Fact_HoSo_Dim_CanhBao FOREIGN KEY (CanhBaoKey) REFERENCES Dim_CanhBaoHocVu(CanhBaoKey)
);
"""

CREATE_INDEXES_SQL = """
CREATE INDEX IX_Dim_Nganh_KhoaKey ON Dim_Nganh(KhoaKey);
CREATE INDEX IX_Dim_Lop_NganhKey ON Dim_Lop(NganhKey);
CREATE INDEX IX_Dim_Lop_KhoaKey ON Dim_Lop(KhoaKey);
CREATE INDEX IX_Dim_SinhVien_LopKey ON Dim_SinhVien(LopKey);
CREATE INDEX IX_Dim_SinhVien_NganhKey ON Dim_SinhVien(NganhKey);
CREATE INDEX IX_Dim_HocKy_NamHoc ON Dim_HocKy(NamHoc);
CREATE INDEX IX_Dim_HocKy_HocKySo ON Dim_HocKy(HocKySo);
CREATE INDEX IX_Dim_HocKy_ThuTuHocKy ON Dim_HocKy(ThuTuHocKy);
CREATE INDEX IX_Dim_HocKy_NgayKetThucHocKy ON Dim_HocKy(NgayKetThucHocKy);
CREATE INDEX IX_Dim_HocKy_NamKetThucHocKy ON Dim_HocKy(NamKetThucHocKy);
CREATE INDEX IX_Dim_CTDT_NganhKey ON Dim_ChuongTrinhDaoTao(NganhKey);
CREATE INDEX IX_Dim_CTDT_MonHocKey ON Dim_ChuongTrinhDaoTao(MonHocKey);
CREATE INDEX IX_Fact_KQ_SinhVienKey ON Fact_KetQuaHocTap(SinhVienKey);
CREATE INDEX IX_Fact_KQ_KhoaKey ON Fact_KetQuaHocTap(KhoaKey);
CREATE INDEX IX_Fact_KQ_NganhKey ON Fact_KetQuaHocTap(NganhKey);
CREATE INDEX IX_Fact_KQ_LopKey ON Fact_KetQuaHocTap(LopKey);
CREATE INDEX IX_Fact_KQ_MonHocKey ON Fact_KetQuaHocTap(MonHocKey);
CREATE INDEX IX_Fact_KQ_HocKyKey ON Fact_KetQuaHocTap(HocKyKey);
CREATE INDEX IX_Fact_DRL_SinhVienKey ON Fact_DiemRenLuyen(SinhVienKey);
CREATE INDEX IX_Fact_DRL_KhoaKey ON Fact_DiemRenLuyen(KhoaKey);
CREATE INDEX IX_Fact_DRL_NganhKey ON Fact_DiemRenLuyen(NganhKey);
CREATE INDEX IX_Fact_DRL_LopKey ON Fact_DiemRenLuyen(LopKey);
CREATE INDEX IX_Fact_DRL_HocKyKey ON Fact_DiemRenLuyen(HocKyKey);
CREATE INDEX IX_Fact_TK_SinhVienKey ON Fact_TongKetHocKy(SinhVienKey);
CREATE INDEX IX_Fact_TK_KhoaKey ON Fact_TongKetHocKy(KhoaKey);
CREATE INDEX IX_Fact_TK_NganhKey ON Fact_TongKetHocKy(NganhKey);
CREATE INDEX IX_Fact_TK_LopKey ON Fact_TongKetHocKy(LopKey);
CREATE INDEX IX_Fact_TK_HocKyKey ON Fact_TongKetHocKy(HocKyKey);
CREATE INDEX IX_Fact_TK_MucNguyCo ON Fact_TongKetHocKy(MucNguyCo);
CREATE INDEX IX_Fact_HoSo_KhoaKey ON Fact_HoSoSinhVienHienTai(KhoaKey);
CREATE INDEX IX_Fact_HoSo_NganhKey ON Fact_HoSoSinhVienHienTai(NganhKey);
CREATE INDEX IX_Fact_HoSo_LopKey ON Fact_HoSoSinhVienHienTai(LopKey);
CREATE INDEX IX_Fact_HoSo_HocKyGanNhatKey ON Fact_HoSoSinhVienHienTai(HocKyGanNhatKey);
"""

# =====================================================
# 5. ĐỌC CSV VÀ IMPORT
# =====================================================

def read_csv_for_sql(table_name: str) -> pd.DataFrame:
    path = os.path.join(CSV_DIR, f"{table_name}.csv")
    if not os.path.exists(path):
        print(f"Thiếu file: {path}")
        print("Hãy chạy trước: python generate_eaut_student_dw_v10_powerbi_hocky.py")
        sys.exit(1)

    df = pd.read_csv(path, encoding="utf-8-sig")
    expected = EXPECTED_COLUMNS[table_name]

    missing = [col for col in expected if col not in df.columns]
    extra = [col for col in df.columns if col not in expected]
    if missing or extra:
        print(f"Sai cấu trúc cột ở {table_name}.csv")
        if missing:
            print("Cột thiếu:", missing)
        if extra:
            print("Cột thừa:", extra)
        print("Hãy xóa output_dw và chạy lại generate_eaut_student_dw_v10_powerbi_hocky.py")
        sys.exit(1)

    df = df[expected]

    date_columns = ["NgaySinh", "NgayNhapHoc", "NgayBatDauHocKy", "NgayKetThucHocKy"]
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce").dt.strftime("%Y-%m-%d")

    df = df.astype(object).where(pd.notnull(df), None)
    return df


def normalize_value(value):
    if pd.isna(value):
        return None
    if hasattr(value, "item"):
        try:
            return value.item()
        except Exception:
            pass
    return value


def insert_dataframe(cursor, table_name: str, df: pd.DataFrame) -> None:
    columns = list(df.columns)
    col_sql = ", ".join(f"[{col}]" for col in columns)
    placeholders = ", ".join("?" for _ in columns)
    sql = f"INSERT INTO [{table_name}] ({col_sql}) VALUES ({placeholders})"

    rows = [tuple(normalize_value(v) for v in row) for row in df.itertuples(index=False, name=None)]
    if not rows:
        return
    cursor.fast_executemany = True
    cursor.executemany(sql, rows)


def main() -> None:
    if not os.path.isdir(CSV_DIR):
        print(f"Không tìm thấy thư mục {CSV_DIR}.")
        print("Hãy chạy trước: python generate_eaut_student_dw_v10_powerbi_hocky.py")
        sys.exit(1)

    create_database_if_not_exists()
    conn = connect(DATABASE)
    cursor = conn.cursor()

    try:
        if RECREATE_TABLES:
            print("Đang xóa bảng cũ nếu có...")
            cursor.execute(DROP_TABLES_SQL)
            conn.commit()

            print("Đang tạo bảng mới...")
            cursor.execute(CREATE_TABLES_SQL)
            conn.commit()

        print("Đang import dữ liệu CSV vào SQL Server...")
        total_rows = 0
        for table_name in IMPORT_ORDER:
            df = read_csv_for_sql(table_name)
            insert_dataframe(cursor, table_name, df)
            conn.commit()
            total_rows += len(df)
            print(f"OK - {table_name}: {len(df):,} dòng")

        if RECREATE_TABLES:
            print("Đang tạo index...")
            cursor.execute(CREATE_INDEXES_SQL)
            conn.commit()

        print("\nHOÀN THÀNH IMPORT DATA WAREHOUSE VÀO SQL SERVER")
        print(f"Database: {DATABASE}")
        print(f"Tổng số dòng đã import: {total_rows:,}")
        print("Trong Power BI, dùng Star Schema: tất cả Dim nối trực tiếp vào Fact; Dim_HocKy dùng chung cho mọi Fact.")

    except Exception as e:
        conn.rollback()
        print("\nCó lỗi khi import. Đã rollback giao dịch hiện tại.")
        print("Chi tiết lỗi:", e)
        sys.exit(1)
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()
