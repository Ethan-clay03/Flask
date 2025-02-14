CREATE DATABASE  IF NOT EXISTS `mydatabase` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `mydatabase`;
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
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('ce28a5ddecee');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

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
  `amount_paid` int NOT NULL,
  `seat_type` varchar(50) NOT NULL,
  `num_seats` int NOT NULL,
  `cancelled` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `listing_id` (`listing_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `bookings_ibfk_1` FOREIGN KEY (`listing_id`) REFERENCES `listings` (`id`) ON DELETE CASCADE,
  CONSTRAINT `bookings_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bookings`
--

LOCK TABLES `bookings` WRITE;
/*!40000 ALTER TABLE `bookings` DISABLE KEYS */;
INSERT INTO `bookings` VALUES (6,4,17,270,'economy',3,0),(7,4,17,900,'business',5,0);
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `listing_availability`
--

LOCK TABLES `listing_availability` WRITE;
/*!40000 ALTER TABLE `listing_availability` DISABLE KEYS */;
INSERT INTO `listing_availability` VALUES (3,17,'2025-02-13',101,21);
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
  `image_description` varchar(255) DEFAULT NULL,
  `main_image` smallint NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `listing_id` (`listing_id`),
  CONSTRAINT `listing_images_ibfk_1` FOREIGN KEY (`listing_id`) REFERENCES `listings` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `listing_images`
--

LOCK TABLES `listing_images` WRITE;
/*!40000 ALTER TABLE `listing_images` DISABLE KEYS */;
INSERT INTO `listing_images` VALUES (58,17,'17_2d852af9f5b64b1abdd5784e8172ce6e.gif',NULL,1);
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
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (3,'ere','ethanclay2017@gmail.com','pbkdf2:sha256:1000000$KLEXQcswJYJuZ8xf$afe1a0bb9fa87afbc6aa1e672b9b0474733311cedfcd2c81585ae10e786b10dc','1fa9452306c06ba227f1081f2573cd2fd80d27e83beb0de4b776308fde22acd1',3),(4,'ethan-root','ethan@email.com','pbkdf2:sha256:1000000$h2bDsdVYQa5hIUZf$09e9fd93e8040fde8c97ce9be8f6ede36ab5f5a83bafb4427c0b0e20b8095a0d','ed662a222a3abc0536fceffda483134def08b339ed73c34e0bb4ca8740389319',1),(5,'64565','dfgfdgfd@gjkonfd.com','pbkdf2:sha256:1000000$YPhFWaRsQeFO1MXe$378bb9e49e2b3e004a0dcfbbbd0af36168d0cc421df7447cfffcf2f0f6ffdee7','823c308e7124145efb8d114b3fe92a960895abda3a904539fe3f68784a9a383d',3),(7,'hgh','hfg@gsdfgnj.com','pbkdf2:sha256:1000000$jOK9q73AdlYw9Zx4$962b9371d7f2ef6d922b50a787e2973574398520f402afd0ddaa0091e007b704','e38b60063929f2faca986b251087d202247a0491258d6e3217c8432eca6fd497',3),(8,'dsfdsfd','sdfd@sfjdifon.com','pbkdf2:sha256:1000000$lbfHzBP6QezPfWJV$5bcff242a0481be1dc934d0aee31d69a6c014127cba8ed208d8929f80f68741c','980d1003086ab1f68e4beb522f9f032dd40c2cb565f4ab3e484e35cf9500f77c',3),(9,'ghjofdgjofigjoi','sdoijf@fsidjf.com','pbkdf2:sha256:1000000$5eExQbI4OvzPeDAO$43116e45de77bc55441d04fb9b9755c26a830393cee9c851343f52b22c7eecb9','b7bddaf30a867146be078ca1f76e16e69f4e7009c8001ba3e5982f93951af72d',3),(10,'vsdnfjvhdvsouij','zxhjcxzkhjl@vhjovfdhn.com','pbkdf2:sha256:1000000$WAq9HaVAfljL1P5n$8ff8d607cddc475557cb23070e7cb6d0ce3a870103ed993c16d999e9c00f23e1','7a6b788885bae598cc5bd9a157498a6da0ec96329f481036f0d08a8e399114e5',3),(11,'fsdfdsfuoh','dshfoiudh@sfodifj.com','pbkdf2:sha256:1000000$oOlS1KqrcgGyoqQm$4c9b55b07d259c7c62833777ac26af3190c86dccf124e83a005e2bfb26669f43','502e720f49250d0ecade74d9e78a5b6d6885de87a0b647a82aa831a8747e79bd',3),(12,'abc','abc@abc.com','pbkdf2:sha256:1000000$Jxzoy9sxTGqGHwiw$40a6f1a57d195d29c0aef1e637755d3c0f928cc28179afb44aa637bde30c67e0','561bc7776ddb3637df3d9bb2fb968e466fd69811e8ef24b318323ac2f231a03b',3),(13,'zxczxcz','zxoijc@vsiodjvd.com','pbkdf2:sha256:1000000$4rlYBHcwN4J4shjz$10a3620747ce9cd9c74d2389ddf54f79836d48d330043af057ae1729b5b9d80a','1c00d83fa89fb06d0d188aa3d93af8e396d21ec8a2a2ed79e3f73694b9f18ef3',3),(14,'fdggyfuigyfudi','dfsuify@dgyufdi.com','pbkdf2:sha256:1000000$WLrKJbAxAyjdVf6L$7238f06e6d6b178935193b85eba4f04d50dff9c7141aad891c1b42f78b23db2e','2484df7f3be68bc30cf679e187cba0bf725c9abdab8f8bd6f36f34e1a88279bf',3),(15,'ethan','e@e.com','pbkdf2:sha256:1000000$lwDjZg0Y11JnOPHw$044b346f4378f2e75fa60dc367e608097dfd845830b7202cbac1bb604ee3b4fe','8e5ed3d7d9e2d88d4c8c63fce9e3889e88424cada91a0c39e254092b416072f6',2),(16,'urdsitur9898','fsduiofdujio@oiscgfjiods.com','pbkdf2:sha256:1000000$WHTfGYXEIAB90YTW$779abcc3b34a00e172725dbecc5d768172453be5cd21ac10912c9e5c2eb60ef4','09438ff7487d5bc54a4a0d04193e092809086464aefdbf0a511dec7e01ac6c4e',3),(17,'ufsdfhuio','sdfuihds@sdoifhj.com','pbkdf2:sha256:1000000$osxKbywtVHGEx3EO$09795c29d5fe10dadb79f6ff1a45b8633042c443581d24df611adbdcad077c20','788db016c51a08692a35bf2020cdec94074599c5b41243b24c47373e56e81114',3);
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

-- Dump completed on 2025-02-14  8:16:55
