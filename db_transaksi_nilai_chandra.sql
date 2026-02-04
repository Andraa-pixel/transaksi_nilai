-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 04, 2026 at 02:53 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_transaksi_nilai_chandra`
--

-- --------------------------------------------------------

--
-- Table structure for table `tbl_absensi_chandra`
--

CREATE TABLE `tbl_absensi_chandra` (
  `id_absen` int(11) NOT NULL,
  `NIS_CHANDRA` int(11) NOT NULL,
  `sakit` int(11) NOT NULL,
  `izin` int(11) NOT NULL,
  `alfa` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_absensi_chandra`
--

INSERT INTO `tbl_absensi_chandra` (`id_absen`, `NIS_CHANDRA`, `sakit`, `izin`, `alfa`) VALUES
(1, 1001, 1, 0, 0),
(2, 1002, 2, 0, 0),
(3, 1003, 3, 0, 0),
(4, 1004, 1, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `tbl_kelas_chandra`
--

CREATE TABLE `tbl_kelas_chandra` (
  `id_kelas_chandra` int(11) NOT NULL,
  `nama_kelas_chandra` varchar(100) NOT NULL,
  `wali_kelas_chandra` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_kelas_chandra`
--

INSERT INTO `tbl_kelas_chandra` (`id_kelas_chandra`, `nama_kelas_chandra`, `wali_kelas_chandra`) VALUES
(1, 'X RPL A', 'Budi Santoso'),
(2, 'X RPL B', 'Siti Aminah'),
(3, 'XI RPL A', 'Ahmad Fauzi'),
(4, 'XI RPL B', 'Dewi Lestari');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_mapel_chandra`
--

CREATE TABLE `tbl_mapel_chandra` (
  `id_mapel_chandra` int(11) NOT NULL,
  `nama_mapel_chandra` varchar(100) NOT NULL,
  `kkm_chandra` decimal(10,0) NOT NULL,
  `jenis_mapel_chandra` enum('UMUM','Kejuruan','Pilihan') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_mapel_chandra`
--

INSERT INTO `tbl_mapel_chandra` (`id_mapel_chandra`, `nama_mapel_chandra`, `kkm_chandra`, `jenis_mapel_chandra`) VALUES
(1, 'Matematika', 75, 'UMUM'),
(2, 'Bahasa Indonesia', 75, 'UMUM'),
(3, 'Rekayasa Perangkat Lunak', 75, 'Kejuruan'),
(4, 'KIK', 75, 'Kejuruan'),
(5, 'Bahasa Inggris', 75, 'Kejuruan'),
(6, 'Sejarah', 75, 'UMUM'),
(7, 'PJOK', 75, 'UMUM'),
(8, 'Pendidikan Pancasila', 75, 'UMUM'),
(9, 'PAIBP', 75, 'UMUM'),
(10, 'Bahasa Jepang', 75, 'Pilihan');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_nilai_chandra`
--

CREATE TABLE `tbl_nilai_chandra` (
  `id_nilai_chandra` varchar(100) NOT NULL,
  `NIS_CHANDRA` int(11) NOT NULL,
  `id_mapel_chandra` int(11) NOT NULL,
  `nilai_tugas_chandra` int(11) NOT NULL,
  `nilai_uts_chandra` int(11) NOT NULL,
  `nilai_uas_chandra` int(11) NOT NULL,
  `deskripsi_chandra` enum('Sangat Baik Nilai anda','Tingkatkan lagi nilai','Nilai Anda cukup baik tingkat kan lagi nilai nya','Nilai anda kurang, tingkatkan lagi nilainya','Nilai Anda Sangat Kurang Baik , perbaiki nilai nya') NOT NULL,
  `semester_chandra` int(11) NOT NULL,
  `tahun_ajaran_chandra` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_nilai_chandra`
--

INSERT INTO `tbl_nilai_chandra` (`id_nilai_chandra`, `NIS_CHANDRA`, `id_mapel_chandra`, `nilai_tugas_chandra`, `nilai_uts_chandra`, `nilai_uas_chandra`, `deskripsi_chandra`, `semester_chandra`, `tahun_ajaran_chandra`) VALUES
('N1000', 1002, 2, 90, 91, 91, 'Sangat Baik Nilai anda', 1, '2024-2025'),
('N1001', 1002, 2, 90, 95, 89, 'Sangat Baik Nilai anda', 2, '2025-2026'),
('N1002', 1002, 1, 75, 89, 94, 'Sangat Baik Nilai anda', 1, '2024-2025'),
('N1003', 1001, 1, 95, 90, 95, 'Sangat Baik Nilai anda', 2, '2025-2026'),
('N1004', 1001, 3, 82, 86, 80, 'Tingkatkan lagi nilai', 1, '2024-2025'),
('N1005', 1001, 3, 98, 92, 90, 'Sangat Baik Nilai anda', 2, '2025-2026'),
('N1006', 1001, 4, 25, 75, 27, 'Nilai Anda Sangat Kurang Baik , perbaiki nilai nya', 2, '2025-2026'),
('N1007', 1004, 2, 24, 24, 42, 'Nilai Anda Sangat Kurang Baik , perbaiki nilai nya', 2, '2025-2026'),
('N1008', 1002, 1, 80, 85, 90, 'Sangat Baik Nilai anda', 2, '2025-2026'),
('N1009', 1002, 3, 95, 85, 80, 'Sangat Baik Nilai anda', 1, '2024-2025'),
('N1010', 1001, 4, 85, 80, 75, 'Tingkatkan lagi nilai', 1, '2024-2025'),
('N1011', 1001, 5, 85, 96, 80, 'Tingkatkan lagi nilai', 1, '2024-2025'),
('N1012', 1001, 1, 95, 85, 80, 'Tingkatkan lagi nilai', 1, '2024-2025'),
('N1013', 1001, 6, 90, 85, 85, 'Tingkatkan lagi nilai', 1, '2024-2025'),
('N1014', 1001, 7, 90, 90, 85, 'Tingkatkan lagi nilai', 1, '2024-2025'),
('N1015', 1001, 8, 85, 85, 90, 'Tingkatkan lagi nilai', 1, '2024-2025'),
('N1016', 1001, 9, 90, 85, 85, 'Tingkatkan lagi nilai', 1, '2024-2025'),
('N1017', 1001, 10, 95, 85, 80, 'Tingkatkan lagi nilai', 1, '2024-2025'),
('N1018', 1001, 2, 85, 90, 90, 'Tingkatkan lagi nilai', 1, '2024-2025'),
('N1019', 1002, 4, 90, 90, 85, 'Tingkatkan lagi nilai', 1, '2024-2025'),
('N1020', 1002, 5, 90, 95, 95, 'Sangat Baik Nilai anda', 1, '2024-2025'),
('N1021', 1002, 6, 90, 85, 90, 'Tingkatkan lagi nilai', 1, '2024-2025'),
('N1022', 1002, 7, 90, 85, 85, 'Tingkatkan lagi nilai', 1, '2024-2025'),
('N1023', 1002, 8, 90, 90, 90, 'Sangat Baik Nilai anda', 1, '2024-2025'),
('N1024', 1002, 9, 90, 95, 85, 'Sangat Baik Nilai anda', 1, '2024-2025'),
('N1025', 1002, 10, 90, 95, 80, 'Tingkatkan lagi nilai', 1, '2024-2025');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_siswa_chandra`
--

CREATE TABLE `tbl_siswa_chandra` (
  `NIS_CHANDRA` int(11) NOT NULL,
  `nama_chandra` varchar(100) NOT NULL,
  `tempat_lahir_chandra` varchar(100) NOT NULL,
  `tgl_lahir_chandra` date NOT NULL,
  `alamat_chandra` varchar(255) NOT NULL,
  `id_kelas_chandra` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_siswa_chandra`
--

INSERT INTO `tbl_siswa_chandra` (`NIS_CHANDRA`, `nama_chandra`, `tempat_lahir_chandra`, `tgl_lahir_chandra`, `alamat_chandra`, `id_kelas_chandra`) VALUES
(1001, 'Ahmad Dwi', 'Bandung', '2008-01-12', 'Jl. Merdeka No 1', 1),
(1002, 'Falisha', 'Jakarta', '2008-03-21', 'Jl. Melati No 5', 1),
(1003, 'Ali Supriatno', 'Bogor', '2007-11-02', 'Jl. Mawar No 10', 2),
(1004, 'Wildan Maulana', 'Depok', '2007-07-15', 'Jl. Anggrek No 8', 3);

-- --------------------------------------------------------

--
-- Table structure for table `tbl_users_chandra`
--

CREATE TABLE `tbl_users_chandra` (
  `id_chandra` int(11) NOT NULL,
  `username_chandra` varchar(100) NOT NULL,
  `password_chandra` varchar(100) NOT NULL,
  `role_chandra` enum('admin','guru','walikelas') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_users_chandra`
--

INSERT INTO `tbl_users_chandra` (`id_chandra`, `username_chandra`, `password_chandra`, `role_chandra`) VALUES
(1, 'admin', 'admin123', 'admin'),
(2, 'guru1', 'guru123', 'guru'),
(3, 'walikelas1', 'wali123', 'walikelas'),
(4, 'guru2', 'guru456', 'guru');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tbl_absensi_chandra`
--
ALTER TABLE `tbl_absensi_chandra`
  ADD PRIMARY KEY (`id_absen`),
  ADD KEY `NIS_CHANDRA` (`NIS_CHANDRA`);

--
-- Indexes for table `tbl_kelas_chandra`
--
ALTER TABLE `tbl_kelas_chandra`
  ADD PRIMARY KEY (`id_kelas_chandra`);

--
-- Indexes for table `tbl_mapel_chandra`
--
ALTER TABLE `tbl_mapel_chandra`
  ADD PRIMARY KEY (`id_mapel_chandra`);

--
-- Indexes for table `tbl_nilai_chandra`
--
ALTER TABLE `tbl_nilai_chandra`
  ADD PRIMARY KEY (`id_nilai_chandra`),
  ADD KEY `NIS_CHANDRA` (`NIS_CHANDRA`),
  ADD KEY `id_mapel_chandra` (`id_mapel_chandra`);

--
-- Indexes for table `tbl_siswa_chandra`
--
ALTER TABLE `tbl_siswa_chandra`
  ADD PRIMARY KEY (`NIS_CHANDRA`),
  ADD KEY `id_kelas_chandra` (`id_kelas_chandra`);

--
-- Indexes for table `tbl_users_chandra`
--
ALTER TABLE `tbl_users_chandra`
  ADD PRIMARY KEY (`id_chandra`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tbl_mapel_chandra`
--
ALTER TABLE `tbl_mapel_chandra`
  MODIFY `id_mapel_chandra` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `tbl_absensi_chandra`
--
ALTER TABLE `tbl_absensi_chandra`
  ADD CONSTRAINT `tbl_absensi_chandra_ibfk_1` FOREIGN KEY (`NIS_CHANDRA`) REFERENCES `tbl_siswa_chandra` (`NIS_CHANDRA`);

--
-- Constraints for table `tbl_nilai_chandra`
--
ALTER TABLE `tbl_nilai_chandra`
  ADD CONSTRAINT `tbl_nilai_chandra_ibfk_1` FOREIGN KEY (`id_mapel_chandra`) REFERENCES `tbl_mapel_chandra` (`id_mapel_chandra`),
  ADD CONSTRAINT `tbl_nilai_chandra_ibfk_2` FOREIGN KEY (`NIS_CHANDRA`) REFERENCES `tbl_siswa_chandra` (`NIS_CHANDRA`);

--
-- Constraints for table `tbl_siswa_chandra`
--
ALTER TABLE `tbl_siswa_chandra`
  ADD CONSTRAINT `tbl_siswa_chandra_ibfk_1` FOREIGN KEY (`id_kelas_chandra`) REFERENCES `tbl_kelas_chandra` (`id_kelas_chandra`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
