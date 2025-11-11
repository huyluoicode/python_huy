-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Máy chủ: 127.0.0.1:3307
-- Thời gian đã tạo: Th10 04, 2025 lúc 10:38 AM
-- Phiên bản máy phục vụ: 10.4.32-MariaDB
-- Phiên bản PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Cơ sở dữ liệu: `qlythuoccaocap`
--

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `danhmuc`
--

CREATE TABLE `danhmuc` (
  `id` int(10) UNSIGNED NOT NULL,
  `ten` varchar(150) NOT NULL,
  `slug` varchar(180) NOT NULL,
  `mo_ta` text DEFAULT NULL,
  `thu_tu` int(11) NOT NULL DEFAULT 0,
  `hien_thi` tinyint(1) NOT NULL DEFAULT 1,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `danhmuc`
--

INSERT INTO `danhmuc` (`id`, `ten`, `slug`, `mo_ta`, `thu_tu`, `hien_thi`, `created_at`, `updated_at`) VALUES
(1, 'Hot Sale', 'hot-sale', 'hot sale lon', 0, 1, '2025-11-04 09:53:49', '2025-11-04 10:21:21'),
(2, 'Mỹ phẩm Gia Bảo', 'thuoc', 'Uống vào đẹp trai như thầy Nhã', 0, 1, '2025-11-04 09:53:49', '2025-11-04 10:23:39'),
(3, 'Thực phẩm chức năng', 'thuc-pham-chuc-nang', NULL, 0, 1, '2025-11-04 09:53:49', '2025-11-04 09:53:49'),
(4, 'Thiết bị, dụng cụ y tế', 'thiet-bi-dung-cu-y-te', 'Bệnh viện', 0, 1, '2025-11-04 09:53:49', '2025-11-04 10:32:30'),
(5, 'Dược mỹ phẩm', 'duoc-my-pham', NULL, 0, 1, '2025-11-04 09:53:49', '2025-11-04 09:53:49'),
(6, 'Chăm sóc cá nhân', 'cham-soc-ca-nhan', NULL, 0, 1, '2025-11-04 09:53:49', '2025-11-04 09:53:49'),
(7, 'Chăm sóc trẻ em', 'cham-soc-tre-em', 'None', 0, 1, '2025-11-04 09:53:49', '2025-11-04 10:32:06'),
(13, 'Đồ dùng', 'o-dung', 'Đinh Gia Bảo', 0, 1, '2025-11-04 10:36:07', '2025-11-04 10:36:07'),
(17, 'Cá nhân', 'ca-nhan', '123', 0, 1, '2025-11-04 10:37:05', '2025-11-04 10:37:05'),
(18, 'Thuốc đông y', 'thuoc-ong-y', 'uống vào khỏi hẳn', 0, 1, '2025-11-04 10:37:20', '2025-11-04 10:37:20'),
(19, 'Quần áo', 'quan-ao', 'mặc vào thành ca sĩ', 0, 1, '2025-11-04 10:37:49', '2025-11-04 10:37:49');

--
-- Chỉ mục cho các bảng đã đổ
--

--
-- Chỉ mục cho bảng `danhmuc`
--
ALTER TABLE `danhmuc`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_danhmuc_slug` (`slug`);

--
-- AUTO_INCREMENT cho các bảng đã đổ
--

--
-- AUTO_INCREMENT cho bảng `danhmuc`
--
ALTER TABLE `danhmuc`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
