-- MySQL dump 10.11
--
-- Host: localhost    Database: tests
-- ------------------------------------------------------
-- Server version	5.0.67-community-nt

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
 
--
-- Current Database: `tests`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `tests` /*!40100 DEFAULT CHARACTER SET latin1 */;
 
USE `tests`;
 
--
-- Table structure for table `my_copy_delete_this`
--

DROP TABLE IF EXISTS `my_copy_delete_this`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `my_copy_delete_this` (
  `date` char(20) default NULL,
  `host_machine` char(20) default NULL,
  `test_name` char(20) default NULL,
  `mpi_tasks` int(10) default NULL,
  `cpu_time` float default NULL,
  `cpu_time_2` float default NULL,
  `auto_index` int(12) NOT NULL auto_increment,
  PRIMARY KEY  (`auto_index`)
) ENGINE=MyISAM AUTO_INCREMENT=33 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `my_copy_delete_this`
--

LOCK TABLES `my_copy_delete_this` WRITE;
/*!40000 ALTER TABLE `my_copy_delete_this` DISABLE KEYS */;
INSERT INTO `my_copy_delete_this` VALUES ('January 21, 2009','Unity','Sierra/Presto',2,4.37,1.457,1),('January 21, 2009','Unity','Sierra/Presto',4,5.37,1.79,2),('January 21, 2009','Unity','Sierra/Presto',8,5.77,1.923,3),('January 21, 2009','Unity','Sierra/Presto',16,6.28,2.09,4),('January 21, 2009','Unity','Sierra/Presto',32,7.93,2.643,5),('January 21, 2009','Unity','Sierra/Presto',64,9.88,3.293,6),('January 21, 2009','Unity','Sierra/Presto',128,13.25,4.417,7),('January 21, 2009','Unity','Sierra/Presto',256,16.08,5.36,8),('January 21, 2009','Unity','Sierra/Presto',512,23.02,7.67,9),('January 21, 2009','Unity','Sierra/Presto',1024,38.75,12.9167,10),('July 4, 1900','Discord','Teddy/Roosevelt',275,10.7,3.56667,11),('September 17, 1983','Discord','Teddy/Roosevelt',7,2.88,0.96,12),('May 5 1998','Discord','Teddy/Roosevelt',40,50.88,16.27,13),('May 15 1998','Discord','Teddy/Roosevelt',60,70.88,23.27,14),('May 25 1998','Discord','Teddy/Roosevelt',60,70.88,23.27,15),('May 26 1998','Discord','Teddy/Roosevelt',90,112,37.3,16),('May 26 1998','Discord','Teddy/Roosevelt',90,112,37.3,17),('May 26 1998','Discord','Teddy/Roosevelt',90,112,37.3,18),('May 25 1998','Discord','Teddy/Roosevelt',60,70.88,23.27,19),('May 26 1998','Discord','Teddy/Roosevelt',90,112,37.3,20),('May 25 1998','Discord','Teddy/Roosevelt',60,70.88,23.27,21),('May 26 1998','Discord','Teddy/Roosevelt',90,112,37.3,22),('May 25 1998','Tyler','Teddy/Roosevelt',60,70.88,23.27,23),('May 26 1998','Longview','Teddy/Roosevelt',90,112,37.3,24),('June 26 1998','Ashdown','miniFE',90,112,37.3,25),('Nov 26 1998','Purple','miniFE',90,112,37.3,26),('Nov 26 1998','Purple','miniFE',90,112,37.3,27),('Nov 26 1998','Purple','miniFE',90,112,37.3,28),('Nov 26 1998','Purple','miniFE',90,112,37.3,29),('Nov 26 1998','Purple','miniFE',90,112,37.3,30),('Nov 26 1998','Purple','miniFE',90,112,37.3,31),('','','',NULL,32,NULL,32);
/*!40000 ALTER TABLE `my_copy_delete_this` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2012-04-10 20:45:23
