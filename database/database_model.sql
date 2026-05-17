-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: localhost    Database: mydb
-- ------------------------------------------------------
-- Server version	8.0.45

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
-- Table structure for table `files`
--
USE mydb;
DROP TABLE IF EXISTS `files`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `files` (
  `file_id` int NOT NULL AUTO_INCREMENT,
  `file_name` varchar(45) NOT NULL,
  `file_path` varchar(500) NOT NULL,
  PRIMARY KEY (`file_id`),
  UNIQUE KEY `File_Path_UNIQUE` (`file_path`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `files`
--

LOCK TABLES `files` WRITE;
/*!40000 ALTER TABLE `files` DISABLE KEYS */;
/*!40000 ALTER TABLE `files` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `job_models`
--

DROP TABLE IF EXISTS `job_models`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `job_models` (
  `serial_no` int NOT NULL AUTO_INCREMENT,
  `job_id` int NOT NULL,
  `model_id` int NOT NULL,
  PRIMARY KEY (`serial_no`),
  KEY `FK_job_models_model_id_idx` (`model_id`),
  KEY `FK_job_models_job_id_idx` (`job_id`),

  CONSTRAINT `FK_job_models_job_id` FOREIGN KEY (`job_id`) REFERENCES `scan_jobs` (`job_id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `FK_job_models_model_id` FOREIGN KEY (`model_id`) REFERENCES `models` (`model_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='	';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `job_models`
--

LOCK TABLES `job_models` WRITE;
/*!40000 ALTER TABLE `job_models` DISABLE KEYS */;
/*!40000 ALTER TABLE `job_models` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `models`
--

DROP TABLE IF EXISTS `models`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `models` (
  `model_id` int NOT NULL AUTO_INCREMENT,
  `model_path` varchar(500) NOT NULL,
  `enabled_flag` tinyint NOT NULL DEFAULT '1',
  `task` varchar(45) NOT NULL,
  PRIMARY KEY (`model_id`),
  UNIQUE KEY `Model_ID_UNIQUE` (`model_id`),
  UNIQUE KEY `Model_Path_UNIQUE` (`model_path`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `models`
--

LOCK TABLES `models` WRITE;
/*!40000 ALTER TABLE `models` DISABLE KEYS */;
INSERT INTO `models` VALUES (1,'C:\\Users\\khushib\\Documents\\github\\Classifier\\Training\\models\\adult_model.pkl',1,'Adult'),(2,'C:\\Users\\khushib\\Documents\\github\\Classifier\\Training\\models\\data_type_model.pkl',1,'DT'),(3,'C:\\Users\\khushib\\Documents\\github\\Classifier\\Training\\models\\sensitivity_model.pkl',1,'Sens');
/*!40000 ALTER TABLE `models` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `path`
--

DROP TABLE IF EXISTS `path`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `path` (
  `path_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `path` varchar(500) NOT NULL,
  `allowed_flag` tinyint NOT NULL DEFAULT '1',
  PRIMARY KEY (`path_id`),
  UNIQUE KEY `Path_UNIQUE` (`path`),
  UNIQUE KEY `Path_ID_UNIQUE` (`path_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `path`
--

LOCK TABLES `path` WRITE;
/*!40000 ALTER TABLE `path` DISABLE KEYS */;
INSERT INTO `path` VALUES (1,'Root','C:\\Users\\khushib\\Documents',1);
/*!40000 ALTER TABLE `path` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `regex`
--

DROP TABLE IF EXISTS `regex`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `regex` (
  `regex_id` int NOT NULL AUTO_INCREMENT,
  `pattern` varchar(200) NOT NULL,
  `enabled_flag` tinyint NOT NULL DEFAULT '1',
  `name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`regex_id`),
  UNIQUE KEY `Pattern_UNIQUE` (`pattern`),
  UNIQUE KEY `Regex_ID_UNIQUE` (`regex_id`) /*!80000 INVISIBLE */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `regex`
--

LOCK TABLES `regex` WRITE;
/*!40000 ALTER TABLE `regex` DISABLE KEYS */;
INSERT INTO `regex` VALUES (1,'[A-Z]{5}[0-9]{4}[A-Z]{1}',1,'PAN'),(2,'[0-9]{4}[ -]?[0-9]{4}[ -]?[0-9]{4}',1,'Adhaar'),(3,'(0[1-9]|1[012])[-/.](0[1-9]|[12][0-9]|3[01])[-/.](19|20)\\\\d\\\\d',1,'DOB'),(4,'[A-Z][1-9]\\d\\s?\\d{4}[1-9]',1,'Passport'),(5,'[A-Z]{3}\\d{7}',1,'Voter id'),(6,'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\\\.[a-zA-Z]{2,}',1,'Email'),(7,'(\\+91[\\-\\s]?)?(\\91[\\-\\s]?)?[0]?(91)?[123456789]\\d{9}',1,'Phone');
/*!40000 ALTER TABLE `regex` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scan_detections`
--

DROP TABLE IF EXISTS `scan_detections`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `scan_detections` (
  `serial_id` int NOT NULL AUTO_INCREMENT,
  `file_id` int NOT NULL,
  `job_id` int NOT NULL,
  `datatype` varchar(45) NOT NULL,
  `sensitivity` varchar(45) NOT NULL,
  `count` int DEFAULT NULL,
  PRIMARY KEY (`serial_id`),
  KEY `FK_scan_detections_file_id_idx` (`file_id`),
  KEY `FK_scan_detections_job_id_idx` (`job_id`),
  CONSTRAINT `FK_scan_detections_file_id` FOREIGN KEY (`file_id`) REFERENCES `files` (`file_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FK_scan_detections_job_id` FOREIGN KEY (`job_id`) REFERENCES `scan_jobs` (`job_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scan_detections`
--

LOCK TABLES `scan_detections` WRITE;
/*!40000 ALTER TABLE `scan_detections` DISABLE KEYS */;
/*!40000 ALTER TABLE `scan_detections` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scan_jobs`
--

DROP TABLE IF EXISTS `scan_jobs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `scan_jobs` (
  `job_id` int NOT NULL AUTO_INCREMENT,
  `started_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `ended_at` datetime NULL,
  `status` varchar(45) NOT NULL,
  PRIMARY KEY (`job_id`),
  UNIQUE KEY `Job_ID_UNIQUE` (`job_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scan_jobs`
--

LOCK TABLES `scan_jobs` WRITE;
/*!40000 ALTER TABLE `scan_jobs` DISABLE KEYS */;
/*!40000 ALTER TABLE `scan_jobs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scan_records`
--

DROP TABLE IF EXISTS `scan_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `scan_records` (
  `serial_no` int NOT NULL AUTO_INCREMENT,
  `job_id` int NOT NULL,
  `file_id` int NOT NULL,
  `timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`serial_no`),
  KEY `FK_scan_records_job_id_idx` (`job_id`),
  KEY `FK_scan_records_file_id_idx` (`file_id`),
  CONSTRAINT `FK_scan_records_file_id` FOREIGN KEY (`file_id`) REFERENCES `files` (`file_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FK_scan_records_job_id` FOREIGN KEY (`job_id`) REFERENCES `scan_jobs` (`job_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scan_records`
--

LOCK TABLES `scan_records` WRITE;
/*!40000 ALTER TABLE `scan_records` DISABLE KEYS */;
/*!40000 ALTER TABLE `scan_records` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-31 13:45:46
