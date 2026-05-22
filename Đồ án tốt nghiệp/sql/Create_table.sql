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