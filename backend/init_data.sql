-- 初始化测试数据
-- 注意：需要在 Django migrations 完成后执行

USE order_management;

-- 创建管理员用户 (密码: admin123)
-- Django 使用 pbkdf2_sha256 加密，这里使用 Django shell 生成的密码哈希
INSERT INTO auth_user (password, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
SELECT 'pbkdf2_sha256$600000$salt$hash', 1, 'admin', '管理员', '', 'admin@example.com', 1, 1, NOW()
WHERE NOT EXISTS (SELECT 1 FROM auth_user WHERE username = 'admin');

-- 插入测试订单数据
INSERT INTO orders (order_number, user_id, total_amount, status, shipping_address, contact_phone, created_at, updated_at) VALUES
('ORD20260101001', 1, 1299.00, 'pending', '北京市朝阳区建国路88号SOHO现代城A座1501室', '13800138001', '2026-01-20 10:30:00', '2026-01-20 10:30:00'),
('ORD20260101002', 1, 2599.00, 'processing', '上海市浦东新区陆家嘴环路1000号恒生银行大厦25层', '13900139002', '2026-01-20 11:45:00', '2026-01-21 09:00:00'),
('ORD20260101003', 1, 899.00, 'shipped', '广州市天河区珠江新城华夏路30号富力盈通大厦12楼', '13700137003', '2026-01-19 14:20:00', '2026-01-22 16:30:00'),
('ORD20260101004', 1, 3999.00, 'delivered', '深圳市南山区科技园南区高新南一道飞亚达大厦5层', '13600136004', '2026-01-18 09:15:00', '2026-01-23 11:00:00'),
('ORD20260101005', 1, 599.00, 'cancelled', '杭州市西湖区文三路478号华星科技大厦8楼', '13500135005', '2026-01-17 16:00:00', '2026-01-18 10:00:00'),
('ORD20260101006', 1, 1899.00, 'pending', '成都市高新区天府大道北段1700号环球中心E1区12层', '13400134006', '2026-01-21 08:30:00', '2026-01-21 08:30:00'),
('ORD20260101007', 1, 4299.00, 'processing', '武汉市江汉区建设大道568号新世界国贸大厦38层', '13300133007', '2026-01-21 10:00:00', '2026-01-22 14:00:00'),
('ORD20260101008', 1, 799.00, 'shipped', '南京市鼓楼区中山北路30号城市名人酒店商务楼15层', '13200132008', '2026-01-19 13:45:00', '2026-01-23 09:30:00'),
('ORD20260101009', 1, 2199.00, 'delivered', '西安市雁塔区高新路52号高新国际商务中心18层', '13100131009', '2026-01-16 11:20:00', '2026-01-20 15:00:00'),
('ORD20260101010', 1, 1599.00, 'pending', '重庆市渝中区解放碑民权路28号英利国际金融中心22层', '13000130010', '2026-01-22 09:00:00', '2026-01-22 09:00:00'),
('ORD20260101011', 1, 699.00, 'processing', '天津市和平区南京路189号津汇广场1座20层', '12900129011', '2026-01-22 14:30:00', '2026-01-23 10:00:00'),
('ORD20260101012', 1, 5999.00, 'shipped', '苏州市工业园区苏州大道东265号现代传媒广场16层', '12800128012', '2026-01-18 16:00:00', '2026-01-22 11:00:00');

-- 插入订单项数据
-- 订单1的商品
INSERT INTO order_items (order_id, product_name, price, quantity, subtotal, created_at) VALUES
(1, 'Apple AirPods Pro 2代', 1299.00, 1, 1299.00, '2026-01-20 10:30:00');

-- 订单2的商品
INSERT INTO order_items (order_id, product_name, price, quantity, subtotal, created_at) VALUES
(2, 'Sony WH-1000XM5 头戴式耳机', 2299.00, 1, 2299.00, '2026-01-20 11:45:00'),
(2, '耳机收纳包', 150.00, 2, 300.00, '2026-01-20 11:45:00');

-- 订单3的商品
INSERT INTO order_items (order_id, product_name, price, quantity, subtotal, created_at) VALUES
(3, '小米手环8 Pro', 299.00, 1, 299.00, '2026-01-19 14:20:00'),
(3, '替换表带套装', 200.00, 3, 600.00, '2026-01-19 14:20:00');

-- 订单4的商品
INSERT INTO order_items (order_id, product_name, price, quantity, subtotal, created_at) VALUES
(4, 'iPad Air 5 64GB', 3999.00, 1, 3999.00, '2026-01-18 09:15:00');

-- 订单5的商品
INSERT INTO order_items (order_id, product_name, price, quantity, subtotal, created_at) VALUES
(5, '罗技MX Master 3S鼠标', 599.00, 1, 599.00, '2026-01-17 16:00:00');

-- 订单6的商品
INSERT INTO order_items (order_id, product_name, price, quantity, subtotal, created_at) VALUES
(6, 'Nintendo Switch OLED', 1599.00, 1, 1599.00, '2026-01-21 08:30:00'),
(6, '塞尔达传说：王国之泪', 300.00, 1, 300.00, '2026-01-21 08:30:00');

-- 订单7的商品
INSERT INTO order_items (order_id, product_name, price, quantity, subtotal, created_at) VALUES
(7, 'MacBook Air M2 256GB', 3999.00, 1, 3999.00, '2026-01-21 10:00:00'),
(7, 'Type-C扩展坞', 150.00, 2, 300.00, '2026-01-21 10:00:00');

-- 订单8的商品
INSERT INTO order_items (order_id, product_name, price, quantity, subtotal, created_at) VALUES
(8, '飞利浦电动牙刷HX9352', 799.00, 1, 799.00, '2026-01-19 13:45:00');

-- 订单9的商品
INSERT INTO order_items (order_id, product_name, price, quantity, subtotal, created_at) VALUES
(9, 'Bose SoundLink Flex 蓝牙音箱', 999.00, 1, 999.00, '2026-01-16 11:20:00'),
(9, 'Bose 便携收纳袋', 200.00, 1, 200.00, '2026-01-16 11:20:00'),
(9, '3.5mm音频线', 50.00, 2, 100.00, '2026-01-16 11:20:00'),
(9, '车载充电器', 150.00, 6, 900.00, '2026-01-16 11:20:00');

-- 订单10的商品
INSERT INTO order_items (order_id, product_name, price, quantity, subtotal, created_at) VALUES
(10, 'Kindle Paperwhite 5', 999.00, 1, 999.00, '2026-01-22 09:00:00'),
(10, 'Kindle保护套', 200.00, 1, 200.00, '2026-01-22 09:00:00'),
(10, '屏幕保护膜', 50.00, 2, 100.00, '2026-01-22 09:00:00'),
(10, 'Type-C充电线', 30.00, 10, 300.00, '2026-01-22 09:00:00');

-- 订单11的商品
INSERT INTO order_items (order_id, product_name, price, quantity, subtotal, created_at) VALUES
(11, '米家台灯Pro', 349.00, 2, 698.00, '2026-01-22 14:30:00');

-- 订单12的商品
INSERT INTO order_items (order_id, product_name, price, quantity, subtotal, created_at) VALUES
(12, 'DJI Mini 3 Pro 无人机', 4999.00, 1, 4999.00, '2026-01-18 16:00:00'),
(12, '无人机电池', 500.00, 2, 1000.00, '2026-01-18 16:00:00');
