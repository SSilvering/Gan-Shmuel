--
-- Database: `Weight`
--

CREATE DATABASE IF NOT EXISTS `weight`;

-- --------------------------------------------------------

--
-- Table structure for table `containers-registered`
--

USE weight;


CREATE TABLE IF NOT EXISTS `containers_registered` (
  `container_id` varchar(15) NOT NULL,
  `weight` int(12) DEFAULT NULL,
  `unit` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`container_id`)
) ENGINE=MyISAM AUTO_INCREMENT=10001 ;

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE IF NOT EXISTS `transactions` (
  `id` int(12) NOT NULL AUTO_INCREMENT,
  `datetime` datetime DEFAULT NULL,
  `direction` varchar(10) DEFAULT NULL,
  `truck` varchar(50) DEFAULT NULL,
  `containers` varchar(10000) DEFAULT NULL,
  `bruto` int(12) DEFAULT NULL,
  `truckTara` int(12) DEFAULT NULL,
  --   "neto": <int> or "na" // na if some of containers unknown
  `neto` int(12) DEFAULT NULL,
  `produce` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=10001 ;

show tables;

describe containers_registered;
describe transactions;

-- -----------------------------------------------------------------------------------------
CREATE DATABASE  IF NOT EXISTS `weight_testing_db` /* Blue's db! */;
USE `weight_testing_db`;
-- MySQL dump 10.13  Distrib 5.7.25, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: db
-- ------------------------------------------------------
-- Server version	8.0.15


DROP TABLE IF EXISTS `containers`;
CREATE TABLE `containers` (
  `id` varchar(45) NOT NULL,
  `weight` float,
  `unit` enum('kg','lbs') NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `products`;
CREATE TABLE `products` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_name` varchar(45) NOT NULL,
  `rate` int(11) NOT NULL,
  `scope` varchar(45) NOT NULL DEFAULT 'ALL',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `providers`;
CREATE TABLE `providers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `providername` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `trucks`;
CREATE TABLE `trucks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `truckid` varchar(45) NOT NULL,
  `providerid` int(11) DEFAULT NULL,
  `weight` float DEFAULT NULL,
  `unit` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `sessions`;
CREATE TABLE `sessions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `direction` enum('in','out','none') DEFAULT NULL,
  `f` bool DEFAULT NULL,
  `date` varchar(45) DEFAULT NULL,
  `bruto` float DEFAULT NULL,
  `neto` float DEFAULT NULL,
  `trucks_id` int(11) DEFAULT NULL,
  `products_id` int(11) DEFAULT NULL,
  `containers` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `trucks` (`id`, `truckid`) VALUES (1, 'none');

INSERT INTO providers (providername) VALUES ('Tapuzina');
INSERT INTO providers (providername) VALUES ('Herut');
INSERT INTO providers (providername) VALUES ('Mishmeret');
INSERT INTO providers (providername) VALUES ('KfarHess');

INSERT INTO containers (id,weight,unit) VALUES ('K-8263',666,'lbs');
INSERT INTO containers (id,weight,unit) VALUES ('K-7854',854,'lbs');
INSERT INTO containers (id,weight,unit) VALUES ('K-6523',741,'kg');
INSERT INTO containers (id,weight,unit) VALUES ('K-2369',120,'kg');
INSERT INTO containers (id,weight,unit) VALUES ('K-7845',999,'lbs');
INSERT INTO containers (id,weight,unit) VALUES ('K-7847',NULL,'lbs');

INSERT INTO products (product_name,rate,scope) VALUES ('Blood',122,'ALL');
INSERT INTO products (product_name,rate,scope) VALUES ('Mandarin',103,'ALL');
INSERT INTO products (product_name,rate,scope) VALUES ('Navel',97,'ALL');
INSERT INTO products (product_name,rate,scope) VALUES ('Blood',102,'1');
INSERT INTO products (product_name,rate,scope) VALUES ('Clementine',100,'ALL');
INSERT INTO products (product_name,rate,scope) VALUES ('Tangerine',80,'ALL');
INSERT INTO products (product_name,rate,scope) VALUES ('Clementine',90,'2');

INSERT INTO trucks (truckid,providerid,weight,unit) VALUES ('77777',2,666,'lbs');
INSERT INTO trucks (truckid,providerid,weight,unit) VALUES ('66666',2,120,'kg');
INSERT INTO trucks (truckid,providerid,weight,unit) VALUES ('99888',1,999,'lbs');
INSERT INTO trucks (truckid,providerid,weight,unit) VALUES ('66321',3,741,'kg');
INSERT INTO trucks (truckid,providerid,weight,unit) VALUES ('12365',4,854,'lbs');

INSERT INTO sessions (direction, f, date, bruto, neto, trucks_id, products_id, containers) VALUES ('in', 1, '20181218181512', 999, 800, 77777, 2, 'K-7845');
INSERT INTO sessions (direction, f, date, bruto, neto, trucks_id, products_id, containers) VALUES ('in', 1, '20161218181512', 120, 100, 99888, 1, 'K-7845');
INSERT INTO sessions (direction, f, date, bruto, neto, trucks_id, products_id, containers) VALUES ('out', 1, '20170920102017', 741, 650, 12365, 3, 'K-7845');



--
-- Dumping data for table `test`
--

-- INSERT INTO `test` (`id`, `aa`) VALUES
-- (1, 'aaaa'),
