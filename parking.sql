-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 07, 2024 at 01:31 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `parking`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `email`, `password`) VALUES
(1, 'admin@gmail.com', '123456');

-- --------------------------------------------------------

--
-- Table structure for table `free_parking`
--

CREATE TABLE `free_parking` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `vehicle_id` int(11) NOT NULL,
  `location_id` int(11) DEFAULT NULL,
  `parking_date` varchar(255) DEFAULT NULL,
  `parking_time` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `free_parking`
--

INSERT INTO `free_parking` (`id`, `user_id`, `vehicle_id`, `location_id`, `parking_date`, `parking_time`) VALUES
(19, 3, 2, 6, '2023-12-17', '23:27'),
(20, 3, 2, 6, '2023-12-18', '01:30'),
(21, 3, 2, 7, '2023-12-19', '02:32'),
(22, 3, 2, 8, '2023-12-20', '04:30'),
(23, 3, 2, 8, '2023-12-25', '22:28');

-- --------------------------------------------------------

--
-- Table structure for table `locations`
--

CREATE TABLE `locations` (
  `id` int(11) NOT NULL,
  `place_name` varchar(500) DEFAULT NULL,
  `latitude` varchar(500) DEFAULT NULL,
  `longitude` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `locations`
--

INSERT INTO `locations` (`id`, `place_name`, `latitude`, `longitude`) VALUES
(6, 'Trafalgar Square, Seven Dials, Covent Garden, City of Westminster, Greater London, England, WC2N 5EJ, United Kingdom', '51.50787970770442', '-0.12775737086485608'),
(7, 'Sophia Road, Custom House, Canning Town, London Borough of Newham, London, Greater London, England, E16 3PF, United Kingdom', '51.51572132739546', '0.026222884262097075'),
(8, 'Carriage Drive West, Battersea, London Borough of Wandsworth, London, Greater London, England, SW11 4PZ, United Kingdom', '51.47748469283738', '-0.161832958656305'),
(9, 'Felsham Road, London Borough of Wandsworth, London, Greater London, England, SW15 1DW, United Kingdom', '51.46648453707899', '-0.22069135327910774');

-- --------------------------------------------------------

--
-- Table structure for table `paid_parking`
--

CREATE TABLE `paid_parking` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `vehicle_id` int(11) NOT NULL,
  `location_id` int(11) DEFAULT NULL,
  `parking_date` varchar(255) DEFAULT NULL,
  `parking_time` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `subscription`
--

CREATE TABLE `subscription` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `card_number` varchar(255) NOT NULL,
  `expiry` varchar(255) NOT NULL,
  `cvv` varchar(255) NOT NULL,
  `cardholder_name` varchar(255) NOT NULL,
  `txn_id` varchar(255) NOT NULL,
  `startdatetime` varchar(255) DEFAULT NULL,
  `enddatetime` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `subscription`
--

INSERT INTO `subscription` (`id`, `user_id`, `card_number`, `expiry`, `cvv`, `cardholder_name`, `txn_id`, `startdatetime`, `enddatetime`) VALUES
(4, 3, '1234567890123456', '02/25', '232', 'testuser', '237E944E030F', '2023-12-17 22:28:44.072697', '2024-01-16 22:28:44.072697');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `password`) VALUES
(3, 'testuser', 'testuser@gmail.com', '$2b$12$jASgLrZptXoLp87bt98p.uZ7ewZfLHSHWiEIby1ju/1yODfRDPBBe');

-- --------------------------------------------------------

--
-- Table structure for table `vehicles`
--

CREATE TABLE `vehicles` (
  `id` int(11) NOT NULL,
  `vehicle_no` varchar(255) DEFAULT NULL,
  `owner_name` varchar(255) DEFAULT NULL,
  `owner_address` varchar(255) DEFAULT NULL,
  `owner_dob` varchar(255) DEFAULT NULL,
  `owner_license_type` varchar(255) DEFAULT NULL,
  `owner_license_no` varchar(255) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `vehicles`
--

INSERT INTO `vehicles` (`id`, `vehicle_no`, `owner_name`, `owner_address`, `owner_dob`, `owner_license_type`, `owner_license_no`, `user_id`) VALUES
(2, '1234567890', 'testuser', 'New Delhi', '2003-01-21', 'permanent', '7894561230123456', 3);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `free_parking`
--
ALTER TABLE `free_parking`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `locations`
--
ALTER TABLE `locations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `paid_parking`
--
ALTER TABLE `paid_parking`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `subscription`
--
ALTER TABLE `subscription`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `vehicles`
--
ALTER TABLE `vehicles`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `free_parking`
--
ALTER TABLE `free_parking`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `locations`
--
ALTER TABLE `locations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `paid_parking`
--
ALTER TABLE `paid_parking`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `subscription`
--
ALTER TABLE `subscription`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `vehicles`
--
ALTER TABLE `vehicles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
