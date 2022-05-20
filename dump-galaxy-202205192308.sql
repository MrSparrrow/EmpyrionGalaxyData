-- MySQL dump 10.13  Distrib 8.0.24, for Win64 (x86_64)
--
-- Host: 34.148.86.190    Database: galaxy
-- ------------------------------------------------------
-- Server version	8.0.26-google

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ 'a6adc139-d474-11ec-ad07-42010a8e0002:1-75976';

--
-- Table structure for table `Planets`
--

DROP TABLE IF EXISTS `Planets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Planets` (
  `system_id` int NOT NULL,
  `planet_id` int NOT NULL AUTO_INCREMENT,
  `planet_name` varchar(50) NOT NULL,
  `planet_type` varchar(50) NOT NULL,
  `isStarter` tinyint(1) DEFAULT NULL,
  `loc_x` int DEFAULT NULL,
  `loc_y` int DEFAULT NULL,
  `loc_z` int DEFAULT NULL,
  PRIMARY KEY (`planet_id`),
  KEY `system_id` (`system_id`),
  CONSTRAINT `Planets_ibfk_1` FOREIGN KEY (`system_id`) REFERENCES `Systems` (`system_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Planets`
--

LOCK TABLES `Planets` WRITE;
/*!40000 ALTER TABLE `Planets` DISABLE KEYS */;
INSERT INTO `Planets` VALUES (1,1,'Omicron','Desert',1,100,50,0);
INSERT INTO `Planets` VALUES (2,2,'Akua','Temperate',1,0,0,0);
INSERT INTO `Planets` VALUES (1,3,'Ningues','Ice',1,100,100,100);
INSERT INTO `Planets` VALUES (2,4,'Roggery','Swamp',1,50,0,50);
INSERT INTO `Planets` VALUES (3,5,'Rogue','Dead',0,1000,150,850);
INSERT INTO `Planets` VALUES (3,6,'Mori','Barren',0,500,-150,1200);
INSERT INTO `Planets` VALUES (1,11,'Bar','Desert',NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `Planets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Resources`
--

DROP TABLE IF EXISTS `Resources`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Resources` (
  `planet_id` int NOT NULL,
  `resource_id` int NOT NULL AUTO_INCREMENT,
  `resource_name` varchar(50) NOT NULL,
  `resource_quantity` int NOT NULL,
  `loc_x` int DEFAULT NULL,
  `loc_y` int DEFAULT NULL,
  `loc_z` int DEFAULT NULL,
  PRIMARY KEY (`resource_id`),
  KEY `planet_id` (`planet_id`),
  CONSTRAINT `Resources_ibfk_1` FOREIGN KEY (`planet_id`) REFERENCES `Planets` (`planet_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Resources`
--

LOCK TABLES `Resources` WRITE;
/*!40000 ALTER TABLE `Resources` DISABLE KEYS */;
INSERT INTO `Resources` VALUES (1,1,'Iron',100,2000,500,0);
INSERT INTO `Resources` VALUES (2,2,'Silicon',100,2000,500,0);
INSERT INTO `Resources` VALUES (3,3,'Cobalt',100,2000,500,0);
INSERT INTO `Resources` VALUES (4,4,'Copper',100,2000,500,0);
INSERT INTO `Resources` VALUES (1,5,'Neodymium',100,2000,500,0);
INSERT INTO `Resources` VALUES (2,6,'Neodymium',100,2000,500,0);
INSERT INTO `Resources` VALUES (3,7,'Neodymium',100,2000,500,0);
INSERT INTO `Resources` VALUES (4,8,'Neodymium',100,2000,500,0);
INSERT INTO `Resources` VALUES (5,9,'Zascosium',250,0,250,0);
INSERT INTO `Resources` VALUES (5,10,'Erestrum',150,800,200,120);
INSERT INTO `Resources` VALUES (6,11,'Tungsten',20,50,150,80);
/*!40000 ALTER TABLE `Resources` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `SimpleGalaxyInfo`
--

DROP TABLE IF EXISTS `SimpleGalaxyInfo`;
/*!50001 DROP VIEW IF EXISTS `SimpleGalaxyInfo`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `SimpleGalaxyInfo` AS SELECT 
 1 AS `system_name`,
 1 AS `system_id`,
 1 AS `system_class`,
 1 AS `planet_name`,
 1 AS `planet_id`,
 1 AS `planet_type`,
 1 AS `resource_name`,
 1 AS `resource_id`,
 1 AS `resource_quantity`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `Systems`
--

DROP TABLE IF EXISTS `Systems`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Systems` (
  `system_id` int NOT NULL AUTO_INCREMENT,
  `system_name` varchar(25) NOT NULL,
  `system_class` varchar(5) NOT NULL,
  `loc_x` int DEFAULT NULL,
  `loc_y` int DEFAULT NULL,
  `loc_z` int DEFAULT NULL,
  PRIMARY KEY (`system_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Systems`
--

LOCK TABLES `Systems` WRITE;
/*!40000 ALTER TABLE `Systems` DISABLE KEYS */;
INSERT INTO `Systems` VALUES (1,'Beta','F',50,100,0);
INSERT INTO `Systems` VALUES (2,'Delta','A',0,0,100);
INSERT INTO `Systems` VALUES (3,'Epsilon','K',250,0,500);
/*!40000 ALTER TABLE `Systems` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'galaxy'
--

--
-- Final view structure for view `SimpleGalaxyInfo`
--

/*!50001 DROP VIEW IF EXISTS `SimpleGalaxyInfo`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `SimpleGalaxyInfo` AS select `s`.`system_name` AS `system_name`,`s`.`system_id` AS `system_id`,`s`.`system_class` AS `system_class`,`p`.`planet_name` AS `planet_name`,`p`.`planet_id` AS `planet_id`,`p`.`planet_type` AS `planet_type`,`r`.`resource_name` AS `resource_name`,`r`.`resource_id` AS `resource_id`,`r`.`resource_quantity` AS `resource_quantity` from ((`Systems` `s` join `Planets` `p` on((`s`.`system_id` = `p`.`system_id`))) left join `Resources` `r` on((`p`.`planet_id` = `r`.`planet_id`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-05-19 23:08:26
