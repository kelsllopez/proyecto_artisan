-- MySQL dump 10.13  Distrib 8.0.26, for Win64 (x86_64)
--
-- Host: localhost    Database: artisan
-- ------------------------------------------------------
-- Server version	8.0.26

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

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=157 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add insumo',7,'add_insumo'),(26,'Can change insumo',7,'change_insumo'),(27,'Can delete insumo',7,'delete_insumo'),(28,'Can view insumo',7,'view_insumo'),(29,'Puede ver los insumos',7,'insumo_listar'),(30,'Puede crear un insumo',7,'insumo_crear'),(31,'Puede eliminar un insumo',7,'insumo_eliminar'),(32,'Puede actualizar un insumo',7,'insumo_actualizar'),(33,'Can add insumo directo de producción',8,'add_insumodirectoproducto'),(34,'Can change insumo directo de producción',8,'change_insumodirectoproducto'),(35,'Can delete insumo directo de producción',8,'delete_insumodirectoproducto'),(36,'Can view insumo directo de producción',8,'view_insumodirectoproducto'),(37,'Can add rama',9,'add_rama'),(38,'Can change rama',9,'change_rama'),(39,'Can delete rama',9,'delete_rama'),(40,'Can view rama',9,'view_rama'),(41,'Can add producto',10,'add_producto'),(42,'Can change producto',10,'change_producto'),(43,'Can delete producto',10,'delete_producto'),(44,'Can view producto',10,'view_producto'),(45,'Can add bodega',11,'add_bodega'),(46,'Can change bodega',11,'change_bodega'),(47,'Can delete bodega',11,'delete_bodega'),(48,'Can view bodega',11,'view_bodega'),(49,'Can add inventario Producto',12,'add_inventarioproducto'),(50,'Can change inventario Producto',12,'change_inventarioproducto'),(51,'Can delete inventario Producto',12,'delete_inventarioproducto'),(52,'Can view inventario Producto',12,'view_inventarioproducto'),(53,'Can add inventario Insumo',13,'add_inventarioinsumo'),(54,'Can change inventario Insumo',13,'change_inventarioinsumo'),(55,'Can delete inventario Insumo',13,'delete_inventarioinsumo'),(56,'Can view inventario Insumo',13,'view_inventarioinsumo'),(57,'Can add proovedor',14,'add_proveedor'),(58,'Can change proovedor',14,'change_proveedor'),(59,'Can delete proovedor',14,'delete_proveedor'),(60,'Can view proovedor',14,'view_proveedor'),(61,'Puede ver el listado de los proveedores',14,'listar'),(62,'Puede crear un proveedor',14,'crear'),(63,'Permite eliminar un proveedor',14,'eliminar'),(64,'Permite actualizar un proveedor',14,'actualizar'),(65,'Permite ver el detalle de un proveedor',14,'detalle'),(66,'Can add Asociación Proveedor Insumo',15,'add_proveedorinsumo'),(67,'Can change Asociación Proveedor Insumo',15,'change_proveedorinsumo'),(68,'Can delete Asociación Proveedor Insumo',15,'delete_proveedorinsumo'),(69,'Can view Asociación Proveedor Insumo',15,'view_proveedorinsumo'),(70,'Can add cliente',16,'add_cliente'),(71,'Can change cliente',16,'change_cliente'),(72,'Can delete cliente',16,'delete_cliente'),(73,'Can view cliente',16,'view_cliente'),(74,'Can add Producto - Cliente',17,'add_clienteproducto'),(75,'Can change Producto - Cliente',17,'change_clienteproducto'),(76,'Can delete Producto - Cliente',17,'delete_clienteproducto'),(77,'Can view Producto - Cliente',17,'view_clienteproducto'),(78,'Can add local',18,'add_clientelocal'),(79,'Can change local',18,'change_clientelocal'),(80,'Can delete local',18,'delete_clientelocal'),(81,'Can view local',18,'view_clientelocal'),(82,'Puede ver las ordenes de compra',19,'listar'),(83,'Puede crear una orden de compra',19,'crear'),(84,'Permite generar el pdf de una orden de compra',19,'pdf'),(85,'Permite recepcionar una orden de compra',19,'recepcionar'),(86,'Permite rechazar una orden de compra',19,'rechazar'),(87,'Permite validar una orden de compra',19,'validar'),(88,'Permite eliminar una orden de compra',19,'eliminar'),(89,'Permite pagar una orden',19,'pagar'),(90,'Permite eliminar archivos asociados a las ordenes de compra',19,'eliminararchivo'),(91,'Permite ver los archivos adjuntos',19,'verarchivo'),(92,'Can add Registro',20,'add_registro'),(93,'Can change Registro',20,'change_registro'),(94,'Can delete Registro',20,'delete_registro'),(95,'Can view Registro',20,'view_registro'),(96,'Can add orden de compra insumo',21,'add_ordendecomprainsumo'),(97,'Can change orden de compra insumo',21,'change_ordendecomprainsumo'),(98,'Can delete orden de compra insumo',21,'delete_ordendecomprainsumo'),(99,'Can view orden de compra insumo',21,'view_ordendecomprainsumo'),(100,'Can add archivo',22,'add_archivo'),(101,'Can change archivo',22,'change_archivo'),(102,'Can delete archivo',22,'delete_archivo'),(103,'Can view archivo',22,'view_archivo'),(104,'Puede ver el listado de las bodegas',11,'listar'),(105,'Puede crear una bodega',11,'crear'),(106,'Permite eliminar una bodega',11,'eliminar'),(107,'Permite actualizar una bodega',11,'actualizar'),(108,'Can add group object permission',23,'add_groupobjectpermission'),(109,'Can change group object permission',23,'change_groupobjectpermission'),(110,'Can delete group object permission',23,'delete_groupobjectpermission'),(111,'Can view group object permission',23,'view_groupobjectpermission'),(112,'Can add user object permission',24,'add_userobjectpermission'),(113,'Can change user object permission',24,'change_userobjectpermission'),(114,'Can delete user object permission',24,'delete_userobjectpermission'),(115,'Can view user object permission',24,'view_userobjectpermission'),(119,'Inventario Insumos - Santiago',11,'inventarioi_santiago'),(120,'Inventario Productos - Santiago',11,'inventariop_santiago'),(121,'Puede ver el listado de los productos',12,'listar'),(122,'Permite actualizar un producto',12,'actualizar'),(123,'Puede ver el listado de los insumos',13,'listar'),(124,'Permite actualizar un insumo',13,'actualizar'),(125,'Puede ver el listado de las bodegas',11,'bodega.listar'),(126,'Puede crear una bodega',11,'bodega.crear'),(127,'Permite eliminar una bodega',11,'bodega.eliminar'),(128,'Permite actualizar una bodega',11,'bodega.actualizar'),(129,'Puede ver el listado de los productos',12,'inventariop.listar'),(130,'Permite actualizar un producto',12,'inventariop.actualizar'),(131,'Puede ver el listado de los insumos',13,'inventarioi.listar'),(132,'Permite actualizar un insumo',13,'inventarioi.actualizar'),(133,'Inventario Insumos - San Felipe',11,'inventarioi_san-felipe'),(134,'Inventario Productos - San Felipe',11,'inventariop_san-felipe'),(135,'Inventario Insumos - Valdivia',11,'inventarioi_valdivia'),(136,'Inventario Productos - Valdivia',11,'inventariop_valdivia'),(138,'Inventario Insumos - Valdiviad',11,'inventarioi_valdiviad'),(139,'Inventario Productos - Valdiviad',11,'inventariop_valdiviad'),(145,'Puede ver el listado de los clientes',16,'cliente.listar'),(146,'Puede crear un cliente',16,'cliente.crear'),(147,'Permite eliminar una cliente',16,'cliente.eliminar'),(148,'Permite actualizar un cliente',16,'cliente.actualizar'),(149,'Puede ver el listado de los locales',18,'local.listar'),(150,'Puede crear un local',18,'local.crear'),(151,'Permite eliminar un local',18,'local.eliminar'),(152,'Permite actualizar un local',18,'local.actualizar'),(153,'Permite ver el detalle de un cliente',16,'cliente.detalle'),(154,'Permite ver el detalle de un local',18,'local.detalle'),(155,'Inventario Insumos - Curico',11,'inventarioi_curico'),(156,'Inventario Productos - Curico',11,'inventariop_curico');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$260000$6IKiXI0N4cpm5gWnBs5Q8p$BKy+PfroHAlCTuCkD8oLXeQLfvvuJHHirHZINJfLpvM=','2021-08-25 13:53:38.721914',1,'seba','Sebastián','Valenzuela','seba.valengo@gmail.com',1,1,'2021-08-23 10:06:09.000000'),(2,'!LjuHx7QUbeKDmEAWFYD1hgTjV2N854ZGBv1OqR26',NULL,0,'AnonymousUser','','','',0,1,'2021-08-24 09:48:42.675592'),(3,'pbkdf2_sha256$260000$EaeGijr1jDPRFCWCtvQLwJ$WI6G9EYZ1GT4xk3Nb2AWhlOrEHyGpiE7qr6fEifL6rA=','2021-08-25 11:31:04.000000',0,'prueba','','','',0,1,'2021-08-24 11:03:06.000000'),(4,'pbkdf2_sha256$260000$cx8B5X92cvYu2qUV7hxl8q$OYGaTPkE1Rtqelm2Ig7O1Qz8+55GZqTTuzsuCjn7qmU=',NULL,1,'hvigil','Hernan','Vigil','hvigil@quesosartisan.cl',1,1,'2021-08-25 13:51:34.000000'),(5,'pbkdf2_sha256$260000$bRWyysSEJmryQlIextipf6$OyLADzB4VKNrrI+7EW3x4zClM5aDp5SnDYXpc54LvS0=','2021-08-25 13:58:05.000000',1,'hernan','Hernan','Vigil','',1,1,'2021-08-25 13:57:32.000000');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
INSERT INTO `auth_user_user_permissions` VALUES (8,3,105),(12,3,106),(11,3,107),(4,3,119),(1,3,123),(6,3,124),(7,3,125),(9,3,126),(13,3,127),(10,3,128),(3,3,131),(5,3,132),(14,3,145),(15,3,146),(17,3,147),(16,3,148),(19,3,149),(22,3,150),(23,3,151),(20,3,152),(18,3,153),(21,3,154),(24,5,155),(25,5,156);
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clientes_cliente`
--

DROP TABLE IF EXISTS `clientes_cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clientes_cliente` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `tipo` varchar(255) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `razon_social` varchar(255) NOT NULL,
  `rut` varchar(50) NOT NULL,
  `giro` varchar(100) NOT NULL,
  `telefono` varchar(255) DEFAULT NULL,
  `region` varchar(255) DEFAULT NULL,
  `comuna` varchar(255) DEFAULT NULL,
  `direccion` varchar(255) NOT NULL,
  `contacto` varchar(255) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `celular` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes_cliente`
--

LOCK TABLES `clientes_cliente` WRITE;
/*!40000 ALTER TABLE `clientes_cliente` DISABLE KEYS */;
INSERT INTO `clientes_cliente` VALUES (1,'HORECA','Hotel Trivago','Trivago','1230123-k','Estafar Gente','+56984902256','Tarapacá','Camiña','Manquehue sur 1380','Loco James','loco.james@gmail.com',NULL,'2021-08-24 16:11:56.994515','2021-08-24 16:58:12.304869'),(3,'Supermercado','Montserratd','Montserrat y asociados','2394238-k','Supermercado','3155224','Metropolitana','La Cisterna','Franklin 123','Montse',NULL,NULL,'2021-08-25 09:25:15.841720','2021-08-25 12:08:37.271716');
/*!40000 ALTER TABLE `clientes_cliente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clientes_clientelocal`
--

DROP TABLE IF EXISTS `clientes_clientelocal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clientes_clientelocal` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `local` varchar(255) NOT NULL,
  `telefono` varchar(255) NOT NULL,
  `region` varchar(255) DEFAULT NULL,
  `comuna` varchar(255) DEFAULT NULL,
  `direccion` varchar(255) NOT NULL,
  `contacto` varchar(255) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `celular` varchar(255) DEFAULT NULL,
  `id_comercio_electronico` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `cliente_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `clientes_clientelocal_cliente_id_54e0f87b_fk_clientes_cliente_id` (`cliente_id`),
  CONSTRAINT `clientes_clientelocal_cliente_id_54e0f87b_fk_clientes_cliente_id` FOREIGN KEY (`cliente_id`) REFERENCES `clientes_cliente` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes_clientelocal`
--

LOCK TABLES `clientes_clientelocal` WRITE;
/*!40000 ALTER TABLE `clientes_clientelocal` DISABLE KEYS */;
INSERT INTO `clientes_clientelocal` VALUES (1,'Hotel Trivago Las Condes','3155224','Metropolitana','Cerrillos','Manquehue sur 1380','Fernando Gonzalez','fena@gmail.com',NULL,NULL,'2021-08-25 08:53:22.725187','2021-08-25 08:53:22.725187',1),(2,'Barrio Bellavista','3121312','Metropolitana','Recoleta','Constitución 53 Patio Bellavista','Ignacio Alfaro','ignacio.alfaro@gmail.com',NULL,NULL,'2021-08-25 09:05:12.735616','2021-08-25 09:23:21.414141',1),(5,'Barrio Bellavista','3155224','Tarapacá','Camiña','Manquehue sur 1380','Rodrigo Gallardo','rgallardo@explora.com',NULL,NULL,'2021-08-25 10:44:19.426602','2021-08-25 10:44:19.426602',3),(6,'Plaza Italia','3155224','Metropolitana','La Cisterna','Avenida Lavin 1231','Ernesto Lavin',NULL,NULL,NULL,'2021-08-25 12:15:15.516581','2021-08-25 12:47:49.577652',3);
/*!40000 ALTER TABLE `clientes_clientelocal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clientes_clienteproducto`
--

DROP TABLE IF EXISTS `clientes_clienteproducto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clientes_clienteproducto` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `precio` double NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `cliente_id` bigint NOT NULL,
  `producto_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `clientes_clienteprod_cliente_id_527534e7_fk_clientes_` (`cliente_id`),
  KEY `clientes_clienteprod_producto_id_98a6114f_fk_nucleo_pr` (`producto_id`),
  CONSTRAINT `clientes_clienteprod_cliente_id_527534e7_fk_clientes_` FOREIGN KEY (`cliente_id`) REFERENCES `clientes_cliente` (`id`),
  CONSTRAINT `clientes_clienteprod_producto_id_98a6114f_fk_nucleo_pr` FOREIGN KEY (`producto_id`) REFERENCES `nucleo_producto` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes_clienteproducto`
--

LOCK TABLES `clientes_clienteproducto` WRITE;
/*!40000 ALTER TABLE `clientes_clienteproducto` DISABLE KEYS */;
/*!40000 ALTER TABLE `clientes_clienteproducto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=122 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2021-08-23 10:06:47.083958','1','SANTIAGO',1,'[{\"added\": {}}]',11,1),(2,'2021-08-23 10:06:50.198469','2','VALDIVIA',1,'[{\"added\": {}}]',11,1),(3,'2021-08-23 10:06:53.716713','3','SAN FELIPE',1,'[{\"added\": {}}]',11,1),(4,'2021-08-23 11:10:49.635029','1','Proveedor Ingredion Chile S.A.',1,'El proveedor Ingredion Chile S.A. ha sido creado por el usuario  ',14,1),(5,'2021-08-23 11:11:45.876118','1','Orden de compra 1',1,'La orden de compra 1 ha sido solicitada el usuario  ',19,1),(6,'2021-08-23 11:11:51.237863','1','Orden de compra 1',2,'La orden de compra 1 ha sido Validada por el usuario  ',19,1),(7,'2021-08-23 11:11:57.413928','1','Orden de compra 1',2,'La orden de compra 1 ha sido Recepcionada por el usuario  ',19,1),(8,'2021-08-23 11:58:07.330858','2','Orden de compra 2',1,'La orden de compra 2 ha sido solicitada el usuario  ',19,1),(9,'2021-08-23 11:58:10.418548','2','Orden de compra 2',2,'La orden de compra 2 ha sido Validada por el usuario  ',19,1),(10,'2021-08-23 11:58:16.726956','2','Orden de compra 2',2,'La orden de compra 2 ha sido Recepcionada por el usuario  ',19,1),(11,'2021-08-23 13:04:35.377409','1','Leche',2,'[{\"changed\": {\"fields\": [\"Cantidad\"]}}]',13,1),(12,'2021-08-23 17:08:50.514068','2','Orden de compra 2',2,'La orden de compra 2 ha sido Validada por el usuario  ',19,1),(13,'2021-08-24 09:16:45.131141','3','Orden de compra 3',1,'La orden de compra 3 ha sido solicitada el usuario  ',19,1),(14,'2021-08-24 09:16:49.901773','3','Orden de compra 3',2,'La orden de compra 3 ha sido Validada por el usuario  ',19,1),(15,'2021-08-24 09:16:57.371991','3','Orden de compra 3',2,'La orden de compra 3 ha sido Recepcionada por el usuario  ',19,1),(16,'2021-08-24 09:17:39.879659','1','Orden de compra 1',2,'La orden de compra 1 ha sido Validada por el usuario  ',19,1),(17,'2021-08-24 09:19:38.990663','1','Orden de compra 1',2,'La orden de compra 1 ha sido Recepcionada por el usuario  ',19,1),(18,'2021-08-24 09:22:17.479262','1','Orden de compra 1',2,'La orden de compra 1 ha sido Validada por el usuario  ',19,1),(19,'2021-08-24 09:23:42.485793','1','Orden de compra 1',2,'La orden de compra 1 ha sido Recepcionada por el usuario  ',19,1),(20,'2021-08-24 09:23:52.993255','1','Orden de compra 1',2,'La orden de compra 1 ha sido Validada por el usuario  ',19,1),(21,'2021-08-24 09:24:38.247659','1','Orden de compra 1',2,'La orden de compra 1 ha sido Semi-Recepcionada por el usuario  ',19,1),(22,'2021-08-24 09:31:40.118353','1','Orden de compra 1',2,'La orden de compra 1 ha sido Recepcionada por el usuario  ',19,1),(23,'2021-08-24 10:32:58.194420','2','SAN FELIPE',1,'[{\"added\": {}}]',11,1),(24,'2021-08-24 10:34:53.245922','2','SAN FELIPE',3,'',11,1),(25,'2021-08-24 10:38:28.225428','3','SAN FELIPE',1,'[{\"added\": {}}]',11,1),(26,'2021-08-24 10:39:05.021570','3','SAN FELIPE',3,'',11,1),(27,'2021-08-24 11:03:06.217395','3',' ',1,'[{\"added\": {}}]',4,1),(28,'2021-08-24 11:03:38.319864','3',' ',2,'[{\"changed\": {\"fields\": [\"User permissions\"]}}]',4,1),(29,'2021-08-24 11:04:12.589653','2','Orden de compra 2',2,'La orden de compra 2 ha sido Inicial por el usuario  ',19,1),(30,'2021-08-24 11:04:30.453699','4','Orden de compra 4',1,'La orden de compra 4 ha sido solicitada el usuario  ',19,1),(31,'2021-08-24 11:04:34.436260','4','Orden de compra 4',2,'La orden de compra 4 ha sido Validada por el usuario  ',19,1),(32,'2021-08-24 11:04:40.635874','4','Orden de compra 4',2,'La orden de compra 4 ha sido Recepcionada por el usuario  ',19,1),(33,'2021-08-24 11:20:07.090781','3',' ',2,'[{\"changed\": {\"fields\": [\"User permissions\"]}}]',4,1),(34,'2021-08-24 11:36:03.091650','3',' ',2,'[{\"changed\": {\"fields\": [\"User permissions\"]}}]',4,1),(35,'2021-08-24 11:39:02.859586','3',' ',2,'[{\"changed\": {\"fields\": [\"User permissions\"]}}]',4,1),(36,'2021-08-24 11:40:20.221416','3',' ',2,'[{\"changed\": {\"fields\": [\"User permissions\"]}}]',4,1),(37,'2021-08-24 11:46:14.268969','3',' ',2,'[{\"changed\": {\"fields\": [\"User permissions\"]}}]',4,1),(38,'2021-08-24 12:45:36.112103','5','Orden de compra 5',1,'La orden de compra 5 ha sido solicitada el usuario  ',19,1),(39,'2021-08-24 12:45:40.717201','5','Orden de compra 5',2,'La orden de compra 5 ha sido Validada por el usuario  ',19,1),(40,'2021-08-24 12:45:51.925513','5','Orden de compra 5',2,'La orden de compra 5 ha sido Recepcionada por el usuario  ',19,1),(41,'2021-08-24 15:06:49.170587','5','Inventario Insumo Leche - San Felipe',2,'Se ha actualizado el inventario de Leche en San Felipe de manera MANUAL por el usuario  ',13,1),(42,'2021-08-24 15:07:55.659650','1','Sebastián Valenzuela',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\"]}}]',4,1),(43,'2021-08-24 15:08:13.212002','5','Inventario Insumo Leche - San Felipe',2,'Se ha actualizado el inventario de Leche en San Felipe de manera MANUAL por el usuario Sebastián Valenzuela',13,1),(44,'2021-08-24 15:13:24.291298','6','Bodega Valdivia',1,'El usuario Sebastián Valenzuela ha creado la bodega Valdivia',11,1),(45,'2021-08-24 15:20:33.913574','6','Bodega Valdiviad',2,'El usuario Sebastián Valenzuela ha modificado la bodega Valdiviad',11,1),(46,'2021-08-24 15:23:56.159288','6','Bodega ValdiviaD',2,'El usuario Sebastián Valenzuela ha modificado la bodega ValdiviaD',11,1),(47,'2021-08-24 15:23:59.164382','6','Bodega Valdivia',2,'El usuario Sebastián Valenzuela ha modificado la bodega Valdivia',11,1),(48,'2021-08-24 15:32:10.059246','7','Bodega Chicureo',1,'El usuario Sebastián Valenzuela ha creado la bodega Chicureo',11,1),(49,'2021-08-24 15:32:24.770434','7','Bodega Atacama',2,'El usuario Sebastián Valenzuela ha modificado la bodega Atacama',11,1),(50,'2021-08-24 15:34:12.738114','7','Bodega Atacamax',2,'El usuario Sebastián Valenzuela ha modificado la bodega Atacamax',11,1),(51,'2021-08-24 15:35:39.402658','7','Bodega Atacama',2,'El usuario Sebastián Valenzuela ha modificado la bodega Atacama',11,1),(52,'2021-08-24 15:37:44.757097','7','Bodega Chicureo',2,'El usuario Sebastián Valenzuela ha modificado el nombre de la bodega Atacama a Chicureo',11,1),(53,'2021-08-24 15:38:35.131292','3',' ',2,'[{\"changed\": {\"fields\": [\"User permissions\"]}}]',4,1),(54,'2021-08-24 15:46:54.230432','3',' ',2,'[{\"changed\": {\"fields\": [\"User permissions\"]}}]',4,1),(55,'2021-08-24 15:47:23.244989','8','Bodega Los Andes',1,'El usuario prueba ha creado la bodega Los Andes',11,3),(56,'2021-08-24 15:48:58.244281','3',' ',2,'[{\"changed\": {\"fields\": [\"User permissions\"]}}]',4,1),(57,'2021-08-24 15:49:31.980537','8','Bodega Andes',2,'El usuario prueba ha modificado el nombre de la bodega Los Andes a Andes',11,3),(58,'2021-08-24 15:50:48.898355','3',' ',2,'[{\"changed\": {\"fields\": [\"User permissions\"]}}]',4,1),(59,'2021-08-24 15:51:33.498278','8','Bodega Andes',3,'El usuario Sebastián Valenzuela ha eliminado la bodega Andes',11,1),(60,'2021-08-24 15:51:37.347152','7','Bodega Chicureo',3,'El usuario Sebastián Valenzuela ha eliminado la bodega Chicureo',11,1),(61,'2021-08-24 16:11:57.005007','1','Hotel Trivago',1,'[{\"added\": {}}]',16,1),(62,'2021-08-25 08:51:00.418173','3','Inventario Insumo Leche - Santiago',2,'Se ha actualizado el inventario de Leche en Santiago de manera MANUAL por el usuario Sebastián Valenzuela',13,1),(63,'2021-08-25 11:31:51.842907','3',' ',2,'[{\"changed\": {\"fields\": [\"User permissions\"]}}]',4,1),(64,'2021-08-25 11:32:31.643703','3',' ',2,'[{\"changed\": {\"fields\": [\"User permissions\"]}}]',4,1),(65,'2021-08-25 11:33:47.694788','3',' ',2,'[{\"changed\": {\"fields\": [\"User permissions\"]}}]',4,1),(66,'2021-08-25 11:34:08.718302','3',' ',2,'[{\"changed\": {\"fields\": [\"User permissions\"]}}]',4,1),(67,'2021-08-25 11:37:18.626051','3',' ',2,'[{\"changed\": {\"fields\": [\"User permissions\"]}}]',4,1),(68,'2021-08-25 11:38:14.249233','3',' ',2,'[{\"changed\": {\"fields\": [\"User permissions\"]}}]',4,1),(69,'2021-08-25 11:38:29.034514','3',' ',2,'[{\"changed\": {\"fields\": [\"User permissions\"]}}]',4,1),(70,'2021-08-25 12:08:37.126747','3','Cliente Montserratd',2,'Se ha actualizado el cliente Montserratd - 2394238-k por el usuario Sebastián Valenzuela',16,1),(71,'2021-08-25 12:09:54.913330','5','Cliente Leche',1,'Se ha creado el cliente Leche - 19522999 por el usuario Sebastián Valenzuela',16,1),(72,'2021-08-25 12:10:01.974681','5','Cliente Leched',2,'Se ha actualizado el cliente Leched - 19522999 por el usuario Sebastián Valenzuela',16,1),(73,'2021-08-25 12:10:04.173033','5','Cliente Leched',2,'Se ha borrado el cliente Leched - 19522999 por el usuario Sebastián Valenzuela',16,1),(74,'2021-08-25 12:15:15.685886','6','Cliente Montserratd - Barrio Bellavista',1,'Se ha creado el local Barrio Bellavista para el cliente Montserratd por el usuario Sebastián Valenzuela',18,1),(75,'2021-08-25 12:47:25.673287','6','Cliente Montserratd - Plaza Italia',2,'Se ha creado actualizado el local Plaza Italia para el cliente Montserratd por el usuario Sebastián Valenzuela',18,1),(76,'2021-08-25 12:47:39.844856','6','Cliente Montserratd - Plaza Italia',2,'Se ha creado actualizado el local Plaza Italia para el cliente Montserratd por el usuario Sebastián Valenzuela',18,1),(77,'2021-08-25 12:47:49.403939','6','Cliente Montserratd - Plaza Italia',2,'Se ha creado actualizado el local Plaza Italia para el cliente Montserratd por el usuario Sebastián Valenzuela',18,1),(78,'2021-08-25 13:51:34.757995','4',' ',1,'[{\"added\": {}}]',4,1),(79,'2021-08-25 13:51:46.403507','4','Hernan Vigil',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Email address\", \"Staff status\", \"Superuser status\"]}}]',4,1),(80,'2021-08-25 13:57:32.272215','5',' ',1,'[{\"added\": {}}]',4,1),(81,'2021-08-25 13:57:43.583826','5',' ',2,'[{\"changed\": {\"fields\": [\"Staff status\", \"Superuser status\"]}}]',4,1),(82,'2021-08-25 13:58:55.857974','9','Bodega Curico',1,'El usuario hernan ha creado la bodega Curico',11,5),(83,'2021-08-25 14:00:12.320050','5',' ',2,'[{\"changed\": {\"fields\": [\"User permissions\"]}}]',4,5),(84,'2021-08-25 14:01:28.742704','5','Inventario Insumo Leche - San Felipe',2,'Se ha actualizado el inventario de Leche en San Felipe de manera MANUAL por el usuario  ',13,5),(85,'2021-08-25 14:01:30.020342','5','Inventario Insumo Leche - San Felipe',2,'Se ha actualizado el inventario de Leche en San Felipe de manera MANUAL por el usuario  ',13,5),(86,'2021-08-25 14:01:58.111796','5','Inventario Insumo Leche - San Felipe',2,'Se ha actualizado el inventario de Leche en San Felipe de manera MANUAL por el usuario  ',13,5),(87,'2021-08-25 14:25:47.875290','2','Proveedor Serviform',1,'El proveedor Serviform ha sido creado por el usuario  ',14,5),(88,'2021-08-25 17:41:35.038899','5','Hernan Vigil',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\"]}}]',4,1),(89,'2021-08-26 10:12:01.952545','6','Orden de compra 6',1,'La orden de compra 6 ha sido solicitada el usuario Sebastián Valenzuela',19,1),(90,'2021-08-26 10:13:10.182818','6','Orden de compra 7',2,'La orden de compra 7 ha sido Validada por el usuario Sebastián Valenzuela',19,1),(91,'2021-08-26 10:13:43.760113','6','Orden de compra 7',2,'La orden de compra 7 ha sido Inicial por el usuario Sebastián Valenzuela',19,1),(92,'2021-08-26 10:14:50.242288','6','Orden de compra 7',2,'La orden de compra 7 ha sido Validada por el usuario Sebastián Valenzuela',19,1),(93,'2021-08-26 11:02:52.313267','7','Orden de compra 8',1,'La orden de compra 8 ha sido solicitada el usuario Sebastián Valenzuela',19,1),(94,'2021-08-26 11:02:59.183925','7','Orden de compra 8',2,'La orden de compra 8 ha sido Validada por el usuario Sebastián Valenzuela',19,1),(95,'2021-08-26 11:03:07.619737','7','Orden de compra 8',2,'La orden de compra 8 ha sido Inicial por el usuario Sebastián Valenzuela',19,1),(96,'2021-08-27 09:07:20.746705','4','Insumo Etiquetas 50x50',1,'El empleado Sebastián Valenzuela ha agregado el insumo Etiquetas 50x50',7,1),(97,'2021-08-27 09:07:36.376907','4','Insumo Etiquetas 50x50d',2,'El empleado Sebastián Valenzuela ha modificado el insumo Etiquetas 50x50d',7,1),(98,'2021-08-27 09:07:50.886633','4','Insumo Etiquetas 50x50d',1,'El empleado Sebastián Valenzuela ha eliminado el insumo Etiquetas 50x50d',7,1),(99,'2021-08-27 09:15:18.173997','4','Área de negocio: Queso Campo',1,'El empleado Sebastián Valenzuela ha agregado el área de negocio: Queso Campo',9,1),(100,'2021-08-27 09:15:27.549114','4','Área de negocio: Queso CampoD',2,'El empleado Sebastián Valenzuela ha modificado el área de negocio: Queso CampoD',9,1),(101,'2021-08-27 09:15:33.001283','4','Área de negocio: Queso CampoD',3,'El empleado Sebastián Valenzuela ha eliminado el área de negocio: Queso CampoD',9,1),(102,'2021-08-27 09:24:13.888038','16','Producto: Producto Permiso',1,'El empleado Sebastián Valenzuela ha agregado el producto: Producto Permiso',10,1),(103,'2021-08-27 09:27:10.521579','16','Producto: Producto Permisod',2,'El empleado Sebastián Valenzuela ha modificado el producto: Producto Permisod',10,1),(104,'2021-08-27 09:27:48.745664','16','Producto: Producto Permisodd',2,'El empleado Sebastián Valenzuela ha modificado el producto: Producto Permisodd',10,1),(105,'2021-08-27 09:28:05.382131','16','Producto: Producto Permisoddd',2,'El empleado Sebastián Valenzuela ha modificado el producto: Producto Permisoddd',10,1),(106,'2021-08-27 09:30:04.546155','16','Producto: Producto Permisoddd',2,'El empleado Sebastián Valenzuela ha modificado el producto: Producto Permisoddd',10,1),(107,'2021-08-27 09:30:21.315746','17','Producto: Santiago',1,'El empleado Sebastián Valenzuela ha agregado el producto: Santiago',10,1),(108,'2021-08-27 09:31:10.787349','17','Producto: Santiagod',2,'El empleado Sebastián Valenzuela ha modificado el producto: Santiagod',10,1),(109,'2021-08-27 09:31:24.181738','18','Producto: Santiago',1,'El empleado Sebastián Valenzuela ha agregado el producto: Santiago',10,1),(110,'2021-08-27 09:31:49.917969','19','Producto: Santiago',1,'El empleado Sebastián Valenzuela ha agregado el producto: Santiago',10,1),(111,'2021-08-27 09:46:41.841809','20','Producto: Santiago',1,'El empleado Sebastián Valenzuela ha agregado el producto: Santiago',10,1),(112,'2021-08-27 09:47:45.493933','21','Producto: 123',1,'El empleado Sebastián Valenzuela ha agregado el producto: 123',10,1),(113,'2021-08-27 09:49:37.099780','22','Producto: Santiago',1,'El empleado Sebastián Valenzuela ha agregado el producto: Santiago',10,1),(114,'2021-08-27 09:52:21.721155','16','Producto: Producto Permisoddd',3,'El empleado Sebastián Valenzuela ha eliminado el producto: Producto Permisoddd',10,1),(115,'2021-08-27 09:52:28.112143','11','Producto: Santiago',3,'El empleado Sebastián Valenzuela ha eliminado el producto: Santiago',10,1),(116,'2021-08-27 09:53:37.551809','23','Producto: Santiago',1,'El empleado Sebastián Valenzuela ha agregado el producto: Santiago',10,1),(117,'2021-08-27 09:56:20.132362','5','Área de negocio: QUESO CAMPO',1,'El empleado Sebastián Valenzuela ha agregado el área de negocio: QUESO CAMPO',9,1),(118,'2021-08-27 09:56:40.804072','24','Producto: Queso de Chancho',1,'El empleado Sebastián Valenzuela ha agregado el producto: Queso de Chancho',10,1),(119,'2021-08-27 09:57:01.399283','5','Área de negocio: Queso Campo',2,'El empleado Sebastián Valenzuela ha modificado el área de negocio: Queso Campo',9,1),(120,'2021-08-27 12:11:42.673945','21','Producto: 123',3,'El empleado Sebastián Valenzuela ha eliminado el producto: 123',10,1),(121,'2021-08-27 12:11:50.434048','23','Producto: Santiago',3,'El empleado Sebastián Valenzuela ha eliminado el producto: Santiago',10,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(16,'clientes','cliente'),(18,'clientes','clientelocal'),(17,'clientes','clienteproducto'),(5,'contenttypes','contenttype'),(23,'guardian','groupobjectpermission'),(24,'guardian','userobjectpermission'),(11,'inventario','bodega'),(13,'inventario','inventarioinsumo'),(12,'inventario','inventarioproducto'),(7,'nucleo','insumo'),(8,'nucleo','insumodirectoproducto'),(10,'nucleo','producto'),(9,'nucleo','rama'),(22,'ordendecompra','archivo'),(19,'ordendecompra','ordendecompra'),(21,'ordendecompra','ordendecomprainsumo'),(20,'ordendecompra','registro'),(14,'proveedores','proveedor'),(15,'proveedores','proveedorinsumo'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2021-08-23 10:02:53.328845'),(2,'auth','0001_initial','2021-08-23 10:03:31.654435'),(3,'admin','0001_initial','2021-08-23 10:03:37.773212'),(4,'admin','0002_logentry_remove_auto_add','2021-08-23 10:03:37.962224'),(5,'admin','0003_logentry_add_action_flag_choices','2021-08-23 10:03:38.023492'),(6,'contenttypes','0002_remove_content_type_name','2021-08-23 10:03:45.547327'),(7,'auth','0002_alter_permission_name_max_length','2021-08-23 10:03:49.672396'),(8,'auth','0003_alter_user_email_max_length','2021-08-23 10:03:52.186713'),(9,'auth','0004_alter_user_username_opts','2021-08-23 10:03:52.423033'),(10,'auth','0005_alter_user_last_login_null','2021-08-23 10:03:54.735712'),(11,'auth','0006_require_contenttypes_0002','2021-08-23 10:03:54.789793'),(12,'auth','0007_alter_validators_add_error_messages','2021-08-23 10:03:54.881049'),(13,'auth','0008_alter_user_username_max_length','2021-08-23 10:03:58.021286'),(14,'auth','0009_alter_user_last_name_max_length','2021-08-23 10:04:03.877864'),(15,'auth','0010_alter_group_name_max_length','2021-08-23 10:04:07.136081'),(16,'auth','0011_update_proxy_permissions','2021-08-23 10:04:07.310594'),(17,'auth','0012_alter_user_first_name_max_length','2021-08-23 10:04:10.235628'),(18,'nucleo','0001_initial','2021-08-23 10:04:25.329297'),(19,'clientes','0001_initial','2021-08-23 10:04:39.520159'),(20,'inventario','0001_initial','2021-08-23 10:04:58.142399'),(21,'proveedores','0001_initial','2021-08-23 10:05:11.697748'),(22,'ordendecompra','0001_initial','2021-08-23 10:05:47.776368'),(23,'sessions','0001_initial','2021-08-23 10:05:49.658410'),(24,'inventario','0002_auto_20210823_1030','2021-08-23 10:31:14.082036'),(25,'inventario','0003_auto_20210823_1705','2021-08-23 17:05:50.737295'),(26,'guardian','0001_initial','2021-08-24 09:48:39.854586'),(27,'guardian','0002_generic_permissions_index','2021-08-24 09:48:42.067178'),(28,'ordendecompra','0002_alter_ordendecompra_bodega','2021-08-24 10:41:39.789678'),(29,'ordendecompra','0003_auto_20210824_1042','2021-08-24 10:43:00.851785'),(30,'inventario','0004_auto_20210824_1049','2021-08-24 10:49:56.266400'),(31,'inventario','0005_auto_20210824_1134','2021-08-24 11:34:06.843027'),(32,'clientes','0002_auto_20210825_1130','2021-08-25 11:30:43.126609'),(33,'clientes','0003_auto_20210825_1137','2021-08-25 11:37:04.564109'),(34,'nucleo','0002_alter_insumo_unidad','2021-08-25 14:49:07.923511'),(35,'proveedores','0002_auto_20210826_1105','2021-08-26 11:05:27.387415'),(36,'proveedores','0003_alter_proveedorinsumo_lead','2021-08-26 11:06:51.522726'),(37,'nucleo','0003_auto_20210826_1111','2021-08-26 11:11:46.127374'),(38,'nucleo','0004_alter_rama_nombre','2021-08-26 12:22:38.773000');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('2ivu234jddv9vbf8jsz3qxyhevy8et37','.eJxVjMEOwiAQRP-FsyGyXSB69O43kF1YpGogKe2p8d9tkx70Npn3ZlYVaJlLWLpMYUzqqqw6_XZM8SV1B-lJ9dF0bHWeRta7og_a9b0led8O9--gUC_bGgAsnxkHoSwX8OSceGtABkTxPqMRQHIIESC7NICwcShxy4k9OPX5AtbMN8w:1mIxA5:9fki-Ozll2RCUprJcv_WjyjY4DMAb1cVU7BVVR_7QFc','2021-09-08 13:58:05.411686'),('5bswuzuk2n82x6rdijc1hrfqm5c3men6','.eJxVjEEOgjAURO_StWkopYXv0r1naKb9vxY1kFBYGe-uJCx0O--9eamAbS1hq7KEkdVZGXX63SLSQ6Yd8B3TbdZpntZljHpX9EGrvs4sz8vh_h0U1PKte7IxJxt7uCaSgCCUxCTPjjMRsveuMxYDmrazDETh1kAcBmayWb0_Elw5Ug:1mIAaa:w-nO0_04j5f6XM835WG0pmFui-sxPjzpRW1uPWeh7Yo','2021-09-06 10:06:12.562091'),('bv4x3tjqw1m21u59dep4gmaqf8jcffjy','.eJxVjDsOwjAQBe_iGlmLf7CU9DlDtPaucQDZUpxUiLtDpBTQvpl5LzXSupRx7TKPE6uLsurwu0VKD6kb4DvVW9Op1WWeot4UvdOuh8byvO7u30GhXr41SgSQkCWaaCwFcow2eCfMViSjO3owgiEAmoRAyXqTfTqJseDOCOr9AfSEN6M:1mIurp:MNM6FyrlBpMY0McwvlLjAOCVy1rJwN4AURaB9Yl8nNc','2021-09-08 11:31:05.161148'),('jlebt471wgkqjxlee256edfsql12vpz5','.eJxVjEEOgjAURO_StWkopYXv0r1naKb9vxY1kFBYGe-uJCx0O--9eamAbS1hq7KEkdVZGXX63SLSQ6Yd8B3TbdZpntZljHpX9EGrvs4sz8vh_h0U1PKte7IxJxt7uCaSgCCUxCTPjjMRsveuMxYDmrazDETh1kAcBmayWb0_Elw5Ug:1mIx5m:YqgcFp4Ah1Xj7e5DM25kUsXLKTuqIbgANsxHHUBjApI','2021-09-08 13:53:38.779995'),('khgsz3z0tcuvf9fb7xo8h7uat0b2v8np','.eJxVjDsOwjAQBe_iGlmLf7CU9DlDtPaucQDZUpxUiLtDpBTQvpl5LzXSupRx7TKPE6uLsurwu0VKD6kb4DvVW9Op1WWeot4UvdOuh8byvO7u30GhXr41SgSQkCWaaCwFcow2eCfMViSjO3owgiEAmoRAyXqTfTqJseDOCOr9AfSEN6M:1mIXxH:6fl5O-9vL_HuYR59gPphSqww_so15BDTe2KsyT6hxj8','2021-09-07 11:03:11.455769');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `guardian_groupobjectpermission`
--

DROP TABLE IF EXISTS `guardian_groupobjectpermission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `guardian_groupobjectpermission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `object_pk` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `guardian_groupobjectperm_group_id_permission_id_o_3f189f7c_uniq` (`group_id`,`permission_id`,`object_pk`),
  KEY `guardian_groupobject_permission_id_36572738_fk_auth_perm` (`permission_id`),
  KEY `guardian_gr_content_ae6aec_idx` (`content_type_id`,`object_pk`),
  CONSTRAINT `guardian_groupobject_content_type_id_7ade36b8_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `guardian_groupobject_group_id_4bbbfb62_fk_auth_grou` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `guardian_groupobject_permission_id_36572738_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `guardian_groupobjectpermission`
--

LOCK TABLES `guardian_groupobjectpermission` WRITE;
/*!40000 ALTER TABLE `guardian_groupobjectpermission` DISABLE KEYS */;
/*!40000 ALTER TABLE `guardian_groupobjectpermission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `guardian_userobjectpermission`
--

DROP TABLE IF EXISTS `guardian_userobjectpermission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `guardian_userobjectpermission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `object_pk` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `permission_id` int NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `guardian_userobjectpermi_user_id_permission_id_ob_b0b3d2fc_uniq` (`user_id`,`permission_id`,`object_pk`),
  KEY `guardian_userobjectp_permission_id_71807bfc_fk_auth_perm` (`permission_id`),
  KEY `guardian_us_content_179ed2_idx` (`content_type_id`,`object_pk`),
  CONSTRAINT `guardian_userobjectp_content_type_id_2e892405_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `guardian_userobjectp_permission_id_71807bfc_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `guardian_userobjectpermission_user_id_d5c1e964_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `guardian_userobjectpermission`
--

LOCK TABLES `guardian_userobjectpermission` WRITE;
/*!40000 ALTER TABLE `guardian_userobjectpermission` DISABLE KEYS */;
/*!40000 ALTER TABLE `guardian_userobjectpermission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventario_bodega`
--

DROP TABLE IF EXISTS `inventario_bodega`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventario_bodega` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `inventario_bodega_nombre_0dee8fa5_uniq` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventario_bodega`
--

LOCK TABLES `inventario_bodega` WRITE;
/*!40000 ALTER TABLE `inventario_bodega` DISABLE KEYS */;
INSERT INTO `inventario_bodega` VALUES (4,'Santiago','2021-08-24 10:46:35.647642','2021-08-24 10:46:35.647642'),(5,'San Felipe','2021-08-24 12:45:13.386360','2021-08-24 12:45:13.386360'),(6,'Valdivia','2021-08-24 15:13:23.913494','2021-08-24 15:23:58.945264'),(9,'Curico','2021-08-25 13:58:55.409312','2021-08-25 13:58:55.409312');
/*!40000 ALTER TABLE `inventario_bodega` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventario_inventarioinsumo`
--

DROP TABLE IF EXISTS `inventario_inventarioinsumo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventario_inventarioinsumo` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `cantidad` bigint NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `bodega_id` bigint NOT NULL,
  `insumo_id` bigint NOT NULL,
  `estado` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `inventario_inventarioinsumo_bodega_id_insumo_id_8861ccbc_uniq` (`bodega_id`,`insumo_id`),
  KEY `inventario_inventari_insumo_id_23f7b56d_fk_nucleo_in` (`insumo_id`),
  CONSTRAINT `inventario_inventari_bodega_id_292ee580_fk_inventari` FOREIGN KEY (`bodega_id`) REFERENCES `inventario_bodega` (`id`),
  CONSTRAINT `inventario_inventari_insumo_id_23f7b56d_fk_nucleo_in` FOREIGN KEY (`insumo_id`) REFERENCES `nucleo_insumo` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventario_inventarioinsumo`
--

LOCK TABLES `inventario_inventarioinsumo` WRITE;
/*!40000 ALTER TABLE `inventario_inventarioinsumo` DISABLE KEYS */;
INSERT INTO `inventario_inventarioinsumo` VALUES (4,10,'2021-08-24 12:45:47.833848','2021-08-24 12:46:46.833805',5,2,'Peligro');
/*!40000 ALTER TABLE `inventario_inventarioinsumo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventario_inventarioproducto`
--

DROP TABLE IF EXISTS `inventario_inventarioproducto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventario_inventarioproducto` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `cantidad` bigint NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `bodega_id` bigint NOT NULL,
  `producto_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `inventario_inventariopro_bodega_id_producto_id_a8939745_uniq` (`bodega_id`,`producto_id`),
  KEY `inventario_inventari_producto_id_76404bef_fk_nucleo_pr` (`producto_id`),
  CONSTRAINT `inventario_inventari_bodega_id_6ba7a20d_fk_inventari` FOREIGN KEY (`bodega_id`) REFERENCES `inventario_bodega` (`id`),
  CONSTRAINT `inventario_inventari_producto_id_76404bef_fk_nucleo_pr` FOREIGN KEY (`producto_id`) REFERENCES `nucleo_producto` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventario_inventarioproducto`
--

LOCK TABLES `inventario_inventarioproducto` WRITE;
/*!40000 ALTER TABLE `inventario_inventarioproducto` DISABLE KEYS */;
/*!40000 ALTER TABLE `inventario_inventarioproducto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nucleo_insumo`
--

DROP TABLE IF EXISTS `nucleo_insumo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nucleo_insumo` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `unidad` varchar(50) NOT NULL,
  `stock_critico` bigint NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nucleo_insumo`
--

LOCK TABLES `nucleo_insumo` WRITE;
/*!40000 ALTER TABLE `nucleo_insumo` DISABLE KEYS */;
INSERT INTO `nucleo_insumo` VALUES (2,'Botella 1LT','N/A',300,'2021-08-23 11:57:28.629730','2021-08-24 12:44:28.781671'),(3,'Envase Yogurt 0,15','Unidad',1000,'2021-08-25 14:25:06.323199','2021-08-26 11:12:03.485976');
/*!40000 ALTER TABLE `nucleo_insumo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nucleo_insumodirectoproducto`
--

DROP TABLE IF EXISTS `nucleo_insumodirectoproducto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nucleo_insumodirectoproducto` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `cantidad` int NOT NULL,
  `detalle` varchar(255) NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `insumo_id` bigint NOT NULL,
  `producto_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `nucleo_insumodirecto_producto_id_a10036ad_fk_nucleo_pr` (`producto_id`),
  KEY `nucleo_insumodirecto_insumo_id_f737fb29_fk_nucleo_in` (`insumo_id`),
  CONSTRAINT `nucleo_insumodirecto_insumo_id_f737fb29_fk_nucleo_in` FOREIGN KEY (`insumo_id`) REFERENCES `nucleo_insumo` (`id`),
  CONSTRAINT `nucleo_insumodirecto_producto_id_a10036ad_fk_nucleo_pr` FOREIGN KEY (`producto_id`) REFERENCES `nucleo_producto` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nucleo_insumodirectoproducto`
--

LOCK TABLES `nucleo_insumodirectoproducto` WRITE;
/*!40000 ALTER TABLE `nucleo_insumodirectoproducto` DISABLE KEYS */;
INSERT INTO `nucleo_insumodirectoproducto` VALUES (9,123,'123','2021-08-26 16:08:02.918043','2021-08-26 16:08:02.918043',2,12),(10,123,'12332','2021-08-26 16:08:02.962678','2021-08-26 16:08:02.962678',2,12),(16,1,'','2021-08-26 16:21:28.437460','2021-08-26 16:21:28.437460',2,14),(17,3,'','2021-08-26 16:21:28.524241','2021-08-26 16:21:28.524241',3,14),(18,2,'123','2021-08-26 16:26:52.419351','2021-08-26 16:26:52.419351',2,15),(24,1,'250','2021-08-26 17:20:30.114026','2021-08-26 17:20:30.114026',3,13);
/*!40000 ALTER TABLE `nucleo_insumodirectoproducto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nucleo_producto`
--

DROP TABLE IF EXISTS `nucleo_producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nucleo_producto` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `codigo` varchar(255) NOT NULL,
  `presentacion` bigint NOT NULL,
  `unidad` varchar(50) NOT NULL,
  `duracion` int NOT NULL,
  `maduracion` bigint NOT NULL,
  `stock_critico` bigint NOT NULL,
  `id_comercio_net` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `rama_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `nucleo_producto_rama_id_dd0cef14_fk_nucleo_rama_id` (`rama_id`),
  CONSTRAINT `nucleo_producto_rama_id_dd0cef14_fk_nucleo_rama_id` FOREIGN KEY (`rama_id`) REFERENCES `nucleo_rama` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nucleo_producto`
--

LOCK TABLES `nucleo_producto` WRITE;
/*!40000 ALTER TABLE `nucleo_producto` DISABLE KEYS */;
INSERT INTO `nucleo_producto` VALUES (12,'Santiago','QUCA02',123213,'gr',12312,3123,123,NULL,'2021-08-26 16:08:02.825080','2021-08-26 16:08:02.825080',3),(13,'Botellona','QUCA06',15,'gr',151,151,1515,NULL,'2021-08-26 16:19:44.990131','2021-08-26 17:20:30.024563',3),(14,'Santiago','QUCA04',123,'gr',123,123,123,NULL,'2021-08-26 16:21:28.268799','2021-08-26 16:21:28.268799',3),(15,'Santiago Botellita','QUCA05',123123,'cc',123123,123123,123,NULL,'2021-08-26 16:26:52.230447','2021-08-26 16:26:52.230447',3),(17,'Santiagod','QUCA07',12321,'gr',123,123,123,NULL,'2021-08-27 09:30:21.093841','2021-08-27 09:31:10.612492',3),(18,'Santiago','QUCA08',123,'gr',123,123,123,NULL,'2021-08-27 09:31:24.060023','2021-08-27 09:31:24.060023',3),(19,'Santiago','QUCA09',123,'gr',123,123,123,NULL,'2021-08-27 09:31:49.652222','2021-08-27 09:31:49.652222',3),(20,'Santiago','QUCA01',123,'gr',123,123,123,NULL,'2021-08-27 09:46:41.675059','2021-08-27 09:46:41.675059',3),(22,'Santiago','QUCA10',123,'gr',123,123,123,NULL,'2021-08-27 09:49:36.950182','2021-08-27 09:49:36.950182',3),(24,'Queso de Chancho','QUCA12',1500,'gr',15,15,150,NULL,'2021-08-27 09:56:40.671955','2021-08-27 09:56:40.671955',5);
/*!40000 ALTER TABLE `nucleo_producto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nucleo_rama`
--

DROP TABLE IF EXISTS `nucleo_rama`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nucleo_rama` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nucleo_rama_nombre_eec3e1ce_uniq` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nucleo_rama`
--

LOCK TABLES `nucleo_rama` WRITE;
/*!40000 ALTER TABLE `nucleo_rama` DISABLE KEYS */;
INSERT INTO `nucleo_rama` VALUES (3,'Queso CamBri','2021-08-26 14:10:53.381656','2021-08-26 14:10:53.381656'),(5,'Queso Campo','2021-08-27 09:56:19.927043','2021-08-27 09:57:01.495582');
/*!40000 ALTER TABLE `nucleo_rama` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ordendecompra_archivo`
--

DROP TABLE IF EXISTS `ordendecompra_archivo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ordendecompra_archivo` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `archivo` varchar(100) NOT NULL,
  `orden_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ordendecompra_archiv_orden_id_d3f7e4af_fk_ordendeco` (`orden_id`),
  CONSTRAINT `ordendecompra_archiv_orden_id_d3f7e4af_fk_ordendeco` FOREIGN KEY (`orden_id`) REFERENCES `ordendecompra_ordendecompra` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ordendecompra_archivo`
--

LOCK TABLES `ordendecompra_archivo` WRITE;
/*!40000 ALTER TABLE `ordendecompra_archivo` DISABLE KEYS */;
INSERT INTO `ordendecompra_archivo` VALUES (1,'ordendecompra/adjuntos/16299871770863871137135973078183.jpg',6),(2,'ordendecompra/adjuntos/20210826_101430.jpg',6),(3,'ordendecompra/adjuntos/20210826_101427.jpg',6),(4,'ordendecompra/adjuntos/20210826_101424.jpg',6);
/*!40000 ALTER TABLE `ordendecompra_archivo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ordendecompra_ordendecompra`
--

DROP TABLE IF EXISTS `ordendecompra_ordendecompra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ordendecompra_ordendecompra` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `numero` bigint NOT NULL,
  `condiciones` longtext,
  `estado` varchar(50) NOT NULL,
  `fecha` date NOT NULL,
  `total_neto` double NOT NULL,
  `guia_despacho` varchar(50) DEFAULT NULL,
  `numero_factura` varchar(50) DEFAULT NULL,
  `fecha_recepcion` date DEFAULT NULL,
  `fecha_facturacion` date DEFAULT NULL,
  `fecha_pago` date DEFAULT NULL,
  `pago` varchar(100) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `bodega_id` bigint DEFAULT NULL,
  `proveedor_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `numero` (`numero`),
  KEY `ordendecompra_ordend_proveedor_id_22f275f4_fk_proveedor` (`proveedor_id`),
  KEY `ordendecompra_ordend_bodega_id_6fe26c51_fk_inventari` (`bodega_id`),
  CONSTRAINT `ordendecompra_ordend_bodega_id_6fe26c51_fk_inventari` FOREIGN KEY (`bodega_id`) REFERENCES `inventario_bodega` (`id`),
  CONSTRAINT `ordendecompra_ordend_proveedor_id_22f275f4_fk_proveedor` FOREIGN KEY (`proveedor_id`) REFERENCES `proveedores_proveedor` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ordendecompra_ordendecompra`
--

LOCK TABLES `ordendecompra_ordendecompra` WRITE;
/*!40000 ALTER TABLE `ordendecompra_ordendecompra` DISABLE KEYS */;
INSERT INTO `ordendecompra_ordendecompra` VALUES (1,1,'','Recepcionada','2021-08-23',500000,NULL,'123','2021-08-23',NULL,NULL,NULL,'2021-08-23 11:11:43.860765','2021-08-24 09:31:39.980850',NULL,1),(2,2,'','Inicial','2021-08-23',10000,NULL,'123','2021-08-23',NULL,NULL,NULL,'2021-08-23 11:58:05.134350','2021-08-24 11:04:10.666471',NULL,1),(3,3,'','Recepcionada','2021-08-24',25000,NULL,'123','2021-08-24',NULL,NULL,NULL,'2021-08-24 09:16:42.984481','2021-08-24 09:16:57.288580',NULL,1),(4,4,'','Recepcionada','2021-08-24',250000,NULL,'123','2021-08-24',NULL,NULL,NULL,'2021-08-24 11:04:28.364929','2021-08-24 11:04:40.477536',4,1),(5,5,'100 de todo','Recepcionada','2021-08-24',600000,NULL,'123','2021-08-24',NULL,NULL,NULL,'2021-08-24 12:45:33.595272','2021-08-24 12:45:51.842420',5,1),(6,7,'','Validada','2021-08-26',10500,NULL,NULL,NULL,NULL,NULL,NULL,'2021-08-26 10:11:58.887078','2021-08-26 10:14:50.150372',9,2),(7,8,'','Inicial','2021-08-26',86100,NULL,NULL,NULL,NULL,NULL,NULL,'2021-08-26 11:02:50.060423','2021-08-26 11:03:06.077456',9,2);
/*!40000 ALTER TABLE `ordendecompra_ordendecompra` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ordendecompra_ordendecomprainsumo`
--

DROP TABLE IF EXISTS `ordendecompra_ordendecomprainsumo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ordendecompra_ordendecomprainsumo` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `cantidad` bigint NOT NULL,
  `cantidad_recibida` bigint NOT NULL,
  `detalle` varchar(255) DEFAULT NULL,
  `neto` int NOT NULL,
  `conversion` double DEFAULT NULL,
  `insumo_id` bigint NOT NULL,
  `orden_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ordendecompra_ordend_insumo_id_10121dd3_fk_proveedor` (`insumo_id`),
  KEY `ordendecompra_ordend_orden_id_ce957df8_fk_ordendeco` (`orden_id`),
  CONSTRAINT `ordendecompra_ordend_insumo_id_10121dd3_fk_proveedor` FOREIGN KEY (`insumo_id`) REFERENCES `proveedores_proveedorinsumo` (`id`),
  CONSTRAINT `ordendecompra_ordend_orden_id_ce957df8_fk_ordendeco` FOREIGN KEY (`orden_id`) REFERENCES `ordendecompra_ordendecompra` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ordendecompra_ordendecomprainsumo`
--

LOCK TABLES `ordendecompra_ordendecomprainsumo` WRITE;
/*!40000 ALTER TABLE `ordendecompra_ordendecomprainsumo` DISABLE KEYS */;
INSERT INTO `ordendecompra_ordendecomprainsumo` VALUES (2,10,0,'',1000,NULL,2,2),(5,100,100,'',1000,NULL,2,5),(7,15,0,'',700,NULL,3,6),(8,123,0,'',700,NULL,3,7);
/*!40000 ALTER TABLE `ordendecompra_ordendecomprainsumo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ordendecompra_registro`
--

DROP TABLE IF EXISTS `ordendecompra_registro`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ordendecompra_registro` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `estado` varchar(255) NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `empleado_id` int DEFAULT NULL,
  `orden_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ordendecompra_registro_empleado_id_f8c6e67c_fk_auth_user_id` (`empleado_id`),
  KEY `ordendecompra_regist_orden_id_1b869aee_fk_ordendeco` (`orden_id`),
  CONSTRAINT `ordendecompra_regist_orden_id_1b869aee_fk_ordendeco` FOREIGN KEY (`orden_id`) REFERENCES `ordendecompra_ordendecompra` (`id`),
  CONSTRAINT `ordendecompra_registro_empleado_id_f8c6e67c_fk_auth_user_id` FOREIGN KEY (`empleado_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ordendecompra_registro`
--

LOCK TABLES `ordendecompra_registro` WRITE;
/*!40000 ALTER TABLE `ordendecompra_registro` DISABLE KEYS */;
INSERT INTO `ordendecompra_registro` VALUES (1,'Inicial','2021-08-23 11:11:43.999376','2021-08-23 11:11:43.999376',1,1),(2,'Validada','2021-08-23 11:11:50.944906','2021-08-23 11:11:50.944906',1,1),(3,'Recepcionada','2021-08-23 11:11:57.108127','2021-08-23 11:11:57.108127',1,1),(4,'Inicial','2021-08-23 11:58:05.395991','2021-08-23 11:58:05.395991',1,2),(5,'Validada','2021-08-23 11:58:10.201344','2021-08-23 11:58:10.201344',1,2),(6,'Recepcionada','2021-08-23 11:58:16.347440','2021-08-23 11:58:16.347440',1,2),(7,'Validada','2021-08-23 17:08:50.353965','2021-08-23 17:08:50.353965',1,2),(8,'Inicial','2021-08-24 09:16:43.371173','2021-08-24 09:16:43.371173',1,3),(9,'Validada','2021-08-24 09:16:49.648405','2021-08-24 09:16:49.648405',1,3),(10,'Recepcionada','2021-08-24 09:16:57.239422','2021-08-24 09:16:57.239422',1,3),(11,'Validada','2021-08-24 09:17:39.815115','2021-08-24 09:17:39.815115',1,1),(12,'Recepcionada','2021-08-24 09:19:38.637780','2021-08-24 09:19:38.637780',1,1),(13,'Validada','2021-08-24 09:22:17.328085','2021-08-24 09:22:17.328085',1,1),(14,'Recepcionada','2021-08-24 09:23:42.194818','2021-08-24 09:23:42.194818',1,1),(15,'Validada','2021-08-24 09:23:52.672262','2021-08-24 09:23:52.672262',1,1),(16,'Semi-Recepcionada','2021-08-24 09:24:37.921875','2021-08-24 09:24:37.921875',1,1),(17,'Recepcionada','2021-08-24 09:31:39.733346','2021-08-24 09:31:39.733346',1,1),(18,'Inicial','2021-08-24 11:04:10.732641','2021-08-24 11:04:10.732641',1,2),(19,'Inicial','2021-08-24 11:04:28.635904','2021-08-24 11:04:28.635904',1,4),(20,'Validada','2021-08-24 11:04:34.224962','2021-08-24 11:04:34.224962',1,4),(21,'Recepcionada','2021-08-24 11:04:40.274221','2021-08-24 11:04:40.274221',1,4),(22,'Inicial','2021-08-24 12:45:33.945313','2021-08-24 12:45:33.945313',1,5),(23,'Validada','2021-08-24 12:45:40.523870','2021-08-24 12:45:40.523870',1,5),(24,'Recepcionada','2021-08-24 12:45:51.751537','2021-08-24 12:45:51.751537',1,5),(25,'Inicial','2021-08-26 10:11:59.313069','2021-08-26 10:11:59.313069',1,6),(26,'Validada','2021-08-26 10:13:09.925595','2021-08-26 10:13:09.925595',1,6),(27,'Inicial','2021-08-26 10:13:41.860878','2021-08-26 10:13:41.860878',1,6),(28,'Validada','2021-08-26 10:14:49.950266','2021-08-26 10:14:49.950266',1,6),(29,'Inicial','2021-08-26 11:02:50.405220','2021-08-26 11:02:50.405220',1,7),(30,'Validada','2021-08-26 11:02:58.912541','2021-08-26 11:02:58.912541',1,7),(31,'Inicial','2021-08-26 11:03:06.176774','2021-08-26 11:03:06.176774',1,7);
/*!40000 ALTER TABLE `ordendecompra_registro` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `proveedores_proveedor`
--

DROP TABLE IF EXISTS `proveedores_proveedor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `proveedores_proveedor` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `empresa_nombre` varchar(255) NOT NULL,
  `empresa_rut` varchar(50) NOT NULL,
  `empresa_giro` varchar(100) DEFAULT NULL,
  `empresa_region` varchar(255) DEFAULT NULL,
  `empresa_comuna` varchar(255) DEFAULT NULL,
  `empresa_direccion` varchar(255) DEFAULT NULL,
  `ventas_nombre` varchar(255) DEFAULT NULL,
  `ventas_email` varchar(255) NOT NULL,
  `ventas_celular` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `empresa_rut` (`empresa_rut`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proveedores_proveedor`
--

LOCK TABLES `proveedores_proveedor` WRITE;
/*!40000 ALTER TABLE `proveedores_proveedor` DISABLE KEYS */;
INSERT INTO `proveedores_proveedor` VALUES (1,'Ingredion Chile S.A.','82.525.800-0',NULL,'Metropolitana','Cerrillos',NULL,NULL,'efren@ingredion.cl',NULL,'2021-08-23 11:10:49.447548','2021-08-23 11:10:49.773790'),(2,'Serviform','102947266',NULL,NULL,'Selecciona una región',NULL,NULL,'serviform@afa.cl',NULL,'2021-08-25 14:25:47.663291','2021-08-25 14:25:48.371050');
/*!40000 ALTER TABLE `proveedores_proveedor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `proveedores_proveedorinsumo`
--

DROP TABLE IF EXISTS `proveedores_proveedorinsumo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `proveedores_proveedorinsumo` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre_insumo` varchar(255) NOT NULL,
  `formato` double NOT NULL,
  `precio` double NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `insumo_id` bigint NOT NULL,
  `proveedor_id` bigint NOT NULL,
  `lead` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `proveedores_proveedo_insumo_id_2c8f16a6_fk_nucleo_in` (`insumo_id`),
  KEY `proveedores_proveedo_proveedor_id_1c2ccbcd_fk_proveedor` (`proveedor_id`),
  CONSTRAINT `proveedores_proveedo_insumo_id_2c8f16a6_fk_nucleo_in` FOREIGN KEY (`insumo_id`) REFERENCES `nucleo_insumo` (`id`),
  CONSTRAINT `proveedores_proveedo_proveedor_id_1c2ccbcd_fk_proveedor` FOREIGN KEY (`proveedor_id`) REFERENCES `proveedores_proveedor` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proveedores_proveedorinsumo`
--

LOCK TABLES `proveedores_proveedorinsumo` WRITE;
/*!40000 ALTER TABLE `proveedores_proveedorinsumo` DISABLE KEYS */;
INSERT INTO `proveedores_proveedorinsumo` VALUES (2,'Pack 10 botellas',10,1000,'2021-08-23 11:57:51.906057','2021-08-24 12:46:25.585605',2,1,10),(3,'Envase 150 ML yogur',100,700,'2021-08-25 14:27:11.219995','2021-08-25 14:59:03.605085',3,2,10);
/*!40000 ALTER TABLE `proveedores_proveedorinsumo` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-08-30 10:07:14
