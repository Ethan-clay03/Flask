-- MySQL dump 10.13  Distrib 8.0.32, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: mydatabase
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `bookings`
--

DROP TABLE IF EXISTS `bookings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bookings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `listing_id` int NOT NULL,
  `amount_paid` float NOT NULL,
  `seat_type` varchar(50) NOT NULL,
  `num_seats` int NOT NULL,
  `booking_date` date NOT NULL,
  `depart_date` date NOT NULL,
  `last_four_card_nums` varchar(4) NOT NULL,
  `cancelled` tinyint(1) NOT NULL,
  `cancelled_date` date DEFAULT NULL,
  `refund_amount` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `listing_id` (`listing_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `bookings_ibfk_1` FOREIGN KEY (`listing_id`) REFERENCES `listings` (`id`) ON DELETE CASCADE,
  CONSTRAINT `bookings_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bookings`
--

LOCK TABLES `bookings` WRITE;
/*!40000 ALTER TABLE `bookings` DISABLE KEYS */;
INSERT INTO `bookings` VALUES (17,4,17,90,'economy',1,'2025-02-17','2025-02-17','6494',1,'2025-02-24',NULL),(18,4,23,450,'economy',5,'2025-02-17','2025-02-17','4379',1,'2025-02-20',NULL),(19,4,17,90,'economy',1,'2025-02-24','2025-02-24','6466',1,'2025-02-24',NULL),(20,4,17,90,'economy',1,'2025-02-24','2025-02-24','3933',1,'2025-02-24',NULL),(21,4,17,90,'economy',1,'2025-02-24','2025-02-24','3333',1,'2025-02-24',NULL),(22,4,23,90,'economy',1,'2025-02-24','2025-02-24','3333',1,'2025-02-24',0),(23,4,23,90,'economy',1,'2025-02-24','2025-02-24','3333',0,NULL,NULL),(24,4,23,67.5,'economy',1,'2025-02-24','2025-05-22','3333',1,'2025-02-24',67.5),(25,4,17,405,'business',3,'2025-04-27','2025-07-24','1211',1,'2025-04-27',405),(26,22,17,405,'business',3,'2025-04-27','2025-07-25','1211',1,'2025-04-27',405),(27,23,17,540,'business',4,'2025-04-27','2025-07-25','3939',1,'2025-04-27',540);
/*!40000 ALTER TABLE `bookings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `listing_availability`
--

DROP TABLE IF EXISTS `listing_availability`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `listing_availability` (
  `id` int NOT NULL AUTO_INCREMENT,
  `listing_id` int NOT NULL,
  `date` date NOT NULL,
  `air_economy_seats` int NOT NULL DEFAULT '104',
  `air_business_seats` int NOT NULL DEFAULT '26',
  PRIMARY KEY (`id`),
  KEY `listing_id` (`listing_id`),
  CONSTRAINT `listing_availability_ibfk_1` FOREIGN KEY (`listing_id`) REFERENCES `listings` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `listing_availability`
--

LOCK TABLES `listing_availability` WRITE;
/*!40000 ALTER TABLE `listing_availability` DISABLE KEYS */;
INSERT INTO `listing_availability` VALUES (6,23,'2025-02-17',99,26),(7,17,'2025-02-24',101,26),(8,23,'2025-02-24',102,26),(9,23,'2025-05-22',103,26),(10,17,'2025-07-24',104,23),(11,17,'2025-07-25',104,19);
/*!40000 ALTER TABLE `listing_availability` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `listing_images`
--

DROP TABLE IF EXISTS `listing_images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `listing_images` (
  `id` int NOT NULL AUTO_INCREMENT,
  `listing_id` int NOT NULL,
  `image_location` varchar(255) NOT NULL,
  `main_image` smallint NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `listing_id` (`listing_id`),
  CONSTRAINT `listing_images_ibfk_1` FOREIGN KEY (`listing_id`) REFERENCES `listings` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=70 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `listing_images`
--

LOCK TABLES `listing_images` WRITE;
/*!40000 ALTER TABLE `listing_images` DISABLE KEYS */;
INSERT INTO `listing_images` VALUES (62,17,'17_f4d9efcbc6114c77982c11a5f6a4ae32.jpeg',1),(63,17,'17_b8826e38386d483ca9306d14d7578198.jpeg',0),(64,23,'23_1794fce261724f8c9cf66c32ea41c8ec.jpeg',1),(65,23,'23_e993b069266a40b1adc86dde1ba9833a.jpeg',0),(66,24,'24_4e7eaca89d8e4e80b5b313619bfc3c96.jpeg',1),(67,24,'24_ad7c0a52b61d4bfa8c9667238b83c025.jpeg',0),(68,25,'25_d64dce962e0e48c6ae30c7d9a6182b3e.jpeg',1),(69,26,'26_b48c3c36459945ad88ba96a417f607f5.jpeg',1);
/*!40000 ALTER TABLE `listing_images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `listings`
--

DROP TABLE IF EXISTS `listings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `listings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `depart_location` varchar(255) NOT NULL,
  `depart_time` time NOT NULL,
  `destination_location` varchar(255) NOT NULL,
  `destination_time` time NOT NULL,
  `economy_fair_cost` float NOT NULL,
  `business_fair_cost` float DEFAULT NULL,
  `transport_type` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `listings`
--

LOCK TABLES `listings` WRITE;
/*!40000 ALTER TABLE `listings` DISABLE KEYS */;
INSERT INTO `listings` VALUES (17,'Newcastle','17:45:00','Bristol','19:00:00',90,180,'Airplane'),(23,'Bristol','09:00:00','Newcastle','10:15:00',90,180,'Airplane'),(24,'Cardiff','07:00:00','Edinburgh','08:30:00',90,180,'Airplane'),(25,'Bristol','12:30:00','Manchester','13:30:00',80,160,'Airplane'),(26,'Manchester','13:20:00','Bristol','14:20:00',80,160,'Airplane'),(27,'Bristol','07:40:00','London','08:20:00',80,160,'Airplane'),(28,'London','13:00:00','Manchester','14:00:00',100,200,'Airplane'),(29,'Manchester','12:20:00','Glasgow','13:30:00',100,200,'Airplane'),(30,'Bristol','08:40:00','Glasgow','09:45:00',110,220,'Airplane'),(31,'Glasgow','14:30:00','Newcastle','15:45:00',100,200,'Airplane'),(32,'Newcastle','16:15:00','Manchester','17:05:00',100,200,'Airplane'),(33,'Manchester','18:25:00','Bristol','19:30:00',80,160,'Airplane'),(34,'Bristol','06:20:00','Manchester','07:20:00',80,160,'Airplane'),(35,'Portsmouth','12:00:00','Dundee','14:00:00',120,240,'Airplane'),(36,'Dundee','10:00:00','Portsmouth','12:00:00',120,240,'Airplane'),(37,'Edinburgh','18:30:00','Cardiff','20:00:00',90,180,'Airplane'),(38,'Southampton','12:00:00','Manchester','13:30:00',90,180,'Airplane'),(39,'Manchester','19:00:00','Southampton','20:30:00',90,180,'Airplane'),(40,'Birmingham','17:00:00','Newcastle','17:45:00',100,200,'Airplane'),(41,'Newcastle','07:00:00','Birmingham','07:45:00',100,200,'Airplane'),(42,'Aberdeen','08:00:00','Portsmouth','09:30:00',100,200,'Airplane');
/*!40000 ALTER TABLE `listings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(80) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'super-admin','Super Admin, all admin perms and can create new admins'),(2,'admin','Can create/delete and modify bookings'),(3,'user','Standard user');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `fs_uniquifier` varchar(64) NOT NULL,
  `role_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `fs_uniquifier` (`fs_uniquifier`),
  UNIQUE KEY `fs_uniquifier_2` (`fs_uniquifier`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (3,'ethan-admin','ethana@gmail.com','pbkdf2:sha256:1000000$KLEXQcswJYJuZ8xf$afe1a0bb9fa87afbc6aa1e672b9b0474733311cedfcd2c81585ae10e786b10dc','1fa9452306c06ba227f1081f2573cd2fd80d27e83beb0de4b776308fde22acd1',2),(4,'ethan-root','ethan@email.com','pbkdf2:sha256:1000000$h2bDsdVYQa5hIUZf$09e9fd93e8040fde8c97ce9be8f6ede36ab5f5a83bafb4427c0b0e20b8095a0d','ed662a222a3abc0536fceffda483134def08b339ed73c34e0bb4ca8740389319',1),(22,'ethan-user','ethanu@gmail.com','pbkdf2:sha256:1000000$AmXlwMIiU31QnGf1$dea3f9aa829ab2733de46e39c03e825e3f13d1bc57ffd017a49dc0501279ad73','31561dee6b23790959b65268a42b350798c3c966c41fb5898abfd4ef493af530',3),(23,'ethan-username121','ethan1@email.comm','pbkdf2:sha256:1000000$hsjXY6F9PXr9b2xs$b543f8eca6ae75a382edfdec12e79fed6b4517b534d4cf603578f46967262760','a23fb47f07c25246a778b6e39cdb337c8e1c446526d95b12b05b03d9fc05cb59',3);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-27 22:09:36
