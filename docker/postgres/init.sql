-- 1. Tạo bảng lưu trữ giá vé máy bay (Bảng cũ của bạn)
CREATE TABLE IF NOT EXISTS flight_prices (
    timestamp TIMESTAMPTZ,
    id_departure VARCHAR(10),
    id_arrival VARCHAR(10),
    departure_datetime TIMESTAMPTZ,
    arrival_datetime TIMESTAMPTZ,
    airline_name VARCHAR(100),
    travel_class VARCHAR(50),
    is_nonstop BOOLEAN,
    price NUMERIC
);

-- 2. Tạo bảng danh mục sân bay (Bảng mới)
CREATE TABLE IF NOT EXISTS airports (
    iata VARCHAR(5) PRIMARY KEY,
    airport VARCHAR(255)
);

-- 3. Nạp dữ liệu danh sách sân bay
-- ON CONFLICT DO NOTHING giúp tránh lỗi nếu dữ liệu đã tồn tại khi chạy lại
INSERT INTO airports (iata, airport) VALUES
('VCA', 'Can Tho International Airport'),
('DAD', 'Da Nang International Airport'),
('HPH', 'Cat Bi International Airport'),
('HAN', 'Noi Bai International Airport'),
('SGN', 'Tan Son Nhat International Airport'),
('HUI', 'Phu Bai International Airport'),
('CRX', 'Cam Ranh International Airport'),
('PQC', 'Phu Quoc International Airport'),
('VDO', 'Van Don International Airport'),
('VII', 'Vinh International Airport'),
('BMV', 'Buon Ma Thuot Airport'),
('CAH', 'Ca Mau Airport'),
('VCS', 'Co Ong Airport'),
('VCL', 'Chu Lai Airport'),
('DLI', 'Lien Khuong Airport'),
('DIN', 'Dien Bien Phu Airport'),
('VDH', 'Dong Hoi Airport'),
('PXU', 'Pleiku Airport'),
('UIH', 'Phu Cat Airport'),
('VKG', 'Rach Gia Airport'),
('TBB', 'Dong Tac Airport'),
('VTG', 'Vung Tau Airport'),
('THD', 'Tho Xuan Airport')
ON CONFLICT (iata) DO NOTHING;