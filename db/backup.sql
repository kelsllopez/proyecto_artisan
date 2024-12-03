-- MySQL dump 10.13  Distrib 8.0.26, for Linux (x86_64)
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (4,'Registro limpieza'),(3,'Supervisor');
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
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES (38,3,417),(39,3,418),(40,3,419),(41,3,420),(42,3,443),(43,3,445),(44,3,446),(45,3,447),(46,3,448),(47,3,449),(48,3,450),(49,3,451),(50,3,452),(51,3,453),(52,3,454),(53,3,455),(54,3,456),(55,3,457),(56,3,458),(60,3,459),(57,4,450),(58,4,452),(59,4,454);
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
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=466 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (296,'Can add log entry',1,'add_logentry'),(297,'Can change log entry',1,'change_logentry'),(298,'Can delete log entry',1,'delete_logentry'),(299,'Can view log entry',1,'view_logentry'),(300,'Can add permission',2,'add_permission'),(301,'Can change permission',2,'change_permission'),(302,'Can delete permission',2,'delete_permission'),(303,'Can view permission',2,'view_permission'),(304,'Can add group',3,'add_group'),(305,'Can change group',3,'change_group'),(306,'Can delete group',3,'delete_group'),(307,'Can view group',3,'view_group'),(308,'Can add user',4,'add_user'),(309,'Can change user',4,'change_user'),(310,'Can delete user',4,'delete_user'),(311,'Can view user',4,'view_user'),(312,'Can add content type',5,'add_contenttype'),(313,'Can change content type',5,'change_contenttype'),(314,'Can delete content type',5,'delete_contenttype'),(315,'Can view content type',5,'view_contenttype'),(316,'Can add session',6,'add_session'),(317,'Can change session',6,'change_session'),(318,'Can delete session',6,'delete_session'),(319,'Can view session',6,'view_session'),(320,'Puede ver los insumos',7,'insumo_listar'),(321,'Puede crear un insumo',7,'insumo_crear'),(322,'Puede eliminar un insumo',7,'insumo_eliminar'),(323,'Puede actualizar un insumo',7,'insumo_actualizar'),(324,'Puede ver el listado de las bodegas',11,'bodega.listar'),(325,'Puede crear una bodega',11,'bodega.crear'),(326,'Permite eliminar una bodega',11,'bodega.eliminar'),(327,'Permite actualizar una bodega',11,'bodega.actualizar'),(328,'Puede ver el listado de los productos',12,'inventariop.listar'),(329,'Permite actualizar un producto',12,'inventariop.actualizar'),(330,'Puede ver el listado de los insumos',13,'inventarioi.listar'),(331,'Permite actualizar un insumo',13,'inventarioi.actualizar'),(332,'Puede ver el listado de los proveedores',14,'listar'),(333,'Puede crear un proveedor',14,'crear'),(334,'Permite eliminar un proveedor',14,'eliminar'),(335,'Permite actualizar un proveedor',14,'actualizar'),(336,'Permite ver el detalle de un proveedor',14,'detalle'),(337,'Puede ver el listado de los clientes',16,'cliente.listar'),(338,'Puede crear un cliente',16,'cliente.crear'),(339,'Permite eliminar una cliente',16,'cliente.eliminar'),(340,'Permite actualizar un cliente',16,'cliente.actualizar'),(341,'Permite ver el detalle de un cliente',16,'cliente.detalle'),(342,'Puede ver el listado de los locales',18,'local.listar'),(343,'Puede crear un local',18,'local.crear'),(344,'Permite eliminar un local',18,'local.eliminar'),(345,'Permite actualizar un local',18,'local.actualizar'),(346,'Permite ver el detalle de un local',18,'local.detalle'),(347,'Puede ver las ordenes de compra',19,'listar'),(348,'Puede crear una orden de compra',19,'crear'),(349,'Permite generar el pdf de una orden de compra',19,'pdf'),(350,'Permite recepcionar una orden de compra',19,'recepcionar'),(351,'Permite rechazar una orden de compra',19,'rechazar'),(352,'Permite validar una orden de compra',19,'validar'),(353,'Permite eliminar una orden de compra',19,'eliminar'),(354,'Permite pagar una orden',19,'pagar'),(355,'Permite eliminar archivos asociados a las ordenes de compra',19,'eliminararchivo'),(356,'Permite ver los archivos adjuntos',19,'verarchivo'),(357,'Can add historical orden de compra insumo',35,'add_historicalordendecomprainsumo'),(358,'Can change historical orden de compra insumo',35,'change_historicalordendecomprainsumo'),(359,'Can delete historical orden de compra insumo',35,'delete_historicalordendecomprainsumo'),(360,'Can view historical orden de compra insumo',35,'view_historicalordendecomprainsumo'),(361,'Can add historical Orden de compra',36,'add_historicalordendecompra'),(362,'Can change historical Orden de compra',36,'change_historicalordendecompra'),(363,'Can delete historical Orden de compra',36,'delete_historicalordendecompra'),(364,'Can view historical Orden de compra',36,'view_historicalordendecompra'),(365,'Permite listar los parámetros',23,'columna.listar'),(366,'Permite crear un parámetro',23,'columna.crear'),(367,'Permite eliminar un parámetro',23,'columna.eliminar'),(368,'Permite actualizar un parámetro',23,'columna.actualizar'),(369,'Permite listar las pautas de elaboración',27,'listar'),(370,'Permite crear una pauta de elaboración',27,'crear'),(371,'Permite eliminar una pauta de elaboración',27,'eliminar'),(372,'Permite actualizar una pauta de elaboración',27,'actualizar'),(373,'Permite ver el detalle de una pauta',27,'detalle'),(374,'Can add historical Pauta de elaboración',30,'add_historicalpauta'),(375,'Can change historical Pauta de elaboración',30,'change_historicalpauta'),(376,'Can delete historical Pauta de elaboración',30,'delete_historicalpauta'),(377,'Can view historical Pauta de elaboración',30,'view_historicalpauta'),(378,'Can add historical Parámetro',31,'add_historicalcolumna'),(379,'Can change historical Parámetro',31,'change_historicalcolumna'),(380,'Can delete historical Parámetro',31,'delete_historicalcolumna'),(381,'Can view historical Parámetro',31,'view_historicalcolumna'),(382,'Can add historical Instrucción',32,'add_historicalinstruccion'),(383,'Can change historical Instrucción',32,'change_historicalinstruccion'),(384,'Can delete historical Instrucción',32,'delete_historicalinstruccion'),(385,'Can view historical Instrucción',32,'view_historicalinstruccion'),(386,'Can add historical Ingrediente',33,'add_historicalingrediente'),(387,'Can change historical Ingrediente',33,'change_historicalingrediente'),(388,'Can delete historical Ingrediente',33,'delete_historicalingrediente'),(389,'Can view historical Ingrediente',33,'view_historicalingrediente'),(390,'Can add historical Etapa',34,'add_historicaletapa'),(391,'Can change historical Etapa',34,'change_historicaletapa'),(392,'Can delete historical Etapa',34,'delete_historicaletapa'),(393,'Can view historical Etapa',34,'view_historicaletapa'),(394,'Inventario Insumos - San Felipe',11,'inventarioi_san-felipe'),(395,'Inventario Productos - San Felipe',11,'inventariop_san-felipe'),(396,'Puede ver los insumos',7,'insumo.listar'),(397,'Puede crear un insumo',7,'insumo.crear'),(398,'Puede eliminar un insumo',7,'insumo.eliminar'),(399,'Puede actualizar un insumo',7,'insumo.actualizar'),(400,'Puede ver las áreas de negocio',9,'rama.listar'),(401,'Puede crear una área de negocio',9,'rama.crear'),(402,'Puede eliminar un área de negocio',9,'rama.eliminar'),(403,'Puede actualizar un área de negocio',9,'rama.actualizar'),(404,'Puede ver los productos',10,'producto.listar'),(405,'Puede crear un producto',10,'producto.crear'),(406,'Puede eliminar un producto',10,'producto.eliminar'),(407,'Puede actualizar un producto',10,'producto.actualizar'),(408,'test',11,'test'),(409,'Puede ver el listado de las asociaciones',15,'insumo.listar'),(410,'Puede crear una asociación',15,'insumo.crear'),(411,'Puede actualizar una asociación',15,'insumo.actualizar'),(412,'Puede eliminar una asociación',15,'insumo.eliminar'),(413,'Puede ver las máquinas',37,'listar'),(414,'Puede añadir una máquina',37,'crear'),(415,'Puede eliminar una máquina',37,'eliminar'),(416,'Puede actualizar una máquina',37,'actualizar'),(417,'Puede ver los equipos',38,'listar'),(418,'Puede añadir un equipo',38,'crear'),(419,'Puede eliminar un equipo',38,'eliminar'),(420,'Puede actualizar un equipo',38,'actualizar'),(441,'Inventario Insumos - Santiago',11,'inventarioi_santiago'),(442,'Inventario Productos - Santiago',11,'inventariop_santiago'),(443,'Permite generar el qr de limpieza',38,'qrlimpieza'),(445,'Puede ver los utensilios',39,'utensiliolimpieza.listar'),(446,'Puede añadir un utensilio',39,'utensiliolimpieza.crear'),(447,'Puede eliminar un utensilio',39,'utensiliolimpieza.eliminar'),(448,'Puede actualizar un utensilio',39,'utensiliolimpieza.actualizar'),(449,'Puede asociar un equipo al utensilio',39,'utensiliolimpieza.asociar'),(450,'Puede ver los registros',41,'registrolimpiezaequipo.listar'),(451,'Puede ver todos los registros',41,'registrolimpiezaequipo.administrador'),(452,'Puede añadir un registro',41,'registrolimpiezaequipo.crear'),(453,'Puede eliminar un registro',41,'registrolimpiezaequipo.eliminar'),(454,'Puede actualizar un registro',41,'registrolimpiezaequipo.actualizar'),(455,'Puede ver las areas',43,'area.listar'),(456,'Puede añadir un area',43,'area.crear'),(457,'Puede eliminar una area',43,'area.eliminar'),(458,'Puede actualizar un area',43,'area.actualizar'),(459,'Puede generar un excel',41,'registrolimpiezaequipo.excel'),(460,'Inventario Insumos - Valdivia',11,'inventarioi_valdivia'),(461,'Inventario Productos - Valdivia',11,'inventariop_valdivia'),(462,'Permite Crear Usuarios',44,'permiso.crear.usuario'),(463,'Permite Actualizar Usuarios',44,'permiso.actualizar.usuario'),(464,'Permite Eliminar Usuarios',44,'permiso.eliminar.usuario'),(465,'Permite Listar Usuarios',44,'permiso.listar.usuario');
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
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$260000$Sn5btacbH0tvf6uMYnT7jL$J8ywjdETVhN8S+HWJLYShGcN8DTaFla48ynxe2uzIGg=','2021-11-08 11:44:52.236151',1,'seba','Sebastián','Valenzuela','seba.valengo@gmail.com',1,1,'2021-08-30 18:29:02.000000'),(11,'pbkdf2_sha256$260000$oRxAeLIpIENOmqozp0npDc$v7CNGqPhoG29bmRcN2O26sEPg28YEhSkHnP7USMo4QY=','2021-10-13 08:58:40.535695',0,'adriana','Adriana','Artunduaga Rojas','',0,1,'2021-09-03 17:35:59.000000'),(26,'pbkdf2_sha256$260000$Hk46RaCDc87wRdARaUVORe$IePd6MQ/oJFhT/OENOJrlswCVumaoDGPPaQunBZG0nM=',NULL,0,'Francisco1','Francisco','Mesa','admvaldivia@quesosartisan.cl',0,1,'2021-09-13 09:22:46.875753'),(33,'pbkdf2_sha256$260000$SI7yDgKYORWRpgqqC9XtAl$NU1mgDkhmb7Mef+8I24ckq8HFr1FAsYKsvnQuikanv4=','2021-11-09 13:05:28.003088',0,'jose','Jose','Fuenmayor','jos.fuenmayor94@gmail.com',0,1,'2021-09-27 10:47:54.044100'),(34,'pbkdf2_sha256$260000$Zwo6aYCPM8GCfTSic9q9HX$kOZhFdrLcOvnDogpbzrZ/AdGKN9//vuzq3BxmoP7/vA=','2021-10-15 12:44:14.982155',0,'bastian','Bastian','Oliva','bastianignaciooliva2018@gmail.com',0,1,'2021-10-15 09:42:48.971875'),(36,'pbkdf2_sha256$260000$bXeZaXlrcrAl10OhcUdwOX$QAYHMvCkccWm/jvG0EmEYxwS8pq2VDS9O10RjNSucMc=',NULL,0,'pan@pan.cl','','','',0,1,'2021-10-20 17:05:43.184587'),(37,'pbkdf2_sha256$260000$mLNgEi28nfpFRvoSGgB0O0$3DO0i/uVgPpTLzUO/IFsc18bvqelN1V6/SzIawI4N5w=','2021-11-09 11:02:40.660598',1,'calidad@quesosartisan.cl','Adriana','Artunduaga','calidad@quesosartisan.cl',0,1,'2021-10-20 17:06:00.000000'),(38,'pbkdf2_sha256$260000$PNzZkhWGbgZPId4phXTWTO$NzPXWqCmJjylixJIxZPX3T8+Ha0a2wx3ASUDpFmTJfE=',NULL,1,'produccion@quesosartisan.cl','Camila','Gatica','produccion@quesosartisan.cl',0,1,'2021-10-20 17:06:46.000000'),(39,'pbkdf2_sha256$260000$yBeDzZfSaL7kfxDqOK43oh$X/gUWzDApjdKhvwEHLSNJAVuayUovAeNijLrT2bnF4k=','2021-11-02 15:08:17.669470',1,'logistica@quesosartisan.cl','Deyanira','Poblete','Logistica@quesosartisan.cl',0,1,'2021-10-20 17:07:09.000000'),(40,'pbkdf2_sha256$260000$V0W3aj5RxeN6AXhjQkHIxh$6Gomchd9aEl8cPKG8JruEGiWjktihyC2faRtGdo/ECE=',NULL,1,'admvaldivia@quesosartisan.cl','Francisco','Mesa','admvaldivia@quesosartisan.cl',0,1,'2021-10-20 17:07:28.000000'),(41,'pbkdf2_sha256$260000$tagj6QXynBAuoNcIBXMYGC$T4M7RcC8DueZy8Q7QYqmhGHATcCXj2CDJgrmdgzAm1A=','2021-11-08 10:52:16.986534',1,'administracion@quesosartisan.cl','Santiago','Donoso','administracion@quesosartisan.cl',1,1,'2021-10-20 17:07:45.000000'),(42,'pbkdf2_sha256$260000$XPVFJe30gRmKaQTim0TNcv$7fG1+fGmzyMvJWzPTpkd1o+4HhM8LoSa1Q93fEM+Stw=','2021-11-09 16:20:50.495727',1,'hvigil@quesosartisan.cl','Hernan','Vigil','hvigil@quesosartisan.cl',1,1,'2021-10-20 17:08:06.000000');
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
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
INSERT INTO `auth_user_groups` VALUES (2,11,3),(6,26,3),(14,33,4),(15,34,4),(18,37,3);
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
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=168 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
INSERT INTO `auth_user_user_permissions` VALUES (165,11,462),(166,11,463),(167,11,465);
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `calidad_equipoutensiliolimpieza`
--

DROP TABLE IF EXISTS `calidad_equipoutensiliolimpieza`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `calidad_equipoutensiliolimpieza` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `equipo_id` bigint NOT NULL,
  `utensilio_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `calidad_equipoutensiliol_equipo_id_utensilio_id_c197f7df_uniq` (`equipo_id`,`utensilio_id`),
  KEY `calidad_equipoutensi_utensilio_id_b540df24_fk_calidad_u` (`utensilio_id`),
  CONSTRAINT `calidad_equipoutensi_equipo_id_7de311ae_fk_equipo_eq` FOREIGN KEY (`equipo_id`) REFERENCES `equipo_equipo` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `calidad_equipoutensi_utensilio_id_b540df24_fk_calidad_u` FOREIGN KEY (`utensilio_id`) REFERENCES `calidad_utensiliolimpieza` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `calidad_equipoutensiliolimpieza`
--

LOCK TABLES `calidad_equipoutensiliolimpieza` WRITE;
/*!40000 ALTER TABLE `calidad_equipoutensiliolimpieza` DISABLE KEYS */;
INSERT INTO `calidad_equipoutensiliolimpieza` VALUES (6,'2021-09-27 08:58:02.224593','2021-09-27 08:58:02.224623',4,5),(7,'2021-09-27 08:58:27.843289','2021-09-27 08:58:27.843311',4,6),(8,'2021-09-27 08:59:13.477339','2021-09-27 08:59:13.477361',1,7),(9,'2021-09-27 09:00:47.198528','2021-09-27 09:00:47.198553',4,7),(10,'2021-09-27 09:01:38.459556','2021-09-27 09:01:38.459581',4,8);
/*!40000 ALTER TABLE `calidad_equipoutensiliolimpieza` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `calidad_registrolimpiezaequipo`
--

DROP TABLE IF EXISTS `calidad_registrolimpiezaequipo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `calidad_registrolimpiezaequipo` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `observacion` longtext,
  `estado` longtext NOT NULL,
  `observacion_correctiva` longtext,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `equipo_id` bigint NOT NULL,
  `encargado_id` int DEFAULT NULL,
  `revisado_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `calidad_registrolimp_equipo_id_c251a62b_fk_equipo_eq` (`equipo_id`),
  KEY `calidad_registrolimp_encargado_id_7bd6e355_fk_auth_user` (`encargado_id`),
  KEY `calidad_registrolimp_revisado_id_73096a14_fk_auth_user` (`revisado_id`),
  CONSTRAINT `calidad_registrolimp_encargado_id_7bd6e355_fk_auth_user` FOREIGN KEY (`encargado_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `calidad_registrolimp_equipo_id_c251a62b_fk_equipo_eq` FOREIGN KEY (`equipo_id`) REFERENCES `equipo_equipo` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `calidad_registrolimp_revisado_id_73096a14_fk_auth_user` FOREIGN KEY (`revisado_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `calidad_registrolimpiezaequipo`
--

LOCK TABLES `calidad_registrolimpiezaequipo` WRITE;
/*!40000 ALTER TABLE `calidad_registrolimpiezaequipo` DISABLE KEYS */;
INSERT INTO `calidad_registrolimpiezaequipo` VALUES (15,'','Aprobado','','2021-09-30 12:19:34.641580','2021-10-01 10:40:51.331665',4,33,11),(16,'','Aprobado','','2021-10-01 08:55:30.784104','2021-10-01 10:41:00.196958',4,33,11),(17,'','Aprobado','ok','2021-10-02 14:22:27.460734','2021-10-04 11:48:28.983163',4,33,11),(18,'','Aprobado','','2021-10-05 09:00:12.413806','2021-10-08 11:44:04.621261',4,33,11),(19,'','Aprobado','Se cambia el termómetro y se hace limpieza de accesorios (válvula mariposa)','2021-10-08 09:33:07.598817','2021-10-08 11:46:40.520801',4,33,11),(20,'','Aprobado','','2021-10-12 10:06:50.807541','2021-10-13 08:59:18.110894',4,33,11),(21,'Lavado por fuera , lavado en llave de paso.','Aprobado','','2021-10-15 11:44:36.585847','2021-10-15 12:37:18.890942',4,34,11),(22,'','Aprobado','','2021-10-20 08:22:38.490363','2021-10-22 08:27:48.678259',4,33,11),(23,'','Aprobado','','2021-10-23 10:22:41.579328','2021-10-26 08:19:02.445160',4,33,37),(24,'','Aprobado','','2021-10-27 10:11:26.712269','2021-10-28 11:52:07.054279',4,33,37),(25,'','Aprobado','Lavado de llave y termómetro','2021-10-28 11:04:25.279466','2021-10-28 11:52:35.601798',4,33,37),(26,'','Ejecutado',NULL,'2021-11-09 13:05:32.170232','2021-11-09 13:05:32.178931',4,33,NULL);
/*!40000 ALTER TABLE `calidad_registrolimpiezaequipo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `calidad_registrolimpiezaequipo_utensilios`
--

DROP TABLE IF EXISTS `calidad_registrolimpiezaequipo_utensilios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `calidad_registrolimpiezaequipo_utensilios` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `registrolimpiezaequipo_id` bigint NOT NULL,
  `utensiliolimpieza_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `calidad_registrolimpieza_registrolimpiezaequipo_i_27ba4a90_uniq` (`registrolimpiezaequipo_id`,`utensiliolimpieza_id`),
  KEY `calidad_registrolimp_utensiliolimpieza_id_76046cb6_fk_calidad_u` (`utensiliolimpieza_id`),
  CONSTRAINT `calidad_registrolimp_registrolimpiezaequi_6c2d033e_fk_calidad_r` FOREIGN KEY (`registrolimpiezaequipo_id`) REFERENCES `calidad_registrolimpiezaequipo` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `calidad_registrolimp_utensiliolimpieza_id_76046cb6_fk_calidad_u` FOREIGN KEY (`utensiliolimpieza_id`) REFERENCES `calidad_utensiliolimpieza` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `calidad_registrolimpiezaequipo_utensilios`
--

LOCK TABLES `calidad_registrolimpiezaequipo_utensilios` WRITE;
/*!40000 ALTER TABLE `calidad_registrolimpiezaequipo_utensilios` DISABLE KEYS */;
INSERT INTO `calidad_registrolimpiezaequipo_utensilios` VALUES (16,15,5),(17,15,7),(18,16,5),(19,16,7),(20,17,5),(21,17,7),(22,18,5),(23,18,7),(24,19,5),(25,20,5),(26,21,5),(27,21,7),(28,22,5),(29,23,5),(30,24,5),(31,25,5),(32,26,5);
/*!40000 ALTER TABLE `calidad_registrolimpiezaequipo_utensilios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `calidad_registrolimpiezaequipohistorial`
--

DROP TABLE IF EXISTS `calidad_registrolimpiezaequipohistorial`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `calidad_registrolimpiezaequipohistorial` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `observacion` longtext,
  `estado` longtext NOT NULL,
  `observacion_correctiva` longtext,
  `registrolimpiezequipo_id` bigint NOT NULL,
  `created` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `calidad_registrolimp_registrolimpiezequip_fe52f4ee_fk_calidad_r` (`registrolimpiezequipo_id`),
  CONSTRAINT `calidad_registrolimp_registrolimpiezequip_fe52f4ee_fk_calidad_r` FOREIGN KEY (`registrolimpiezequipo_id`) REFERENCES `calidad_registrolimpiezaequipo` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `calidad_registrolimpiezaequipohistorial`
--

LOCK TABLES `calidad_registrolimpiezaequipohistorial` WRITE;
/*!40000 ALTER TABLE `calidad_registrolimpiezaequipohistorial` DISABLE KEYS */;
INSERT INTO `calidad_registrolimpiezaequipohistorial` VALUES (16,'','Ejecutado',NULL,15,'2021-09-30 12:19:34.688028'),(17,'','Ejecutado',NULL,16,'2021-10-01 08:55:30.823484'),(18,'','Aprobado','',15,'2021-10-01 10:40:51.327938'),(19,'','Aprobado','',16,'2021-10-01 10:41:00.193694'),(20,'','Ejecutado',NULL,17,'2021-10-02 14:22:27.503352'),(21,'','Aprobado','ok',17,'2021-10-04 11:48:28.973506'),(22,'','Ejecutado',NULL,18,'2021-10-05 09:00:12.447007'),(23,'','Ejecutado',NULL,19,'2021-10-08 09:33:07.632231'),(24,'','Aprobado','',18,'2021-10-08 11:44:04.616949'),(25,'','Ejecutado','Se cambia el termómetro y se hace limpieza de accesorios (válvula mariposa)',19,'2021-10-08 11:46:25.725176'),(26,'','Aprobado','Se cambia el termómetro y se hace limpieza de accesorios (válvula mariposa)',19,'2021-10-08 11:46:40.517396'),(27,'','Ejecutado',NULL,20,'2021-10-12 10:06:50.850763'),(28,'','Aprobado','',20,'2021-10-13 08:59:18.106111'),(29,'Lavado por fuera , lavado en llave de paso.','Ejecutado',NULL,21,'2021-10-15 11:44:36.610977'),(30,'Lavado por fuera , lavado en llave de paso.','Aprobado','',21,'2021-10-15 12:37:18.887482'),(31,'','Ejecutado',NULL,22,'2021-10-20 08:22:38.501928'),(32,'','Aprobado','',22,'2021-10-22 08:27:48.676589'),(33,'','Ejecutado',NULL,23,'2021-10-23 10:22:41.586405'),(34,'','Ejecutado','',23,'2021-10-26 08:18:47.344106'),(35,'','Aprobado','',23,'2021-10-26 08:19:02.443678'),(36,'','Ejecutado',NULL,24,'2021-10-27 10:11:26.720506'),(37,'','Ejecutado',NULL,25,'2021-10-28 11:04:25.287393'),(38,'','Aprobado','',24,'2021-10-28 11:52:07.052469'),(39,'','Aprobado','Lavado de llave y termómetro',25,'2021-10-28 11:52:35.600294'),(40,'','Ejecutado',NULL,26,'2021-11-09 13:05:32.178013');
/*!40000 ALTER TABLE `calidad_registrolimpiezaequipohistorial` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `calidad_utensiliolimpieza`
--

DROP TABLE IF EXISTS `calidad_utensiliolimpieza`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `calidad_utensiliolimpieza` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `categoria` varchar(255) NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `calidad_utensiliolimpieza`
--

LOCK TABLES `calidad_utensiliolimpieza` WRITE;
/*!40000 ALTER TABLE `calidad_utensiliolimpieza` DISABLE KEYS */;
INSERT INTO `calidad_utensiliolimpieza` VALUES (5,'Spumax','detergente','2021-09-13 10:16:59.576403','2021-09-13 10:16:59.576424'),(6,'cepillo azul','utensilio de limpieza','2021-09-22 12:36:07.442187','2021-09-22 12:36:07.442208'),(7,'Hidrolavadora','utensilio de limpieza','2021-09-27 08:59:05.975481','2021-09-27 08:59:05.975501'),(8,'Acid cip','detergente','2021-09-27 09:01:27.719611','2021-09-27 09:01:27.719631');
/*!40000 ALTER TABLE `calidad_utensiliolimpieza` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes_cliente`
--

LOCK TABLES `clientes_cliente` WRITE;
/*!40000 ALTER TABLE `clientes_cliente` DISABLE KEYS */;
INSERT INTO `clientes_cliente` VALUES (1,'HORECA','Universidad Adolfo Ibañez','UAI','3122k','Manicure','+5623155224','Metropolitana','Las Condes','Frederick 312','Mrs Andrews','andrews@uai.cl','3155224','2021-09-02 16:00:44.989900','2021-09-07 10:11:24.495117');
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
  CONSTRAINT `clientes_clientelocal_cliente_id_54e0f87b_fk_clientes_cliente_id` FOREIGN KEY (`cliente_id`) REFERENCES `clientes_cliente` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes_clientelocal`
--

LOCK TABLES `clientes_clientelocal` WRITE;
/*!40000 ALTER TABLE `clientes_clientelocal` DISABLE KEYS */;
INSERT INTO `clientes_clientelocal` VALUES (1,'Hotel Trivago Las Condes','3952000','Tarapacá','Camiña','Manquehue sur 1380','Rodrigo Gallardox','seba.valengo@gmail.com','+56223952524',NULL,'2021-09-02 16:11:48.670172','2021-09-07 10:18:36.493981',1),(2,'Barrio Bellavista','3155224','Tarapacá','Huara','3155224','hedro',NULL,NULL,NULL,'2021-09-07 10:14:45.406994','2021-09-07 10:14:45.461689',1),(3,'Central','+56984902256','Tarapacá','Camiña','Manquehue sur 1380','Rodrigo Gallardo',NULL,NULL,NULL,'2021-09-07 10:17:23.310496','2021-09-07 10:17:23.460302',1);
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
  CONSTRAINT `clientes_clienteprod_cliente_id_527534e7_fk_clientes_` FOREIGN KEY (`cliente_id`) REFERENCES `clientes_cliente` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `clientes_clienteprod_producto_id_98a6114f_fk_nucleo_pr` FOREIGN KEY (`producto_id`) REFERENCES `nucleo_producto` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=267 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2021-08-31 09:05:21.312469','1','PH',1,'[{\"added\": {}}]',23,1),(2,'2021-08-31 09:05:25.456726','2','T°',1,'[{\"added\": {}}]',23,1),(3,'2021-08-31 09:05:35.995789','1','Área de negocio: Queso CamBri',1,'El empleado seba ha agregado el área de negocio: Queso CamBri',9,1),(4,'2021-08-31 09:06:10.122149','1','Insumo Leche',1,'El empleado seba ha agregado el insumo Leche',7,1),(5,'2021-08-31 09:06:22.495165','2','Insumo Azucar',1,'El empleado seba ha agregado el insumo Azucar',7,1),(6,'2021-08-31 10:01:07.830503','1','Bodega Santiago',1,'El usuario seba ha creado la bodega Santiago',11,1),(7,'2021-08-31 10:01:26.736266','1','Proveedor Ingredion Chile S.A.',1,'El proveedor Ingredion Chile S.A. ha sido creado por el usuario  ',14,1),(8,'2021-08-31 10:02:08.149646','1','Orden de compra 0',1,'La orden de compra 0 ha sido solicitada el usuario  ',19,1),(9,'2021-08-31 15:32:13.984151','4','Pauta de elaboración Queso Campo',1,'La pauta de elaboración Queso Campo ha sido añadida por el usuario seba',27,1),(10,'2021-08-31 15:32:43.478561','1','Sebastián Valenzuela',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\"]}}]',4,1),(11,'2021-08-31 15:39:42.242615','6','Pauta de elaboración Santiago',1,'La pauta de elaboración Santiago ha sido añadida por el usuario Sebastián Valenzuela',27,1),(12,'2021-08-31 15:44:58.579513','6','Yogurt Clasico',2,'[{\"changed\": {\"fields\": [\"Columnas\"]}}]',27,1),(13,'2021-08-31 16:09:10.931877','1','Orden de compra 0',2,'La orden de compra 0 ha sido Validada por el usuario Sebastián Valenzuela',19,1),(14,'2021-08-31 16:09:48.916331','1','Orden de compra 0',2,'La orden de compra 0 ha sido Inicial por el usuario Sebastián Valenzuela',19,1),(15,'2021-08-31 16:09:55.887900','1','Orden de compra 0',2,'La orden de compra 0 ha sido Validada por el usuario Sebastián Valenzuela',19,1),(16,'2021-08-31 16:12:47.937452','6','Pauta de elaboración Yogurt Clasico',3,'La pauta de elaboración Yogurt Clasico ha sido eliminada por el usuario Sebastián Valenzuela',27,1),(17,'2021-08-31 17:12:41.378873','3','Parámetro Fecha',3,'El parámetro Fecha ha sido eliminado por el usuario Sebastián Valenzuela',23,1),(18,'2021-08-31 18:05:45.352363','2',' ',1,'[{\"added\": {}}]',4,1),(19,'2021-08-31 18:05:55.781703','2','Hernan Vigil',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Email address\", \"Staff status\", \"Superuser status\"]}}]',4,1),(20,'2021-08-31 18:06:02.602064','3',' ',1,'[{\"added\": {}}]',4,1),(21,'2021-08-31 18:06:15.080428','3','Santiago Donoso',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Superuser status\"]}}]',4,1),(22,'2021-08-31 18:06:23.091326','4',' ',1,'[{\"added\": {}}]',4,1),(23,'2021-08-31 18:06:30.447282','4','Camila ',2,'[{\"changed\": {\"fields\": [\"First name\", \"Superuser status\"]}}]',4,1),(24,'2021-09-01 15:16:59.626503','2','Bodega San Felipe',1,'El usuario Sebastián Valenzuela ha creado la bodega San Felipe',11,1),(25,'2021-09-01 16:50:20.375869','1','Clientes',1,'[{\"added\": {}}]',3,1),(41,'2021-09-02 10:51:02.943611','1','Área de negocio: Queso CamBri',3,'El empleado Sebastián Valenzuela ha eliminado el área de negocio: Queso CamBri',9,1),(42,'2021-09-02 10:51:08.835704','2','Área de negocio: Queso CamBri',1,'El empleado Sebastián Valenzuela ha agregado el área de negocio: Queso CamBri',9,1),(43,'2021-09-02 10:52:12.366502','5','Producto: Santiago',1,'El empleado Sebastián Valenzuela ha agregado el producto: Santiago',10,1),(44,'2021-09-02 11:03:46.772682','5','Producto: Santiago',2,'El empleado Sebastián Valenzuela ha modificado el producto: Santiago',10,1),(45,'2021-09-02 15:46:00.208798','10','Prueba Permisos',2,'[{\"changed\": {\"fields\": [\"password\"]}}]',4,1),(46,'2021-09-02 15:48:24.352856','10','Prueba Permisos',2,'[{\"changed\": {\"fields\": [\"User permissions\", \"Last login\"]}}]',4,1),(50,'2021-09-02 15:59:20.575893','10','Prueba Permisos',2,'[{\"changed\": {\"fields\": [\"User permissions\"]}}]',4,1),(51,'2021-09-02 15:59:46.363530','10','Prueba Permisos',2,'[{\"changed\": {\"fields\": [\"User permissions\"]}}]',4,1),(53,'2021-09-02 16:02:51.013312','10','Prueba Permisos',2,'[{\"changed\": {\"fields\": [\"User permissions\"]}}]',4,1),(56,'2021-09-02 16:04:37.174579','10','Prueba Permisos',2,'[{\"changed\": {\"fields\": [\"User permissions\"]}}]',4,1),(57,'2021-09-02 16:11:22.420258','10','Prueba Permisos',2,'[{\"changed\": {\"fields\": [\"User permissions\"]}}]',4,1),(59,'2021-09-02 16:12:02.583675','10','Prueba Permisos',2,'[{\"changed\": {\"fields\": [\"User permissions\"]}}]',4,1),(60,'2021-09-02 16:14:32.618016','10','Prueba Permisos',2,'[{\"changed\": {\"fields\": [\"User permissions\"]}}]',4,1),(62,'2021-09-02 16:15:25.848791','10','Prueba Permisos',2,'[{\"changed\": {\"fields\": [\"User permissions\"]}}]',4,1),(63,'2021-09-03 15:21:36.041460','6','Pauta de elaboración Asd',1,'La pauta de elaboración Asd ha sido añadida por el usuario Sebastián Valenzuela',27,1),(64,'2021-09-03 17:35:59.304035','11',' ',1,'[{\"added\": {}}]',4,1),(65,'2021-09-03 17:36:07.581018','11',' ',2,'[{\"changed\": {\"fields\": [\"User permissions\"]}}]',4,1),(66,'2021-09-03 18:01:33.427099','11',' ',2,'[{\"changed\": {\"fields\": [\"User permissions\"]}}]',4,1),(89,'2021-09-07 10:56:04.274773','3','Equipo Prueba',1,'Se ha creado el equipo Prueba en Santiago por el usuario Sebastián Valenzuela',38,1),(90,'2021-09-07 10:56:07.943902','3','Equipo Pruebad',2,'Se ha actualizado el equipo Pruebad en Santiago por el usuario Sebastián Valenzuela',38,1),(91,'2021-09-07 10:56:10.017182','3','Equipo Pruebad',3,'Se ha eliminado el equipo Pruebad en Santiago por el usuario Sebastián Valenzuela',38,1),(96,'2021-09-07 11:12:13.788469','10','Prueba Permisos',2,'[{\"changed\": {\"fields\": [\"User permissions\"]}}]',4,1),(99,'2021-09-07 11:13:15.042265','10','Prueba Permisos',2,'[{\"changed\": {\"fields\": [\"User permissions\"]}}]',4,1),(101,'2021-09-07 11:35:17.940868','2','Equipo Maquina de Quesos',1,'Se ha creado el equipo Maquina de Quesos en Santiago por el usuario Sebastián Valenzuela',38,1),(102,'2021-09-07 11:53:22.106233','2','Orden de compra 1',1,'La orden de compra 1 ha sido solicitada el usuario Sebastián Valenzuela',19,1),(103,'2021-09-07 11:53:26.587969','2','Orden de compra 1',2,'La orden de compra 1 ha sido Validada por el usuario Sebastián Valenzuela',19,1),(104,'2021-09-07 11:53:44.738402','2','Orden de compra 1',2,'La orden de compra 1 ha sido Recepcionada por el usuario Sebastián Valenzuela',19,1),(107,'2021-09-07 15:29:44.721458','6','Pauta de elaboración Asdd',2,'La pauta de elaboración Asdd ha sido actualizada por el usuario Sebastián Valenzuela',27,1),(112,'2021-09-08 15:45:37.220302','429','calidad | Registro Limpieza Equipo | Puede actualizar un registro',3,'',2,1),(113,'2021-09-08 15:45:37.275352','427','calidad | Registro Limpieza Equipo | Puede añadir un registro',3,'',2,1),(114,'2021-09-08 15:45:37.292332','428','calidad | Registro Limpieza Equipo | Puede eliminar un registro',3,'',2,1),(115,'2021-09-08 15:45:37.309175','426','calidad | Registro Limpieza Equipo | Puede ver los registros',3,'',2,1),(116,'2021-09-08 15:45:37.344026','438','calidad | Registro Limpieza Equipo | Puede actualizar un registro',3,'',2,1),(117,'2021-09-08 15:45:37.434003','444','calidad | Registro Limpieza Equipo | Puede ver todos los registros',3,'',2,1),(118,'2021-09-08 15:45:37.484477','436','calidad | Registro Limpieza Equipo | Puede añadir un registro',3,'',2,1),(119,'2021-09-08 15:45:37.500814','437','calidad | Registro Limpieza Equipo | Puede eliminar un registro',3,'',2,1),(120,'2021-09-08 15:45:37.517951','435','calidad | Registro Limpieza Equipo | Puede ver los registros',3,'',2,1),(121,'2021-09-08 15:45:37.534391','424','calidad | utensilio | Puede actualizar un utensilio',3,'',2,1),(122,'2021-09-08 15:45:37.551308','425','calidad | utensilio | Puede asociar un equipo al utensilio',3,'',2,1),(123,'2021-09-08 15:45:37.567720','422','calidad | utensilio | Puede añadir un utensilio',3,'',2,1),(124,'2021-09-08 15:45:37.585152','423','calidad | utensilio | Puede eliminar un utensilio',3,'',2,1),(125,'2021-09-08 15:45:37.601045','421','calidad | utensilio | Puede ver los utensilios',3,'',2,1),(126,'2021-09-08 15:45:37.618168','433','calidad | utensilio | Puede actualizar un utensilio',3,'',2,1),(127,'2021-09-08 15:45:37.634580','434','calidad | utensilio | Puede asociar un equipo al utensilio',3,'',2,1),(128,'2021-09-08 15:45:37.703360','431','calidad | utensilio | Puede añadir un utensilio',3,'',2,1),(129,'2021-09-08 15:45:37.779909','432','calidad | utensilio | Puede eliminar un utensilio',3,'',2,1),(130,'2021-09-08 15:45:37.835123','430','calidad | utensilio | Puede ver los utensilios',3,'',2,1),(131,'2021-09-08 16:38:36.645317','2','Equipo Maquina de Quesos',2,'Se ha actualizado el equipo Maquina de Quesos en Sala de Queso por el usuario Sebastián Valenzuela',38,1),(132,'2021-09-08 16:39:06.046722','1','Equipo Maquina de Queso',2,'Se ha actualizado el equipo Maquina de Queso en Sala De Jamon por el usuario Sebastián Valenzuela',38,1),(133,'2021-09-08 16:40:51.594671','2','Equipo Maquina de Quesos',2,'Se ha actualizado el equipo Maquina de Quesos en Sala de Queso por el usuario Sebastián Valenzuela',38,1),(134,'2021-09-08 16:41:00.252042','3','Equipo San Felipe',1,'Se ha creado el equipo San Felipe en Sala de Basura por el usuario Sebastián Valenzuela',38,1),(135,'2021-09-09 15:44:21.880026','4','Bodega Valdivia',1,'El usuario Sebastián Valenzuela ha creado la bodega Valdivia',11,1),(136,'2021-09-09 15:58:38.316986','3','Equipo Impresora',2,'Se ha actualizado el equipo Impresora en Santiago por el usuario Sebastián Valenzuela',38,1),(137,'2021-09-09 16:34:38.750809','4','Equipo Impresora v2',1,'Se ha creado el equipo Impresora v2 en Sala De Jamon por el usuario Adriana ',38,11),(138,'2021-09-09 16:34:47.861539','4','Equipo Impresora v2',3,'Se ha eliminado el equipo Impresora v2 en Sala De Jamon por el usuario Adriana ',38,11),(139,'2021-09-09 16:37:44.054078','3','Equipo Impresora',3,'Se ha eliminado el equipo Impresora en Santiago por el usuario Adriana ',38,11),(140,'2021-09-09 16:47:28.975243','5','Área Permiso',1,'Se ha creado el área Permiso en VALDIVIA por el usuario Sebastián Valenzuela',43,1),(141,'2021-09-09 16:47:31.862402','5','Área Permisod',2,'Se ha actualizado el área Permisod en VALDIVIA por el usuario Sebastián Valenzuela',43,1),(142,'2021-09-09 16:47:34.748317','5','Área Permisod',3,'Se ha eliminado el área Permisod en VALDIVIA por el usuario Sebastián Valenzuela',43,1),(143,'2021-09-09 18:02:39.004569','11','Adriana ',2,'[{\"changed\": {\"fields\": [\"User permissions\"]}}]',4,1),(144,'2021-09-09 18:03:14.118174','11','Adriana ',2,'[{\"changed\": {\"fields\": [\"User permissions\"]}}]',4,1),(145,'2021-09-13 10:13:32.206810','5','Área Envasado de yogurt',1,'Se ha creado el área Envasado de yogurt en VALDIVIA por el usuario Adriana ',43,11),(146,'2021-09-13 10:13:58.398896','3','Equipo Envasadora de yogurt',1,'Se ha creado el equipo Envasadora de yogurt en Envasado de yogurt por el usuario Adriana ',38,11),(147,'2021-09-15 10:12:40.898385','30','Jorge Prueba',2,'[{\"changed\": {\"fields\": [\"Superuser status\"]}}]',4,1),(148,'2021-09-15 10:14:04.412778','30','Jorge Prueba',2,'[{\"changed\": {\"fields\": [\"Superuser status\", \"Groups\"]}}]',4,1),(149,'2021-09-21 19:11:59.417072','1','Inventario Insumo Azucar - Santiago',2,'Se ha actualizado el inventario de Azucar en Santiago de manera MANUAL por el usuario Sebastián Valenzuela',13,1),(150,'2021-09-21 19:12:31.472469','3','Orden de compra 2',1,'La orden de compra 2 ha sido solicitada el usuario Sebastián Valenzuela',19,1),(151,'2021-09-21 19:12:42.488512','3','Orden de compra 2',2,'La orden de compra 2 ha sido Validada por el usuario Sebastián Valenzuela',19,1),(152,'2021-09-21 19:13:03.921168','3','Orden de compra 2',2,'La orden de compra 2 ha sido Recepcionada por el usuario Sebastián Valenzuela',19,1),(153,'2021-09-22 12:19:22.723585','3','Equipo Envasadora de yogurt',3,'Se ha eliminado el equipo Envasadora de yogurt en Envasado de yogurt por el usuario Adriana ',38,11),(154,'2021-09-22 12:28:41.478691','5','Área Envasado de yogurt',3,'Se ha eliminado el área Envasado de yogurt en VALDIVIA por el usuario Adriana ',43,11),(155,'2021-09-22 12:28:58.403386','6','Área Sala de yogurt',1,'Se ha creado el área Sala de yogurt en VALDIVIA por el usuario Adriana ',43,11),(156,'2021-09-22 12:29:26.572828','6','Área Sala de yogurt',2,'Se ha actualizado el área Sala de yogurt en VALDIVIA por el usuario Adriana ',43,11),(157,'2021-09-22 12:29:52.834284','4','Equipo Tanque de yogurt',1,'Se ha creado el equipo Tanque de yogurt en Sala de yogurt por el usuario Adriana ',38,11),(158,'2021-10-20 12:32:29.851624','35','Sebastián Valenzuela',2,'[{\"changed\": {\"fields\": [\"Username\", \"Groups\"]}}]',4,1),(159,'2021-10-20 17:05:43.282996','36','pan@pan.cl',1,'[{\"added\": {}}]',4,1),(160,'2021-10-20 17:08:22.126836','41','Santiago Donoso',2,'[{\"changed\": {\"fields\": [\"Staff status\"]}}]',4,1),(161,'2021-10-20 17:08:31.477489','41','Santiago Donoso',2,'[{\"changed\": {\"fields\": [\"Staff status\", \"Superuser status\"]}}]',4,1),(162,'2021-10-20 17:08:37.208964','40','Francisco Mesa',2,'[{\"changed\": {\"fields\": [\"Superuser status\"]}}]',4,1),(163,'2021-10-20 17:08:47.661375','37','Adriana Artunduaga',2,'[{\"changed\": {\"fields\": [\"Superuser status\"]}}]',4,1),(164,'2021-10-20 17:08:54.500767','42','Hernan Vigil',2,'[{\"changed\": {\"fields\": [\"Staff status\", \"Superuser status\"]}}]',4,1),(165,'2021-10-20 17:09:00.973102','39','Deyanira Poblete',2,'[{\"changed\": {\"fields\": [\"Superuser status\"]}}]',4,1),(166,'2021-10-20 17:09:17.381595','38','Camila Gatica',2,'[{\"changed\": {\"fields\": [\"Superuser status\"]}}]',4,1),(167,'2021-10-22 09:14:08.697709','3','Insumo Almidon Snowflakes',1,'El empleado Santiago Donoso ha agregado el insumo Almidon Snowflakes',7,41),(168,'2021-10-22 10:12:56.580553','4','Orden de compra 3',1,'La orden de compra 3 ha sido solicitada el usuario Santiago Donoso',19,41),(169,'2021-10-22 10:16:09.687358','41','Santiago Donoso',2,'[{\"changed\": {\"fields\": [\"Staff status\"]}}]',4,1),(170,'2021-10-22 10:19:44.568716','4','Orden de compra 3',2,'La orden de compra 3 ha sido Validada por el usuario Santiago Donoso',19,41),(171,'2021-10-22 10:20:18.465600','4','Orden de compra 3',3,'La orden de compra 3 ha sido rechazada por el usuario Santiago Donoso',19,41),(172,'2021-10-22 10:20:35.229957','4','Orden de compra 3',2,'La orden de compra 3 ha sido Validada por el usuario Santiago Donoso',19,41),(173,'2021-10-22 10:25:40.400920','2','Insumo Azucar',2,'El empleado Santiago Donoso ha modificado el insumo Azucar',7,41),(174,'2021-10-22 10:26:28.873351','1','Insumo Leche',2,'El empleado Santiago Donoso ha modificado el insumo Leche',7,41),(175,'2021-10-22 10:26:42.706722','1','Insumo Leche en polvo descremada',2,'El empleado Santiago Donoso ha modificado el insumo Leche en polvo descremada',7,41),(176,'2021-10-22 10:26:51.439129','2','Insumo Azucar',2,'El empleado Santiago Donoso ha modificado el insumo Azucar',7,41),(177,'2021-10-22 10:27:17.600502','4','Insumo Proteina de Haba',1,'El empleado Santiago Donoso ha agregado el insumo Proteina de Haba',7,41),(178,'2021-10-22 10:27:38.389720','5','Insumo N-Dulge',1,'El empleado Santiago Donoso ha agregado el insumo N-Dulge',7,41),(179,'2021-10-25 17:21:48.732383','6','Insumo Bolsa Vacio 160x200x80 micras',1,'El empleado Santiago Donoso ha agregado el insumo Bolsa Vacio 160x200x80 micras',7,41),(180,'2021-10-25 17:23:42.058066','2','Proveedor FIBRO CHILE',1,'El proveedor FIBRO CHILE ha sido creado por el usuario Santiago Donoso',14,41),(181,'2021-10-25 17:25:02.713534','5','Orden de compra 4',1,'La orden de compra 4 ha sido solicitada el usuario Santiago Donoso',19,41),(182,'2021-10-25 17:38:11.410247','7','Insumo LACTOSA',1,'El empleado Santiago Donoso ha agregado el insumo LACTOSA',7,41),(183,'2021-10-25 17:38:31.380199','8','Insumo SAL FUNDENTE ST-115',1,'El empleado Santiago Donoso ha agregado el insumo SAL FUNDENTE ST-115',7,41),(184,'2021-10-25 17:41:10.229081','3','Proveedor PRINAL LTDA',1,'El proveedor PRINAL LTDA ha sido creado por el usuario Santiago Donoso',14,41),(185,'2021-10-25 17:43:42.797373','6','Orden de compra 5',1,'La orden de compra 5 ha sido solicitada el usuario Santiago Donoso',19,41),(186,'2021-10-25 17:44:07.615751','8','Insumo SAL FUNDENTE ST-115',2,'El empleado Santiago Donoso ha modificado el insumo SAL FUNDENTE ST-115',7,41),(187,'2021-10-25 17:44:26.706670','6','Orden de compra 5',2,'La orden de compra 5 ha sido Inicial por el usuario Santiago Donoso',19,41),(188,'2021-10-25 17:45:25.883174','6','Orden de compra 5',2,'La orden de compra 5 ha sido Validada por el usuario Santiago Donoso',19,41),(189,'2021-10-26 13:57:32.127353','4','Proveedor DILACO',1,'El proveedor DILACO ha sido creado por el usuario Santiago Donoso',14,41),(190,'2021-10-26 13:59:06.286432','9','Insumo CULTIVO DVS-50 R-708',1,'El empleado Santiago Donoso ha agregado el insumo CULTIVO DVS-50 R-708',7,41),(191,'2021-10-26 14:00:00.090186','10','Insumo PC SAM3 LYO10',1,'El empleado Santiago Donoso ha agregado el insumo PC SAM3 LYO10',7,41),(192,'2021-10-26 14:00:45.205782','11','Insumo R-704',1,'El empleado Santiago Donoso ha agregado el insumo R-704',7,41),(193,'2021-10-26 14:06:08.129098','12','Insumo SAL FUNDENTE 1054',1,'El empleado Santiago Donoso ha agregado el insumo SAL FUNDENTE 1054',7,41),(194,'2021-10-26 16:18:10.423668','7','Orden de compra 6',1,'La orden de compra 6 ha sido solicitada el usuario Santiago Donoso',19,41),(195,'2021-10-27 10:13:49.687830','5','Proveedor MARPLE',1,'El proveedor MARPLE ha sido creado por el usuario Santiago Donoso',14,41),(196,'2021-10-27 10:14:52.889280','13','Insumo POTE 200/95 C/TAPA',1,'El empleado Santiago Donoso ha agregado el insumo POTE 200/95 C/TAPA',7,41),(197,'2021-10-27 10:16:07.553498','8','Orden de compra 7',1,'La orden de compra 7 ha sido solicitada el usuario Santiago Donoso',19,41),(198,'2021-10-28 12:21:49.884249','14','Insumo ACIDO CITRICO',1,'El empleado Santiago Donoso ha agregado el insumo ACIDO CITRICO',7,41),(199,'2021-10-28 12:22:46.254336','9','Orden de compra 8',1,'La orden de compra 8 ha sido solicitada el usuario Santiago Donoso',19,41),(200,'2021-10-28 12:27:14.761915','4','Orden de compra 3',2,'La orden de compra 3 ha sido Recepcionada por el usuario Santiago Donoso',19,41),(201,'2021-10-28 12:28:07.490507','4','Orden de compra 3',2,'La orden de compra 3 ha sido Pagada por el usuario Santiago Donoso',19,41),(202,'2021-10-29 08:33:43.002037','9','Orden de compra 8',2,'La orden de compra 8 ha sido Validada por el usuario Santiago Donoso',19,41),(203,'2021-11-02 15:09:29.509956','7','Orden de compra 6',2,'La orden de compra 6 ha sido Validada por el usuario Deyanira Poblete',19,39),(204,'2021-11-02 15:11:03.825542','7','Orden de compra 6',2,'La orden de compra 6 ha sido Semi-Recepcionada por el usuario Deyanira Poblete',19,39),(205,'2021-11-02 15:21:53.626381','7','Orden de compra 6',2,'La orden de compra 6 ha sido Recepcionada por el usuario Deyanira Poblete',19,39),(206,'2021-11-02 15:29:04.834202','3','Orden de compra 2',3,'La orden de compra 2 ha sido rechazada por el usuario Santiago Donoso',19,41),(207,'2021-11-02 15:29:22.305172','2','Orden de compra 1',2,'La orden de compra 1 ha sido Validada por el usuario Santiago Donoso',19,41),(208,'2021-11-02 15:29:29.643853','2','Orden de compra 1',2,'La orden de compra 1 ha sido Inicial por el usuario Santiago Donoso',19,41),(209,'2021-11-02 15:29:33.980389','2','Orden de compra 1',2,'La orden de compra 1 ha sido Inicial por el usuario Santiago Donoso',19,41),(210,'2021-11-02 15:29:40.986789','3','Orden de compra 2',2,'La orden de compra 2 ha sido Recepcionada por el usuario Santiago Donoso',19,41),(211,'2021-11-02 15:29:52.118376','3','Orden de compra 2',3,'La orden de compra 2 ha sido rechazada por el usuario Santiago Donoso',19,41),(212,'2021-11-02 15:30:01.022754','2','Orden de compra 1',3,'La orden de compra 1 ha sido rechazada por el usuario Santiago Donoso',19,41),(213,'2021-11-02 15:30:15.633832','1','Orden de compra 0',3,'La orden de compra 0 ha sido rechazada por el usuario Santiago Donoso',19,41),(214,'2021-11-02 15:31:07.575302','1','Inventario Insumo Azucar - Santiago',2,'Se ha actualizado el inventario de Azucar en Santiago de manera MANUAL por el usuario Santiago Donoso',13,41),(215,'2021-11-02 15:31:34.522572','2','Inventario Insumo Almidon Snowflakes - Santiago',2,'Se ha actualizado el inventario de Almidon Snowflakes en Santiago de manera MANUAL por el usuario Santiago Donoso',13,41),(216,'2021-11-02 15:35:03.286514','8','Orden de compra 7',2,'La orden de compra 7 ha sido Validada por el usuario Santiago Donoso',19,41),(217,'2021-11-02 15:35:55.747876','6','Orden de compra 5',2,'La orden de compra 5 ha sido Recepcionada por el usuario Santiago Donoso',19,41),(218,'2021-11-02 16:21:43.213331','15','Insumo Pote 200',1,'El empleado Santiago Donoso ha agregado el insumo Pote 200',7,41),(219,'2021-11-02 16:22:14.403870','16','Insumo POTE 400',1,'El empleado Santiago Donoso ha agregado el insumo POTE 400',7,41),(220,'2021-11-02 16:22:33.915864','17','Insumo TAPA CORONA',1,'El empleado Santiago Donoso ha agregado el insumo TAPA CORONA',7,41),(221,'2021-11-02 16:28:24.168901','6','Proveedor COEXPAN',1,'El proveedor COEXPAN ha sido creado por el usuario Santiago Donoso',14,41),(222,'2021-11-02 16:48:06.487566','12','Orden de compra 11',1,'La orden de compra 11 ha sido solicitada el usuario Sebastián Valenzuela',19,1),(223,'2021-11-02 16:54:03.889391','12','Orden de compra 11',2,'La orden de compra 11 ha sido Validada por el usuario Sebastián Valenzuela',19,1),(224,'2021-11-02 16:54:28.318793','9','Orden de compra 8',3,'La orden de compra 8 ha sido eliminada por el usuario Sebastián Valenzuela',19,1),(225,'2021-11-02 16:58:13.837600','10','Orden de compra 9',3,'La orden de compra 9 ha sido eliminada por el usuario Sebastián Valenzuela',19,1),(226,'2021-11-02 16:58:18.310772','11','Orden de compra 10',3,'La orden de compra 10 ha sido eliminada por el usuario Sebastián Valenzuela',19,1),(227,'2021-11-02 16:58:22.547527','12','Orden de compra 11',3,'La orden de compra 11 ha sido eliminada por el usuario Sebastián Valenzuela',19,1),(228,'2021-11-02 16:58:35.538339','13','Orden de compra 8',1,'La orden de compra 8 ha sido solicitada el usuario Sebastián Valenzuela',19,1),(229,'2021-11-02 16:58:42.321355','13','Orden de compra 8',3,'La orden de compra 8 ha sido eliminada por el usuario Sebastián Valenzuela',19,1),(230,'2021-11-02 17:00:45.558673','14','Orden de compra 8',1,'La orden de compra 8 ha sido solicitada el usuario Santiago Donoso',19,41),(231,'2021-11-04 10:15:13.127945','18','Insumo BOTELLA + TAPA TRANSPARENTE',1,'El empleado Santiago Donoso ha agregado el insumo BOTELLA + TAPA TRANSPARENTE',7,41),(232,'2021-11-04 10:15:34.056781','19','Insumo BOTELLA + TAPA BLANCA',1,'El empleado Santiago Donoso ha agregado el insumo BOTELLA + TAPA BLANCA',7,41),(233,'2021-11-04 10:21:26.336139','7','Proveedor ABASTOPLAST',1,'El proveedor ABASTOPLAST ha sido creado por el usuario Santiago Donoso',14,41),(234,'2021-11-08 10:55:13.257366','8','Proveedor INTEGRITY',1,'El proveedor INTEGRITY ha sido creado por el usuario Santiago Donoso',14,41),(235,'2021-11-08 10:56:01.854807','20','Insumo POTE 40-12 FL * 540 UN',1,'El empleado Santiago Donoso ha agregado el insumo POTE 40-12 FL * 540 UN',7,41),(236,'2021-11-08 10:58:40.199391','15','Orden de compra 9',1,'La orden de compra 9 ha sido solicitada el usuario Santiago Donoso',19,41),(237,'2021-11-08 11:36:56.204739','9','Proveedor PRIMEC',1,'El proveedor PRIMEC ha sido creado por el usuario Santiago Donoso',14,41),(238,'2021-11-08 11:38:39.055547','21','Insumo LECHE EN POLVO',1,'El empleado Santiago Donoso ha agregado el insumo LECHE EN POLVO',7,41),(239,'2021-11-08 11:38:52.418979','22','Insumo AZUCAR',1,'El empleado Santiago Donoso ha agregado el insumo AZUCAR',7,41),(240,'2021-11-08 11:39:57.161381','21','Insumo LECHE EN POLVO DESCREMADA',2,'El empleado Santiago Donoso ha modificado el insumo LECHE EN POLVO DESCREMADA',7,41),(241,'2021-11-08 11:47:32.671649','16','Orden de compra 10',1,'La orden de compra 10 ha sido solicitada el usuario Santiago Donoso',19,41),(242,'2021-11-08 12:12:20.195827','16','Orden de compra 10',2,'La orden de compra 10 ha sido Validada por el usuario Santiago Donoso',19,41),(243,'2021-11-08 12:19:11.412053','2','Insumo Azucar',3,'El empleado Santiago Donoso ha eliminado el insumo Azucar',7,41),(244,'2021-11-08 12:19:26.748953','1','Insumo Leche en polvo descremada',3,'El empleado Santiago Donoso ha eliminado el insumo Leche en polvo descremada',7,41),(245,'2021-11-08 12:53:03.527472','23','Insumo Asusar',1,'El empleado Sebastián Valenzuela ha agregado el insumo Asusar',7,1),(246,'2021-11-08 12:53:11.751393','23','Insumo Asusar',3,'El empleado Sebastián Valenzuela ha eliminado el insumo Asusar',7,1),(247,'2021-11-09 09:23:41.454454','10','Proveedor FLORAMATIC',1,'El proveedor FLORAMATIC ha sido creado por el usuario Santiago Donoso',14,41),(248,'2021-11-09 09:27:19.633517','24','Insumo GELATINA 220-BLOOM',1,'El empleado Santiago Donoso ha agregado el insumo GELATINA 220-BLOOM',7,41),(249,'2021-11-09 09:28:35.351445','17','Orden de compra 11',1,'La orden de compra 11 ha sido solicitada el usuario Santiago Donoso',19,41),(250,'2021-11-09 10:11:54.947796','11','Proveedor DIPISA',1,'El proveedor DIPISA ha sido creado por el usuario Santiago Donoso',14,41),(251,'2021-11-09 10:17:10.954896','25','Insumo PAPEL TOALLA INTERFOLIADA',1,'El empleado Santiago Donoso ha agregado el insumo PAPEL TOALLA INTERFOLIADA',7,41),(252,'2021-11-09 10:17:35.236873','26','Insumo PAPEL TOALLA',1,'El empleado Santiago Donoso ha agregado el insumo PAPEL TOALLA',7,41),(253,'2021-11-09 10:17:57.168721','26','Insumo PAPEL TOALLA OVELLA 2X190 HS',2,'El empleado Santiago Donoso ha modificado el insumo PAPEL TOALLA OVELLA 2X190 HS',7,41),(254,'2021-11-09 10:19:34.268587','27','Insumo RESMA PAPEL',1,'El empleado Santiago Donoso ha agregado el insumo RESMA PAPEL',7,41),(255,'2021-11-09 10:20:31.562971','3','Bodega Santiago',2,'El usuario Santiago Donoso ha modificado el nombre de la bodega Santiago a Santiago',11,41),(256,'2021-11-09 10:22:17.364351','12','Proveedor DITZLER',1,'El proveedor DITZLER ha sido creado por el usuario Santiago Donoso',14,41),(257,'2021-11-09 10:23:27.881536','28','Insumo SALSA FRUTILLA',1,'El empleado Santiago Donoso ha agregado el insumo SALSA FRUTILLA',7,41),(258,'2021-11-09 10:23:47.522357','29','Insumo SALSA DURAZNO',1,'El empleado Santiago Donoso ha agregado el insumo SALSA DURAZNO',7,41),(259,'2021-11-09 10:48:15.658202','17','Orden de compra 11',2,'La orden de compra 11 ha sido Validada por el usuario Santiago Donoso',19,41),(260,'2021-11-09 16:32:28.521414','15','Orden de compra 9',2,'La orden de compra 9 ha sido Validada por el usuario Hernan Vigil',19,42),(261,'2021-11-09 17:15:28.286589','16','Orden de compra 10',2,'La orden de compra 10 ha sido Semi-Recepcionada por el usuario Santiago Donoso',19,41),(262,'2021-11-09 17:17:31.714691','16','Orden de compra 10',2,'La orden de compra 10 ha sido Semi-Recepcionada por el usuario Santiago Donoso',19,41),(263,'2021-11-09 17:38:04.552740','30','Insumo YF-L812',1,'El empleado Santiago Donoso ha agregado el insumo YF-L812',7,41),(264,'2021-11-09 17:38:31.833314','31','Insumo YO-MIX 499 LYO 250 DCU',1,'El empleado Santiago Donoso ha agregado el insumo YO-MIX 499 LYO 250 DCU',7,41),(265,'2021-11-09 17:39:34.304600','32','Insumo CHOOZIT HELV A',1,'El empleado Santiago Donoso ha agregado el insumo CHOOZIT HELV A',7,41),(266,'2021-11-09 17:40:04.780498','33','Insumo CHOOZI RA 21 LYO 125 DCU',1,'El empleado Santiago Donoso ha agregado el insumo CHOOZI RA 21 LYO 125 DCU',7,41);
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
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(40,'calidad','equipoutensiliolimpieza'),(41,'calidad','registrolimpiezaequipo'),(45,'calidad','registrolimpiezaequipohistorial'),(39,'calidad','utensiliolimpieza'),(16,'clientes','cliente'),(18,'clientes','clientelocal'),(17,'clientes','clienteproducto'),(5,'contenttypes','contenttype'),(43,'equipo','areaequipo'),(38,'equipo','equipo'),(11,'inventario','bodega'),(13,'inventario','inventarioinsumo'),(12,'inventario','inventarioproducto'),(37,'maquina','maquina'),(7,'nucleo','insumo'),(8,'nucleo','insumodirectoproducto'),(44,'nucleo','permiso'),(10,'nucleo','producto'),(9,'nucleo','rama'),(22,'ordendecompra','archivo'),(36,'ordendecompra','historicalordendecompra'),(35,'ordendecompra','historicalordendecomprainsumo'),(19,'ordendecompra','ordendecompra'),(21,'ordendecompra','ordendecomprainsumo'),(20,'ordendecompra','registro'),(23,'pauta','columna'),(24,'pauta','etapa'),(31,'pauta','historicalcolumna'),(34,'pauta','historicaletapa'),(33,'pauta','historicalingrediente'),(32,'pauta','historicalinstruccion'),(30,'pauta','historicalpauta'),(25,'pauta','ingrediente'),(26,'pauta','instruccion'),(29,'pauta','instruccioncolumna'),(27,'pauta','pauta'),(28,'pauta','pautacolumna'),(42,'perfil','perfil'),(14,'proveedores','proveedor'),(15,'proveedores','proveedorinsumo'),(6,'sessions','session');
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
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2021-08-30 18:27:12.185272'),(2,'auth','0001_initial','2021-08-30 18:27:20.424685'),(3,'admin','0001_initial','2021-08-30 18:27:22.338633'),(4,'admin','0002_logentry_remove_auto_add','2021-08-30 18:27:22.427483'),(5,'admin','0003_logentry_add_action_flag_choices','2021-08-30 18:27:22.510152'),(6,'contenttypes','0002_remove_content_type_name','2021-08-30 18:27:23.681849'),(7,'auth','0002_alter_permission_name_max_length','2021-08-30 18:27:23.856414'),(8,'auth','0003_alter_user_email_max_length','2021-08-30 18:27:24.010845'),(9,'auth','0004_alter_user_username_opts','2021-08-30 18:27:24.077328'),(10,'auth','0005_alter_user_last_login_null','2021-08-30 18:27:24.691570'),(11,'auth','0006_require_contenttypes_0002','2021-08-30 18:27:24.756057'),(12,'auth','0007_alter_validators_add_error_messages','2021-08-30 18:27:24.827194'),(13,'auth','0008_alter_user_username_max_length','2021-08-30 18:27:25.031731'),(14,'auth','0009_alter_user_last_name_max_length','2021-08-30 18:27:25.195109'),(15,'auth','0010_alter_group_name_max_length','2021-08-30 18:27:25.343235'),(16,'auth','0011_update_proxy_permissions','2021-08-30 18:27:25.413226'),(17,'auth','0012_alter_user_first_name_max_length','2021-08-30 18:27:25.609232'),(18,'nucleo','0001_initial','2021-08-30 18:27:29.730917'),(19,'clientes','0001_initial','2021-08-30 18:27:33.580863'),(20,'inventario','0001_initial','2021-08-30 18:27:38.039482'),(21,'proveedores','0001_initial','2021-08-30 18:27:40.732056'),(22,'ordendecompra','0001_initial','2021-08-30 18:27:47.867404'),(23,'pauta','0001_initial','2021-08-30 18:28:01.858877'),(24,'sessions','0001_initial','2021-08-30 18:28:02.802063'),(25,'pauta','0002_remove_instruccioncolumna_medicion','2021-08-31 09:26:10.043717'),(26,'pauta','0003_alter_pauta_options','2021-08-31 15:37:10.592995'),(27,'pauta','0004_historicalcolumna_historicalpauta','2021-08-31 15:38:10.542188'),(28,'pauta','0005_auto_20210831_1606','2021-08-31 16:06:35.331673'),(29,'ordendecompra','0002_historicalordendecompra_historicalordendecomprainsumo','2021-08-31 16:07:41.679514'),(30,'pauta','0006_auto_20210831_1703','2021-08-31 17:03:15.760967'),(31,'proveedores','0002_auto_20210901_0942','2021-09-01 09:42:23.910278'),(32,'clientes','0002_auto_20210901_1204','2021-09-01 12:04:11.105220'),(33,'inventario','0002_auto_20210901_1204','2021-09-01 12:04:11.258166'),(34,'nucleo','0002_auto_20210901_1204','2021-09-01 12:04:11.454359'),(35,'ordendecompra','0003_auto_20210901_1204','2021-09-01 12:04:11.589320'),(36,'pauta','0007_auto_20210901_1204','2021-09-01 12:04:11.719286'),(37,'proveedores','0003_auto_20210901_1204','2021-09-01 12:04:11.867057'),(38,'ordendecompra','0004_alter_archivo_options','2021-09-01 12:06:05.937182'),(39,'pauta','0008_auto_20210901_1205','2021-09-01 12:06:06.095282'),(40,'nucleo','0003_auto_20210902_0919','2021-09-02 09:19:58.138227'),(41,'inventario','0003_alter_bodega_options','2021-09-02 09:20:55.103104'),(42,'inventario','0004_alter_bodega_options','2021-09-02 09:27:55.262072'),(43,'proveedores','0004_alter_proveedorinsumo_options','2021-09-02 09:27:55.404542'),(44,'nucleo','0004_alter_insumo_options','2021-09-03 13:07:43.330925'),(45,'pauta','0009_auto_20210903_1307','2021-09-03 13:07:45.467918'),(46,'maquina','0001_initial','2021-09-03 16:41:41.777702'),(47,'equipo','0001_initial','2021-09-03 18:01:23.171592'),(48,'calidad','0001_initial','2021-09-06 09:08:07.594404'),(49,'equipo','0002_equipo_utensilios','2021-09-06 09:52:43.334547'),(50,'equipo','0003_remove_equipo_utensilios','2021-09-06 09:52:43.686683'),(51,'calidad','0002_auto_20210906_0952','2021-09-06 09:52:45.782968'),(52,'calidad','0003_registrolimpiezaequipo','2021-09-06 10:53:24.200522'),(53,'calidad','0004_auto_20210906_1055','2021-09-06 10:55:48.572243'),(54,'calidad','0005_auto_20210906_1104','2021-09-06 11:04:17.481069'),(55,'calidad','0006_auto_20210907_1002','2021-09-07 10:02:48.821665'),(56,'equipo','0004_alter_equipo_options','2021-09-07 10:02:48.977293'),(57,'calidad','0007_alter_registrolimpiezaequipo_observacion_correctiva','2021-09-07 16:37:08.506746'),(58,'clientes','0003_alter_cliente_options','2021-09-07 16:37:08.647679'),(59,'perfil','0001_initial','2021-09-07 16:37:09.736238'),(60,'perfil','0002_alter_perfil_usuario','2021-09-07 17:16:35.244465'),(61,'calidad','0008_auto_20210908_1537','2021-09-08 15:39:33.843424'),(62,'calidad','0009_auto_20210908_1538','2021-09-08 15:39:34.010109'),(63,'calidad','0010_rename_accion_correctiva_registrolimpiezaequipo_observacion_correctiva','2021-09-08 15:45:57.691001'),(64,'calidad','0011_rename_observacion_correctiva_registrolimpiezaequipo_accion_correctiva','2021-09-08 15:45:57.891679'),(65,'equipo','0005_auto_20210908_1611','2021-09-08 16:11:59.802412'),(66,'equipo','0006_auto_20210908_1629','2021-09-08 16:30:08.237089'),(67,'calidad','0012_alter_registrolimpiezaequipo_estado','2021-09-09 15:27:46.046158'),(68,'calidad','0013_alter_registrolimpiezaequipo_options','2021-09-09 15:29:20.269704'),(69,'calidad','0014_alter_utensiliolimpieza_nombre','2021-09-09 18:01:15.319921'),(70,'nucleo','0005_permiso','2021-09-09 18:01:15.904136'),(71,'calidad','0015_auto_20210910_1212','2021-09-10 12:12:21.041310'),(72,'calidad','0016_auto_20210910_1227','2021-09-10 12:27:38.811441');
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('279rve454b11z7twbdio2gs96tk29zb7','.eJxVjMsOwiAQRf-FtSEwPBpcuvcbyAAzUjWQlHZl_Hdt0oVu7znnvkTEba1xG7TEuYiz0EqcfseE-UFtJ-WO7dZl7m1d5iR3RR50yGsv9Lwc7t9BxVG_dcYMnMCQSUAugykJsmFvfYDgGCdnNYEjZOtsseg1B_Zq0kqZgp7F-wMfrjhS:1mLsfJ:pYe--2ITR6X7pxc0srJQBDmrl5wRnmiqryvOS6eHt8o','2021-09-16 15:46:25.376121'),('3b15p46rnnr7ausrn3owrze6mrexts82','.eJxVjMsOwiAUBf-FtSEtIA-X7vsN5D5AqgaS0q6M_65NutDtmZnzEhG2tcStpyXOLC5iFKffDYEeqe6A71BvTVKr6zKj3BV50C6nxul5Pdy_gwK9fGscTDqbMVhiss76zD4MlK1jHVg5rZ1VoJU3hg2HlAGt8oQIHJApKPH-AN3wOEs:1mSnzB:vBddpCiViIf0B0f2iqxWBTxNDK95NDU0HuwvhmA5cEU','2021-10-05 19:11:33.931832'),('3oore3jiunc5deffycxhlh39btwds27q','.eJxVjDsOwjAQBe_iGllre_2jpOcM1voTHEC2FCcV4u4QKQW0b2beiwXa1hq2UZYwZ3ZmyrPT7xgpPUrbSb5Tu3WeeluXOfJd4Qcd_NpzeV4O9--g0qjfmqK00lKOCbUTZtLWEChAmaKXiAhqSl6RMFAIrNRghJAOlTNeF3SCvT_s3jZ4:1mhyCn:AS-CqKy9-punoewuTwR0Rnplv6Btq-qWfKr7UhFcjk4','2021-11-16 15:08:17.672639'),('64t14rwh3fxjf1kwjlunies0xdkvec2v','.eJxVjMEOwiAQRP-FsyFi6QIevfcbCMsuUjWQlPZk_HdL0oMeJpnMm5m38GFbs98aL34mcRUKxOk3xBCfXDqhRyj3KmMt6zKj7BV50CanSvy6Hd2_gxxa7uvzYHcZBA1G2aQcaa2BHGgzDiE6tGo36ULMNoG1A6RIwIjk9JhQfL7pbzgC:1mOiWT:muEIvEP5oQUbyfOkV4YR7IoyKnsqo_MQepVjHRR9w4A','2021-09-24 12:33:01.990311'),('66kloc67737vps73z29g5aran5nku811','.eJxVjDEOwjAMRe-SGUWxwE3CyM4ZIttxSQElUtNOiLtDpQ6w_vfef5lE61LS2nVOUzZnA2AOvyOTPLRuJN-p3pqVVpd5YrspdqfdXlvW52V3_w4K9fKtEWFEDuw0KgSQGE8OI5HnnAGAxQ9uyOh9EE_MfBwJxKOCsgwUwbw_CKA4jQ:1mUqwj:AZeqH0N8kedm-rXZ8z12ehIyo3vIbULkHmKylr2OVJI','2021-10-11 10:45:29.422593'),('90yup3ky7i9lyiurwadv0zj30qbucwqt','.eJxVjMsOwiAUBf-FtSEtIA-X7vsN5D5AqgaS0q6M_65NutDtmZnzEhG2tcStpyXOLC5iFKffDYEeqe6A71BvTVKr6zKj3BV50C6nxul5Pdy_gwK9fGscTDqbMVhiss76zD4MlK1jHVg5rZ1VoJU3hg2HlAGt8oQIHJApKPH-AN3wOEs:1mO2N8:fnQmVvzSV-xOe8d9tMPBq5jXIryNTeDP0qCcSPv5TIc','2021-09-22 15:32:34.326097'),('bda1qolfasxs140jxe5q6espgs0yl7rr','.eJxVjEsOwiAUAO_C2hAof5fuewbyeDykamhS2pXx7oakC93OTObNIhx7jUenLS6ZXZma2OUXJsAntWHyA9p95bi2fVsSHwk_befzmul1O9u_QYVex9db46kQJglOOxDOeQpBFDcZ6UjIIFHpUmTCbEFDMEppAiwSfdHBss8XAkI4Gg:1mUqq0:uHFf_cyggoltl-wW4CVS1VnymvX86GcGn6JnTl36kUI','2021-10-11 10:38:32.436304'),('c1zzdzy3k1xsi9qe36fsvejnuk83spnp','.eJxVjE0OwiAYBe_C2hD-bMGl-56BPD5AqgaS0q6Md9cmXej2zcx7MY9tLX7rafFzZBdmJDv9jgH0SHUn8Y56a5xaXZc58F3hB-18ajE9r4f7d1DQy7dGJGWEFEjWaBqyRQS0FQ5kddAuuDQKgjqbZAgUnMqDhnAyg8SYwd4fJNo5CQ:1mk54K:ZhymyiA6dE1u63EJ0K_-R1_oNcjR_JMosad4yXkf0Jg','2021-11-22 10:52:16.989792'),('cg9ayf7ubdds2nj4mv0f8qy3j2h4incz','eyJfcGFzc3dvcmRfcmVzZXRfdG9rZW4iOiJhdG1xeWMtMGEzNzViMWIzYWEyOGZmMzBiZDIyMDA2NGMzMjg5YmUifQ:1mUqrx:7GwFZi8YY6yZATVeqkwW4NHa5Y7-ZdPnfayhMmbuw1I','2021-10-11 10:40:33.813653'),('cpjuab9yiktnnusp2ckrm3gvxr0wq766','.eJxVjMsOwiAQRf-FtSEwPBpcuvcbyAAzUjWQlHZl_Hdt0oVu7znnvkTEba1xG7TEuYiz0EqcfseE-UFtJ-WO7dZl7m1d5iR3RR50yGsv9Lwc7t9BxVG_dcYMnMCQSUAugykJsmFvfYDgGCdnNYEjZOtsseg1B_Zq0kqZgp7F-wMfrjhS:1mOIrU:l1t0HjRqPvpjQrNhGnisNgTXa4cNbjg278XjyRJOFuE','2021-09-23 09:09:00.628178'),('do1w5g87rtrx2js5v1mqvvy7d4pnkl8b','.eJxVjMsOwiAUBf-FtSEtIA-X7vsN5D5AqgaS0q6M_65NutDtmZnzEhG2tcStpyXOLC5iFKffDYEeqe6A71BvTVKr6zKj3BV50C6nxul5Pdy_gwK9fGscTDqbMVhiss76zD4MlK1jHVg5rZ1VoJU3hg2HlAGt8oQIHJApKPH-AN3wOEs:1mRzAT:U-zpn35VJGjxDcEvD2cQeNt7jSaF9DE2S9HdFJrgbsI','2021-10-03 12:55:49.329673'),('f5wmgjb1ddc6azo0itd420bmtpzox88w','.eJxVjDsOwjAQBe_iGlkbr_GHkj5nsBzvLg6gRIqTCnF3iJQC2jcz76VS3taatsZLGkldFHp1-h2HXB487YTuebrNuszTuoyD3hV90Kb7mfh5Pdy_g5pb_dbWBUAoCL4bAEWIDUnmKBIBWCAYZ4o3FAjt2WB0vguW2EbvMiOIen8A_543sg:1mdtw4:w81cV-LpvgUJcb8QLfjFJNZfNynigyx4IRg6YqpAFqM','2021-11-05 09:46:12.103881'),('fd1582p327egk7fyntjaa1uyk8ulogtx','.eJxVjEEOwiAQRe_C2hAoBUaX7nsGMjCDVA0kpV0Z765NutDtf-_9lwi4rSVsnZcwk7gIY8Tpd4yYHlx3QnestyZTq-syR7kr8qBdTo34eT3cv4OCvXzr0ViFxEDgdQZWTjmryJFKmjR6y5FjdtkOWjunABFM9BYyni0NzKN4fwAG0jg1:1mVEpU:WodOrfNQCw-8Bt5HfoeKsFuDf47LJwGXq4keXUdPfj0','2021-10-12 12:15:36.145207'),('gqhhmi07f9sk71d7jdv2llz68uzlexur','.eJxVjMsOwiAQRf-FtSG8B1y69xvIMIBUDU1KuzL-uzbpQrf3nHNfLOK2triNssQpszMzip1-x4T0KH0n-Y79NnOa-7pMie8KP-jg1zmX5-Vw_w4ajvati5SOgtLBWE8KnDa-FiedBUoBBDifUQtTpdZABStkENIjWW8qyqTZ-wPdgTdV:1miPAE:ID5VFUDvQx4zjIsJgUrNU3ZF_R2vQCzOU-dA4U47k0U','2021-11-17 19:55:26.412434'),('iy9tyxhvmb4k2e2u4xg6jjl6zz1ayptt','.eJxVjMEOwiAQRP-FsyGWLbB49O43NMuySNXQpLQn47_bJj3obTLvzbzVQOtShrXJPIxJXRSo028XiZ9Sd5AeVO-T5qku8xj1ruiDNn2bkryuh_t3UKiVbX22AATYYUbM5LBLIYhwD2SZ-wDWezYu9wY7D0HQCRvjOQpvIRtQny_PXTe_:1mSfTC:IVbgFPsPp-nVnfH6B2PhfSoyP2IOkA-VQzekb-9hLTo','2021-10-05 10:05:58.287001'),('iygr36lkam8wgng4plhipnh06a8woluy','.eJxVjMsOwiAUBf-FtSEtIA-X7vsN5D5AqgaS0q6M_65NutDtmZnzEhG2tcStpyXOLC5iFKffDYEeqe6A71BvTVKr6zKj3BV50C6nxul5Pdy_gwK9fGscTDqbMVhiss76zD4MlK1jHVg5rZ1VoJU3hg2HlAGt8oQIHJApKPH-AN3wOEs:1mPqwB:A74XauDhY-VwzsaBDAlD2WKIkIXEynANLwG7HLRejh0','2021-09-27 15:44:15.149809'),('kpeakjh3rylpcufiuvrkmqoqpvfxjjpe','.eJxVjDsOwjAQBe_iGlkbr_GHkj5nsBzvLg6gRIqTCnF3iJQC2jcz76VS3taatsZLGkldFHp1-h2HXB487YTuebrNuszTuoyD3hV90Kb7mfh5Pdy_g5pb_dbWBUAoCL4bAEWIDUnmKBIBWCAYZ4o3FAjt2WB0vguW2EbvMiOIen8A_543sg:1mdtyq:kffR701yak6H25wfS92eWwlizVn2O2_J6pHvHsbrhLo','2021-11-05 09:49:04.745862'),('mpmwbs2snpek5p4f9fofxx8g4yjlfiml','.eJxVjDEOwjAMRe-SGUWxwE3CyM4ZIttxSQElUtNOiLtDpQ6w_vfef5lE61LS2nVOUzZnA2AOvyOTPLRuJN-p3pqVVpd5YrspdqfdXlvW52V3_w4K9fKtEWFEDuw0KgSQGE8OI5HnnAGAxQ9uyOh9EE_MfBwJxKOCsgwUwbw_CKA4jQ:1mORCi:08G_u4iy1KRhmrRKsNooem3p5Tqs27_vGohhRV14rOo','2021-09-23 18:03:28.067576'),('n0n2amzvwd920w7odpisxkkigvpcbgqx','.eJxVjEEOwiAQAP_C2RA2sAU9evcNBNitVA0kpT0Z_y4kPeh1ZjJv4cO-Zb83Xv1C4iK0FadfGEN6chmGHqHcq0y1bOsS5UjkYZu8VeLX9Wj_Bjm0PL6oMUzREYG1eEbUmmcHrEzkWQVNCJPtGIESdBGdNayNAuAODYjPF-2SNu0:1mkRhw:5x0gN4625njavdCXlo9jdW71TUXeiOwhV60TLACCla8','2021-11-23 11:02:40.662958'),('o5pm0qw1zx4e7jjuhsijdgbtfn95r9eq','.eJxVjEEOwiAQRe_C2hAoBUaX7nsGMjCDVA0kpV0Z765NutDtf-_9lwi4rSVsnZcwk7gIY8Tpd4yYHlx3QnestyZTq-syR7kr8qBdTo34eT3cv4OCvXzr0ViFxEDgdQZWTjmryJFKmjR6y5FjdtkOWjunABFM9BYyni0NzKN4fwAG0jg1:1meGys:R6nC75IOFYLAhRrbgmZCERVpEl_fX9ES6tL6kqtSZd8','2021-11-06 10:22:38.218651'),('pohsbtf6bptn24c2peihkjrr0ubt6tzf','.eJxVjEEOwiAQRe_C2hAoBUaX7nsGMjCDVA0kpV0Z765NutDtf-_9lwi4rSVsnZcwk7gIY8Tpd4yYHlx3QnestyZTq-syR7kr8qBdTo34eT3cv4OCvXzr0ViFxEDgdQZWTjmryJFKmjR6y5FjdtkOWjunABFM9BYyni0NzKN4fwAG0jg1:1maQBw:pQDzX5YyVMjg6r_OdSV9L1S9YBd0FlBuWPuosZRhrb4','2021-10-26 19:24:12.739483'),('px0uwk4wsa7t76onnlouws4epf2k5e92','.eJxVjMsOwiAQRf-FtSEwPBpcuvcbyAAzUjWQlHZl_Hdt0oVu7znnvkTEba1xG7TEuYiz0EqcfseE-UFtJ-WO7dZl7m1d5iR3RR50yGsv9Lwc7t9BxVG_dcYMnMCQSUAugykJsmFvfYDgGCdnNYEjZOtsseg1B_Zq0kqZgp7F-wMfrjhS:1mO4Oc:Q3qKDqw3aUA3a-kZiEqIdMus8kclPKrcIRm2rX6TbV8','2021-09-22 17:42:14.206774'),('qpphabb87k2dx3np0h4h0zjiosqu4z07','.eJxVjDEOwjAMRe-SGUWxwE3CyM4ZIttxSQElUtNOiLtDpQ6w_vfef5lE61LS2nVOUzZnA2AOvyOTPLRuJN-p3pqVVpd5YrspdqfdXlvW52V3_w4K9fKtEWFEDuw0KgSQGE8OI5HnnAGAxQ9uyOh9EE_MfBwJxKOCsgwUwbw_CKA4jQ:1mMGr8:5IBXS4buPUc6-4xvYiK9Ym1t7Z-3ClGBA1xDHQ6iTtY','2021-09-17 17:36:14.914468'),('qwfqrk3ys90btr359kq8hay63zb5z2b9','.eJxVjMsOwiAUBf-FtSEtIA-X7vsN5D5AqgaS0q6M_65NutDtmZnzEhG2tcStpyXOLC5iFKffDYEeqe6A71BvTVKr6zKj3BV50C6nxul5Pdy_gwK9fGscTDqbMVhiss76zD4MlK1jHVg5rZ1VoJU3hg2HlAGt8oQIHJApKPH-AN3wOEs:1mk5tE:AOf8_gs5_VR5naU5X3eNezmpH9E8g9YZj4lgWnYbUcc','2021-11-22 11:44:52.239580'),('s4x93wiegrllvflo3n90nzcbrr7v2q2q','.eJxVjDEOwjAMRe-SGUWxwE3CyM4ZIttxSQElUtNOiLtDpQ6w_vfef5lE61LS2nVOUzZnA2AOvyOTPLRuJN-p3pqVVpd5YrspdqfdXlvW52V3_w4K9fKtEWFEDuw0KgSQGE8OI5HnnAGAxQ9uyOh9EE_MfBwJxKOCsgwUwbw_CKA4jQ:1mPlYA:KmXnp3O_G884j94JTBJbylBYdmwtvW7qFYvvtu3Idy0','2021-09-27 09:59:06.121814'),('t6acacnvw8ndm3pimfj6hxoahe7mr4cj','.eJxVjEEOwiAQRe_C2hAoBUaX7nsGMjCDVA0kpV0Z765NutDtf-_9lwi4rSVsnZcwk7gIY8Tpd4yYHlx3QnestyZTq-syR7kr8qBdTo34eT3cv4OCvXzr0ViFxEDgdQZWTjmryJFKmjR6y5FjdtkOWjunABFM9BYyni0NzKN4fwAG0jg1:1mkTcm:syJF4aj7sFlkqsu7MsVd00s3Bt-iTA8pLcoaSZ4uR-w','2021-11-23 13:05:28.006739'),('woernbba4caid0emrdef2gfxwzu6369y','.eJxVjMsOwiAUBf-FtSEtIA-X7vsN5D5AqgaS0q6M_65NutDtmZnzEhG2tcStpyXOLC5iFKffDYEeqe6A71BvTVKr6zKj3BV50C6nxul5Pdy_gwK9fGscTDqbMVhiss76zD4MlK1jHVg5rZ1VoJU3hg2HlAGt8oQIHJApKPH-AN3wOEs:1mPkus:9t-STWrNsgJRmkE7ca7fo54P-8c4X32BxiRlG-UejQA','2021-09-27 09:18:30.220811'),('wp2ql7t0t3pfd4uo91uj5htm8h9toues','.eJxVjDsOwjAQBe_iGlkbr_GHkj5nsBzvLg6gRIqTCnF3iJQC2jcz76VS3taatsZLGkldFHp1-h2HXB487YTuebrNuszTuoyD3hV90Kb7mfh5Pdy_g5pb_dbWBUAoCL4bAEWIDUnmKBIBWCAYZ4o3FAjt2WB0vguW2EbvMiOIen8A_543sg:1mdI4t:HZwADuNliItqsSYqiQ1Ke1e2-OkuIR-B_CbOLZ5tNfc','2021-11-03 17:20:47.444954'),('xnl7w7zoqvfvws6ct96a646umb3ivk75','.eJxVjDkOwjAURO_iGll2bLxQ0nMG62_BAZRIcVIh7k4ipYBuNO_NvFWBdallbTKXgdVF-U6dfksEesq4E37AeJ80TeMyD6h3RR-06dvE8roe7t9BhVa3NQlHyD0ZycGaSOQ9SjCWfYec4xYRosspeCfOgMg5JbLMaNhh6nr1-QIl8TjF:1mkWfq:a9DH4QGGbDfsptx5_nSMAhCZzxIbAMQOZY_E6gPV7tQ','2021-11-23 16:20:50.498455'),('yxje0dovlbeu98hd8sdyr0wydrlcx5ml','.eJxVjMsOgjAUBf-la9NQWi7FpXu_gdxXLWpKQmFl_HclYaHbMzPnZUbc1jxuVZdxEnM2wZnT70jIDy07kTuW22x5Lusykd0Ve9Bqr7Po83K4fwcZa_7WgyROQi5Bx-h8AG4FNGhL2sfoQ8fap8ZjQ010EJgBkgBhJKJBfDDvDzVrOSU:1mdtQI:EH6ANp7gxh8HzaZjP0OU8KdkU5vD4qtMLs4TOB9PHbQ','2021-11-05 09:13:22.917566'),('zkip2z8tsyj4gjbtjddxs9rv45fyk6dd','.eJxVjEEOwiAQRe_C2hBkwFKX7j0DmRkGqRpISrsy3l2bdKHb_977LxVxXUpcu8xxSuqswKnD70jID6kbSXest6a51WWeSG-K3mnX15bkedndv4OCvXzrIYMJDh1mCyF5ySR0HNCC9ZlOIzMS8MgByJmcvHGJRSSAz8Ao4tT7Ayw_OYE:1mbNZV:uQBI8uq9bX2DqzFwT5x4uhd8INGfooUp2n-R3tHi5p4','2021-10-29 10:48:29.693733');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `equipo_areaequipo`
--

DROP TABLE IF EXISTS `equipo_areaequipo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `equipo_areaequipo` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `lugar_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`),
  KEY `equipo_areaequipo_lugar_id_4d98739e_fk_inventario_bodega_id` (`lugar_id`),
  CONSTRAINT `equipo_areaequipo_lugar_id_4d98739e_fk_inventario_bodega_id` FOREIGN KEY (`lugar_id`) REFERENCES `inventario_bodega` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `equipo_areaequipo`
--

LOCK TABLES `equipo_areaequipo` WRITE;
/*!40000 ALTER TABLE `equipo_areaequipo` DISABLE KEYS */;
INSERT INTO `equipo_areaequipo` VALUES (3,'Sala De Jamon','2021-09-08 16:38:54.144354','2021-09-08 16:38:54.411130',2),(4,'Santiago','2021-09-09 15:58:22.851556','2021-09-09 15:58:22.911222',3),(6,'Sala de yogurt','2021-09-22 12:28:58.400603','2021-09-22 12:29:26.575915',4);
/*!40000 ALTER TABLE `equipo_areaequipo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `equipo_equipo`
--

DROP TABLE IF EXISTS `equipo_equipo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `equipo_equipo` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `area_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `equipo_equipo_area_id_f99ccdad_fk_equipo_areaequipo_id` (`area_id`),
  CONSTRAINT `equipo_equipo_area_id_f99ccdad_fk_equipo_areaequipo_id` FOREIGN KEY (`area_id`) REFERENCES `equipo_areaequipo` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `equipo_equipo`
--

LOCK TABLES `equipo_equipo` WRITE;
/*!40000 ALTER TABLE `equipo_equipo` DISABLE KEYS */;
INSERT INTO `equipo_equipo` VALUES (1,'Maquina de Queso','2021-09-03 18:02:35.571316','2021-09-08 16:39:06.197074',3),(2,'Maquina de Quesos','2021-09-07 11:35:17.845441','2021-09-08 16:40:51.617979',NULL),(4,'Tanque de yogurt','2021-09-22 12:29:52.830105','2021-09-22 12:29:52.838386',6);
/*!40000 ALTER TABLE `equipo_equipo` ENABLE KEYS */;
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
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventario_bodega`
--

LOCK TABLES `inventario_bodega` WRITE;
/*!40000 ALTER TABLE `inventario_bodega` DISABLE KEYS */;
INSERT INTO `inventario_bodega` VALUES (2,'San Felipe','2021-09-01 15:16:59.530687','2021-09-01 15:16:59.530717'),(3,'Santiago','2021-09-07 10:00:33.450011','2021-11-09 10:20:31.556586'),(4,'Valdivia','2021-09-09 15:44:21.678512','2021-09-09 15:44:21.678534');
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
  `estado` varchar(20) NOT NULL,
  `cantidad` bigint NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `bodega_id` bigint NOT NULL,
  `insumo_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `inventario_inventarioinsumo_bodega_id_insumo_id_8861ccbc_uniq` (`bodega_id`,`insumo_id`),
  KEY `inventario_inventari_insumo_id_23f7b56d_fk_nucleo_in` (`insumo_id`),
  CONSTRAINT `inventario_inventari_bodega_id_292ee580_fk_inventari` FOREIGN KEY (`bodega_id`) REFERENCES `inventario_bodega` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `inventario_inventari_insumo_id_23f7b56d_fk_nucleo_in` FOREIGN KEY (`insumo_id`) REFERENCES `nucleo_insumo` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventario_inventarioinsumo`
--

LOCK TABLES `inventario_inventarioinsumo` WRITE;
/*!40000 ALTER TABLE `inventario_inventarioinsumo` DISABLE KEYS */;
INSERT INTO `inventario_inventarioinsumo` VALUES (2,'Peligro',50,'2021-10-28 12:27:13.570679','2021-11-02 15:31:33.279777',3,3),(3,'Bien',25,'2021-11-02 15:11:01.003141','2021-11-02 15:21:53.614066',3,12),(4,'Bien',25,'2021-11-02 15:35:52.861948','2021-11-02 15:35:54.364532',3,8),(5,'Bien',625,'2021-11-02 15:35:54.369535','2021-11-02 15:35:55.737103',3,7),(6,'Bien',150,'2021-11-09 17:15:26.091786','2021-11-09 17:17:31.693833',3,21),(7,'Bien',100,'2021-11-09 17:15:27.175871','2021-11-09 17:17:31.704845',3,22);
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
  CONSTRAINT `inventario_inventari_bodega_id_6ba7a20d_fk_inventari` FOREIGN KEY (`bodega_id`) REFERENCES `inventario_bodega` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `inventario_inventari_producto_id_76404bef_fk_nucleo_pr` FOREIGN KEY (`producto_id`) REFERENCES `nucleo_producto` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nucleo_insumo`
--

LOCK TABLES `nucleo_insumo` WRITE;
/*!40000 ALTER TABLE `nucleo_insumo` DISABLE KEYS */;
INSERT INTO `nucleo_insumo` VALUES (3,'Almidon Snowflakes','Kilogramo',50,'2021-10-22 09:14:08.694237','2021-10-22 09:14:08.698871'),(4,'Proteina de Haba','Kilogramo',75,'2021-10-22 10:27:17.597743','2021-10-22 10:27:17.602108'),(5,'N-Dulge','Kilogramo',50,'2021-10-22 10:27:38.388089','2021-10-22 10:27:38.391302'),(6,'Bolsa Vacio 160x200x80 micras','Unidad',10000,'2021-10-25 17:21:48.728507','2021-10-25 17:21:48.734286'),(7,'LACTOSA','Kilogramo',10,'2021-10-25 17:38:11.408050','2021-10-25 17:38:11.412223'),(8,'SAL FUNDENTE ST-115','Kilogramo',5,'2021-10-25 17:38:31.377433','2021-10-25 17:44:07.617379'),(9,'CULTIVO DVS-50 R-708','Unidad',8,'2021-10-26 13:59:06.284277','2021-10-26 13:59:06.287680'),(10,'PC SAM3 LYO10','Unidad',10,'2021-10-26 14:00:00.087868','2021-10-26 14:00:00.091623'),(11,'R-704','Unidad',10,'2021-10-26 14:00:45.203340','2021-10-26 14:00:45.207029'),(12,'SAL FUNDENTE 1054','Kilogramo',10,'2021-10-26 14:06:08.126953','2021-10-26 14:06:08.131170'),(13,'POTE 200/95 C/TAPA','Unidad',3000,'2021-10-27 10:14:52.886420','2021-10-27 10:14:52.890765'),(14,'ACIDO CITRICO','Kilogramo',10,'2021-10-28 12:21:49.879362','2021-10-28 12:21:49.885907'),(15,'Pote 200','Unidad',20000,'2021-11-02 16:21:43.210258','2021-11-02 16:21:43.214476'),(16,'POTE 400','Unidad',8000,'2021-11-02 16:22:14.402048','2021-11-02 16:22:14.405634'),(17,'TAPA CORONA','Unidad',25000,'2021-11-02 16:22:33.912460','2021-11-02 16:22:33.917750'),(18,'BOTELLA + TAPA TRANSPARENTE','Unidad',700,'2021-11-04 10:15:13.122843','2021-11-04 10:15:13.130185'),(19,'BOTELLA + TAPA BLANCA','Unidad',700,'2021-11-04 10:15:34.054883','2021-11-04 10:15:34.058375'),(20,'POTE 40-12 FL * 540 UN','Unidad',5000,'2021-11-08 10:56:01.851915','2021-11-08 10:56:01.856850'),(21,'LECHE EN POLVO DESCREMADA','Kilogramo',75,'2021-11-08 11:38:39.051909','2021-11-08 11:39:57.165123'),(22,'AZUCAR','Kilogramo',50,'2021-11-08 11:38:52.416875','2021-11-08 11:38:52.420746'),(24,'GELATINA 220-BLOOM','Kilogramo',5,'2021-11-09 09:27:19.630602','2021-11-09 09:27:19.630625'),(25,'PAPEL TOALLA INTERFOLIADA','Unidad',3,'2021-11-09 10:17:10.953332','2021-11-09 10:17:10.953357'),(26,'PAPEL TOALLA OVELLA 2X190 HS','Unidad',4,'2021-11-09 10:17:35.233369','2021-11-09 10:17:57.161619'),(27,'RESMA PAPEL','Unidad',2,'2021-11-09 10:19:34.266799','2021-11-09 10:19:34.266824'),(28,'SALSA FRUTILLA','Kilogramo',400,'2021-11-09 10:23:27.879616','2021-11-09 10:23:27.879636'),(29,'SALSA DURAZNO','Kilogramo',400,'2021-11-09 10:23:47.520511','2021-11-09 10:23:47.520544'),(30,'YF-L812','Unidad',4,'2021-11-09 17:38:04.549458','2021-11-09 17:38:04.549480'),(31,'YO-MIX 499 LYO 250 DCU','Unidad',5,'2021-11-09 17:38:31.831463','2021-11-09 17:38:31.831486'),(32,'CHOOZIT HELV A','Unidad',5,'2021-11-09 17:39:34.303039','2021-11-09 17:39:34.303061'),(33,'CHOOZI RA 21 LYO 125 DCU','Unidad',5,'2021-11-09 17:40:04.778521','2021-11-09 17:40:04.778549');
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
  CONSTRAINT `nucleo_insumodirecto_insumo_id_f737fb29_fk_nucleo_in` FOREIGN KEY (`insumo_id`) REFERENCES `nucleo_insumo` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `nucleo_insumodirecto_producto_id_a10036ad_fk_nucleo_pr` FOREIGN KEY (`producto_id`) REFERENCES `nucleo_producto` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nucleo_insumodirectoproducto`
--

LOCK TABLES `nucleo_insumodirectoproducto` WRITE;
/*!40000 ALTER TABLE `nucleo_insumodirectoproducto` DISABLE KEYS */;
/*!40000 ALTER TABLE `nucleo_insumodirectoproducto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nucleo_permiso`
--

DROP TABLE IF EXISTS `nucleo_permiso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nucleo_permiso` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nucleo_permiso`
--

LOCK TABLES `nucleo_permiso` WRITE;
/*!40000 ALTER TABLE `nucleo_permiso` DISABLE KEYS */;
/*!40000 ALTER TABLE `nucleo_permiso` ENABLE KEYS */;
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
  CONSTRAINT `nucleo_producto_rama_id_dd0cef14_fk_nucleo_rama_id` FOREIGN KEY (`rama_id`) REFERENCES `nucleo_rama` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nucleo_producto`
--

LOCK TABLES `nucleo_producto` WRITE;
/*!40000 ALTER TABLE `nucleo_producto` DISABLE KEYS */;
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
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nucleo_rama`
--

LOCK TABLES `nucleo_rama` WRITE;
/*!40000 ALTER TABLE `nucleo_rama` DISABLE KEYS */;
INSERT INTO `nucleo_rama` VALUES (3,'Queso CamBri','2021-09-02 15:53:08.949005','2021-09-02 15:53:09.032130');
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
  CONSTRAINT `ordendecompra_archiv_orden_id_d3f7e4af_fk_ordendeco` FOREIGN KEY (`orden_id`) REFERENCES `ordendecompra_ordendecompra` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ordendecompra_archivo`
--

LOCK TABLES `ordendecompra_archivo` WRITE;
/*!40000 ALTER TABLE `ordendecompra_archivo` DISABLE KEYS */;
/*!40000 ALTER TABLE `ordendecompra_archivo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ordendecompra_historicalordendecompra`
--

DROP TABLE IF EXISTS `ordendecompra_historicalordendecompra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ordendecompra_historicalordendecompra` (
  `id` bigint NOT NULL,
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
  `history_id` int NOT NULL AUTO_INCREMENT,
  `history_date` datetime(6) NOT NULL,
  `history_change_reason` varchar(100) DEFAULT NULL,
  `history_type` varchar(1) NOT NULL,
  `bodega_id` bigint DEFAULT NULL,
  `history_user_id` int DEFAULT NULL,
  `proveedor_id` bigint DEFAULT NULL,
  PRIMARY KEY (`history_id`),
  KEY `ordendecompra_histor_history_user_id_7ec07ab8_fk_auth_user` (`history_user_id`),
  KEY `ordendecompra_historicalordendecompra_id_ffd280a2` (`id`),
  KEY `ordendecompra_historicalordendecompra_numero_9c95a5b3` (`numero`),
  KEY `ordendecompra_historicalordendecompra_bodega_id_272082f3` (`bodega_id`),
  KEY `ordendecompra_historicalordendecompra_proveedor_id_9ee6cacb` (`proveedor_id`),
  CONSTRAINT `ordendecompra_histor_history_user_id_7ec07ab8_fk_auth_user` FOREIGN KEY (`history_user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=85 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ordendecompra_historicalordendecompra`
--

LOCK TABLES `ordendecompra_historicalordendecompra` WRITE;
/*!40000 ALTER TABLE `ordendecompra_historicalordendecompra` DISABLE KEYS */;
INSERT INTO `ordendecompra_historicalordendecompra` VALUES (1,0,'','Inicial','2021-08-31',15000,NULL,NULL,NULL,NULL,NULL,NULL,'2021-08-31 10:01:56.413968','2021-08-31 16:09:10.713201',1,'2021-08-31 16:09:10.738841',NULL,'~',1,1,1),(1,0,'','Validada','2021-08-31',22500,NULL,NULL,NULL,NULL,NULL,NULL,'2021-08-31 10:01:56.413968','2021-08-31 16:09:10.890022',2,'2021-08-31 16:09:10.905937',NULL,'~',1,1,1),(1,0,'','Inicial','2021-08-31',22500,NULL,NULL,NULL,NULL,NULL,NULL,'2021-08-31 10:01:56.413968','2021-08-31 16:09:37.171460',3,'2021-08-31 16:09:37.196334',NULL,'~',1,1,1),(1,0,'','Inicial','2021-08-31',22500,NULL,NULL,NULL,NULL,NULL,NULL,'2021-08-31 10:01:56.413968','2021-08-31 16:09:55.684224',4,'2021-08-31 16:09:55.705133',NULL,'~',1,1,1),(1,0,'','Validada','2021-08-31',22500,NULL,NULL,NULL,NULL,NULL,NULL,'2021-08-31 10:01:56.413968','2021-08-31 16:09:55.854878',5,'2021-08-31 16:09:55.870970',NULL,'~',1,1,1),(2,1,'','Inicial','2021-09-07',0,NULL,NULL,NULL,NULL,NULL,NULL,'2021-09-07 11:53:09.528700','2021-09-07 11:53:09.528718',6,'2021-09-07 11:53:09.688995',NULL,'+',3,1,1),(2,1,'','Inicial','2021-09-07',3750,NULL,NULL,NULL,NULL,NULL,NULL,'2021-09-07 11:53:09.528700','2021-09-07 11:53:22.016285',7,'2021-09-07 11:53:22.037572',NULL,'~',3,1,1),(2,1,'','Inicial','2021-09-07',3750,NULL,NULL,NULL,NULL,NULL,NULL,'2021-09-07 11:53:09.528700','2021-09-07 11:53:26.340472',8,'2021-09-07 11:53:26.362847',NULL,'~',3,1,1),(2,1,'','Validada','2021-09-07',3750,NULL,NULL,NULL,NULL,NULL,NULL,'2021-09-07 11:53:09.528700','2021-09-07 11:53:26.504562',9,'2021-09-07 11:53:26.562499',NULL,'~',3,1,1),(2,1,'','Validada','2021-09-07',3750,NULL,'123','2021-09-07',NULL,NULL,NULL,'2021-09-07 11:53:09.528700','2021-09-07 11:53:33.022461',10,'2021-09-07 11:53:33.086773',NULL,'~',3,1,1),(2,1,'','Recepcionada','2021-09-07',3750,NULL,'123','2021-09-07',NULL,NULL,NULL,'2021-09-07 11:53:09.528700','2021-09-07 11:53:44.689903',11,'2021-09-07 11:53:44.713096',NULL,'~',3,1,1),(3,2,'','Inicial','2021-09-21',0,NULL,NULL,NULL,NULL,NULL,NULL,'2021-09-21 19:12:30.331166','2021-09-21 19:12:30.331188',12,'2021-09-21 19:12:30.335723',NULL,'+',3,1,1),(3,2,'','Inicial','2021-09-21',7500,NULL,NULL,NULL,NULL,NULL,NULL,'2021-09-21 19:12:30.331166','2021-09-21 19:12:31.351649',13,'2021-09-21 19:12:31.395493',NULL,'~',3,1,1),(3,2,'','Inicial','2021-09-21',7500,NULL,NULL,NULL,NULL,NULL,NULL,'2021-09-21 19:12:30.331166','2021-09-21 19:12:42.459297',14,'2021-09-21 19:12:42.461335',NULL,'~',3,1,1),(3,2,'','Validada','2021-09-21',7500,NULL,NULL,NULL,NULL,NULL,NULL,'2021-09-21 19:12:30.331166','2021-09-21 19:12:42.482280',15,'2021-09-21 19:12:42.486163',NULL,'~',3,1,1),(3,2,'','Validada','2021-09-21',7500,NULL,'679','2021-09-21',NULL,NULL,NULL,'2021-09-21 19:12:30.331166','2021-09-21 19:13:03.895620',16,'2021-09-21 19:13:03.898551',NULL,'~',3,1,1),(3,2,'','Recepcionada','2021-09-21',7500,NULL,'679','2021-09-21',NULL,NULL,NULL,'2021-09-21 19:12:30.331166','2021-09-21 19:13:03.915655',17,'2021-09-21 19:13:03.917742',NULL,'~',3,1,1),(4,3,'Favor incluir siguiente código en factura: CORFO\r\n19IR-LR-121872','Inicial','2021-10-22',0,NULL,NULL,NULL,NULL,NULL,NULL,'2021-10-22 10:12:54.960601','2021-10-22 10:12:54.960616',18,'2021-10-22 10:12:54.962716',NULL,'+',3,41,1),(4,3,'Favor incluir siguiente código en factura: CORFO\r\n19IR-LR-121872','Inicial','2021-10-22',140000,NULL,NULL,NULL,NULL,NULL,NULL,'2021-10-22 10:12:54.960601','2021-10-22 10:12:56.575545',19,'2021-10-22 10:12:56.577733',NULL,'~',3,41,1),(4,3,'Favor incluir siguiente código en factura: CORFO\r\n19IR-LR-121872','Inicial','2021-10-22',140000,NULL,NULL,NULL,NULL,NULL,NULL,'2021-10-22 10:12:54.960601','2021-10-22 10:19:44.553319',20,'2021-10-22 10:19:44.555057',NULL,'~',3,41,1),(4,3,'Favor incluir siguiente código en factura: CORFO\r\n19IR-LR-121872','Validada','2021-10-22',140000,NULL,NULL,NULL,NULL,NULL,NULL,'2021-10-22 10:12:54.960601','2021-10-22 10:19:44.564124',21,'2021-10-22 10:19:44.565551',NULL,'~',3,41,1),(4,3,'Favor incluir siguiente código en factura: CORFO\r\n19IR-LR-121872','Rechazada','2021-10-22',140000,NULL,NULL,NULL,NULL,NULL,NULL,'2021-10-22 10:12:54.960601','2021-10-22 10:20:18.468274',22,'2021-10-22 10:20:18.470296',NULL,'~',3,41,1),(4,3,'Favor incluir siguiente código en factura: CORFO\r\n19IR-LR-121872','Validada','2021-10-22',140000,NULL,NULL,NULL,NULL,NULL,NULL,'2021-10-22 10:12:54.960601','2021-10-22 10:20:35.224708',23,'2021-10-22 10:20:35.226533',NULL,'~',3,41,1),(5,4,'Por favor incluir la siguiente glosa en la factura: DESARROLLO\r\nDE PORTAFOLIO DE POSTRES VEGETALES A BASE DE\r\nALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código\r\n19IR-LR-121872','Inicial','2021-10-25',0,NULL,NULL,NULL,NULL,NULL,NULL,'2021-10-25 17:25:00.654670','2021-10-25 17:25:00.654687',24,'2021-10-25 17:25:00.657760',NULL,'+',3,41,2),(5,4,'Por favor incluir la siguiente glosa en la factura: DESARROLLO\r\nDE PORTAFOLIO DE POSTRES VEGETALES A BASE DE\r\nALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código\r\n19IR-LR-121872','Inicial','2021-10-25',540000,NULL,NULL,NULL,NULL,NULL,NULL,'2021-10-25 17:25:00.654670','2021-10-25 17:25:02.706667',25,'2021-10-25 17:25:02.709348',NULL,'~',3,41,2),(6,5,'Por favor incluir la siguiente glosa en la factura: DESARROLLO\r\nDE PORTAFOLIO DE POSTRES VEGETALES A BASE DE\r\nALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código\r\n19IR-LR-121872','Inicial','2021-10-25',0,NULL,NULL,NULL,NULL,NULL,NULL,'2021-10-25 17:43:41.294093','2021-10-25 17:43:41.294108',26,'2021-10-25 17:43:41.295798',NULL,'+',3,41,3),(6,5,'Por favor incluir la siguiente glosa en la factura: DESARROLLO\r\nDE PORTAFOLIO DE POSTRES VEGETALES A BASE DE\r\nALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código\r\n19IR-LR-121872','Inicial','2021-10-25',110325,NULL,NULL,NULL,NULL,NULL,NULL,'2021-10-25 17:43:41.294093','2021-10-25 17:43:42.791796',27,'2021-10-25 17:43:42.795277',NULL,'~',3,41,3),(6,5,'Por favor incluir la siguiente glosa en la factura: DESARROLLO\r\nDE PORTAFOLIO DE POSTRES VEGETALES A BASE DE\r\nALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código\r\n19IR-LR-121872','Inicial','2021-10-25',110325,NULL,NULL,NULL,NULL,NULL,NULL,'2021-10-25 17:43:41.294093','2021-10-25 17:45:25.863971',28,'2021-10-25 17:45:25.865662',NULL,'~',3,41,3),(6,5,'Por favor incluir la siguiente glosa en la factura: DESARROLLO\r\nDE PORTAFOLIO DE POSTRES VEGETALES A BASE DE\r\nALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código\r\n19IR-LR-121872','Validada','2021-10-25',110325,NULL,NULL,NULL,NULL,NULL,NULL,'2021-10-25 17:43:41.294093','2021-10-25 17:45:25.878525',29,'2021-10-25 17:45:25.880091',NULL,'~',3,41,3),(7,6,'','Inicial','2021-10-26',0,NULL,NULL,NULL,NULL,NULL,NULL,'2021-10-26 16:18:08.942939','2021-10-26 16:18:08.942959',30,'2021-10-26 16:18:08.946139',NULL,'+',3,41,3),(7,6,'','Inicial','2021-10-26',137500,NULL,NULL,NULL,NULL,NULL,NULL,'2021-10-26 16:18:08.942939','2021-10-26 16:18:10.419897',31,'2021-10-26 16:18:10.422031',NULL,'~',3,41,3),(8,7,'Por favor incluir la siguiente glosa en la factura: DESARROLLO DE PORTAFOLIO DE POSTRES VEGETALES A BASE DE ALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código 19IR-LR-121872','Inicial','2021-10-27',0,NULL,NULL,NULL,NULL,NULL,NULL,'2021-10-27 10:16:05.452138','2021-10-27 10:16:05.452163',32,'2021-10-27 10:16:05.454197',NULL,'+',3,41,5),(8,7,'Por favor incluir la siguiente glosa en la factura: DESARROLLO DE PORTAFOLIO DE POSTRES VEGETALES A BASE DE ALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código 19IR-LR-121872','Inicial','2021-10-27',478800,NULL,NULL,NULL,NULL,NULL,NULL,'2021-10-27 10:16:05.452138','2021-10-27 10:16:07.546809',33,'2021-10-27 10:16:07.549960',NULL,'~',3,41,5),(9,8,'Por favor incluir la siguiente glosa en la factura: DESARROLLO DE PORTAFOLIO DE POSTRES VEGETALES A BASE DE ALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código 19IR-LR-121872','Inicial','2021-10-28',0,NULL,NULL,NULL,NULL,NULL,NULL,'2021-10-28 12:22:44.476260','2021-10-28 12:22:44.476273',34,'2021-10-28 12:22:44.479421',NULL,'+',3,41,3),(9,8,'Por favor incluir la siguiente glosa en la factura: DESARROLLO DE PORTAFOLIO DE POSTRES VEGETALES A BASE DE ALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código 19IR-LR-121872','Inicial','2021-10-28',33750,NULL,NULL,NULL,NULL,NULL,NULL,'2021-10-28 12:22:44.476260','2021-10-28 12:22:46.248093',35,'2021-10-28 12:22:46.250810',NULL,'~',3,41,3),(4,3,'Favor incluir siguiente código en factura: CORFO\r\n19IR-LR-121872','Validada','2021-10-22',140000,NULL,'67689','2021-10-28',NULL,NULL,NULL,'2021-10-22 10:12:54.960601','2021-10-28 12:27:13.561293',36,'2021-10-28 12:27:13.563074',NULL,'~',3,41,1),(4,3,'Favor incluir siguiente código en factura: CORFO\r\n19IR-LR-121872','Recepcionada','2021-10-22',140000,NULL,'67689','2021-10-28',NULL,NULL,NULL,'2021-10-22 10:12:54.960601','2021-10-28 12:27:14.758518',37,'2021-10-28 12:27:14.760317',NULL,'~',3,41,1),(4,3,'Favor incluir siguiente código en factura: CORFO\r\n19IR-LR-121872','Recepcionada','2021-10-22',140000,NULL,'67689','2021-10-28','2021-10-26','2021-10-28','transferencia','2021-10-22 10:12:54.960601','2021-10-28 12:28:07.476108',38,'2021-10-28 12:28:07.478586',NULL,'~',3,41,1),(4,3,'Favor incluir siguiente código en factura: CORFO\r\n19IR-LR-121872','Pagada','2021-10-22',140000,NULL,'67689','2021-10-28','2021-10-26','2021-10-28','transferencia','2021-10-22 10:12:54.960601','2021-10-28 12:28:07.482643',39,'2021-10-28 12:28:07.485372',NULL,'~',3,41,1),(9,8,'Por favor incluir la siguiente glosa en la factura: DESARROLLO DE PORTAFOLIO DE POSTRES VEGETALES A BASE DE ALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código 19IR-LR-121872','Inicial','2021-10-28',33750,NULL,NULL,NULL,NULL,NULL,NULL,'2021-10-28 12:22:44.476260','2021-10-29 08:33:42.977628',40,'2021-10-29 08:33:42.980787',NULL,'~',3,41,3),(9,8,'Por favor incluir la siguiente glosa en la factura: DESARROLLO DE PORTAFOLIO DE POSTRES VEGETALES A BASE DE ALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código 19IR-LR-121872','Validada','2021-10-28',58750,NULL,NULL,NULL,NULL,NULL,NULL,'2021-10-28 12:22:44.476260','2021-10-29 08:33:42.997161',41,'2021-10-29 08:33:42.999143',NULL,'~',3,41,3),(7,6,'','Inicial','2021-10-26',137500,NULL,NULL,NULL,NULL,NULL,NULL,'2021-10-26 16:18:08.942939','2021-11-02 15:09:29.489600',42,'2021-11-02 15:09:29.491940',NULL,'~',3,39,3),(7,6,'','Validada','2021-10-26',137500,NULL,NULL,NULL,NULL,NULL,NULL,'2021-10-26 16:18:08.942939','2021-11-02 15:09:29.504858',43,'2021-11-02 15:09:29.506329',NULL,'~',3,39,3),(7,6,'','Semi-Recepcionada','2021-10-26',137500,NULL,'284506','2021-11-02',NULL,NULL,NULL,'2021-10-26 16:18:08.942939','2021-11-02 15:11:03.821116',44,'2021-11-02 15:11:03.823118',NULL,'~',3,39,3),(7,6,'','Recepcionada','2021-10-26',137500,NULL,'284506','2021-11-02',NULL,NULL,NULL,'2021-10-26 16:18:08.942939','2021-11-02 15:21:53.621376',45,'2021-11-02 15:21:53.623275',NULL,'~',3,39,3),(3,2,'','Rechazada','2021-09-21',7500,NULL,'679','2021-09-21',NULL,NULL,NULL,'2021-09-21 19:12:30.331166','2021-11-02 15:29:04.837412',46,'2021-11-02 15:29:04.843353',NULL,'~',3,41,1),(2,1,'','Validada','2021-09-07',3750,NULL,'123','2021-09-07',NULL,NULL,NULL,'2021-09-07 11:53:09.528700','2021-11-02 15:29:22.297381',47,'2021-11-02 15:29:22.300297',NULL,'~',3,41,1),(2,1,'','Inicial','2021-09-07',3750,NULL,'123','2021-09-07',NULL,NULL,NULL,'2021-09-07 11:53:09.528700','2021-11-02 15:29:28.062879',48,'2021-11-02 15:29:28.065564',NULL,'~',3,41,1),(3,2,'','Recepcionada','2021-09-21',7500,NULL,'679','2021-09-21',NULL,NULL,NULL,'2021-09-21 19:12:30.331166','2021-11-02 15:29:40.979972',49,'2021-11-02 15:29:40.982786',NULL,'~',3,41,1),(3,2,'','Rechazada','2021-09-21',7500,NULL,'679','2021-09-21',NULL,NULL,NULL,'2021-09-21 19:12:30.331166','2021-11-02 15:29:52.120504',50,'2021-11-02 15:29:52.122212',NULL,'~',3,41,1),(2,1,'','Rechazada','2021-09-07',3750,NULL,'123','2021-09-07',NULL,NULL,NULL,'2021-09-07 11:53:09.528700','2021-11-02 15:30:01.024670',51,'2021-11-02 15:30:01.026468',NULL,'~',3,41,1),(1,0,'','Rechazada','2021-08-31',22500,NULL,NULL,NULL,NULL,NULL,NULL,'2021-08-31 10:01:56.413968','2021-11-02 15:30:15.636500',52,'2021-11-02 15:30:15.638918',NULL,'~',NULL,41,1),(8,7,'Por favor incluir la siguiente glosa en la factura: DESARROLLO DE PORTAFOLIO DE POSTRES VEGETALES A BASE DE ALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código 19IR-LR-121872','Inicial','2021-10-27',478800,NULL,NULL,NULL,NULL,NULL,NULL,'2021-10-27 10:16:05.452138','2021-11-02 15:35:03.268000',53,'2021-11-02 15:35:03.270087',NULL,'~',3,41,5),(8,7,'Por favor incluir la siguiente glosa en la factura: DESARROLLO DE PORTAFOLIO DE POSTRES VEGETALES A BASE DE ALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código 19IR-LR-121872','Validada','2021-10-27',478800,NULL,NULL,NULL,NULL,NULL,NULL,'2021-10-27 10:16:05.452138','2021-11-02 15:35:03.283420',54,'2021-11-02 15:35:03.285236',NULL,'~',3,41,5),(6,5,'Por favor incluir la siguiente glosa en la factura: DESARROLLO\r\nDE PORTAFOLIO DE POSTRES VEGETALES A BASE DE\r\nALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código\r\n19IR-LR-121872','Recepcionada','2021-10-25',110325,NULL,'284507','2021-11-02',NULL,NULL,NULL,'2021-10-25 17:43:41.294093','2021-11-02 15:35:55.743627',55,'2021-11-02 15:35:55.745848',NULL,'~',3,41,3),(10,9,'Por favor incluir la siguiente glosa en la factura: DESARROLLO DE PORTAFOLIO DE POSTRES VEGETALES A BASE DE ALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código 19IR-LR-121872','Inicial','2021-11-02',0,NULL,NULL,NULL,NULL,NULL,NULL,'2021-11-02 16:44:28.639158','2021-11-02 16:44:28.639217',56,'2021-11-02 16:44:28.643646',NULL,'+',3,41,6),(11,10,'Por favor incluir la siguiente glosa en la factura: DESARROLLO DE PORTAFOLIO DE POSTRES VEGETALES A BASE DE ALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código 19IR-LR-121872','Inicial','2021-11-02',0,NULL,NULL,NULL,NULL,NULL,NULL,'2021-11-02 16:46:46.257416','2021-11-02 16:46:46.257430',57,'2021-11-02 16:46:46.259125',NULL,'+',NULL,1,6),(12,11,'Por favor incluir la siguiente glosa en la factura: DESARROLLO DE PORTAFOLIO DE POSTRES VEGETALES A BASE DE ALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código 19IR-LR-121872','Inicial','2021-11-02',0,NULL,NULL,NULL,NULL,NULL,NULL,'2021-11-02 16:48:05.292265','2021-11-02 16:48:05.292278',58,'2021-11-02 16:48:05.294284',NULL,'+',NULL,1,6),(12,11,'Por favor incluir la siguiente glosa en la factura: DESARROLLO DE PORTAFOLIO DE POSTRES VEGETALES A BASE DE ALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código 19IR-LR-121872','Inicial','2021-11-02',18,NULL,NULL,NULL,NULL,NULL,NULL,'2021-11-02 16:48:05.292265','2021-11-02 16:48:06.479611',59,'2021-11-02 16:48:06.482808',NULL,'~',NULL,1,6),(12,11,'Por favor incluir la siguiente glosa en la factura: DESARROLLO DE PORTAFOLIO DE POSTRES VEGETALES A BASE DE ALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código 19IR-LR-121872','Inicial','2021-11-02',18,NULL,NULL,NULL,NULL,NULL,NULL,'2021-11-02 16:48:05.292265','2021-11-02 16:54:03.858077',60,'2021-11-02 16:54:03.860832',NULL,'~',NULL,1,6),(12,11,'Por favor incluir la siguiente glosa en la factura: DESARROLLO DE PORTAFOLIO DE POSTRES VEGETALES A BASE DE ALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código 19IR-LR-121872','Validada','2021-11-02',18.4,NULL,NULL,NULL,NULL,NULL,NULL,'2021-11-02 16:48:05.292265','2021-11-02 16:54:03.883001',61,'2021-11-02 16:54:03.885126',NULL,'~',NULL,1,6),(9,8,'Por favor incluir la siguiente glosa en la factura: DESARROLLO DE PORTAFOLIO DE POSTRES VEGETALES A BASE DE ALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código 19IR-LR-121872','Validada','2021-10-28',58750,NULL,NULL,NULL,NULL,NULL,NULL,'2021-10-28 12:22:44.476260','2021-10-29 08:33:42.997161',62,'2021-11-02 16:54:28.330149',NULL,'-',3,1,3),(10,9,'Por favor incluir la siguiente glosa en la factura: DESARROLLO DE PORTAFOLIO DE POSTRES VEGETALES A BASE DE ALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código 19IR-LR-121872','Inicial','2021-11-02',0,NULL,NULL,NULL,NULL,NULL,NULL,'2021-11-02 16:44:28.639158','2021-11-02 16:44:28.639217',63,'2021-11-02 16:58:13.846505',NULL,'-',3,1,6),(11,10,'Por favor incluir la siguiente glosa en la factura: DESARROLLO DE PORTAFOLIO DE POSTRES VEGETALES A BASE DE ALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código 19IR-LR-121872','Inicial','2021-11-02',0,NULL,NULL,NULL,NULL,NULL,NULL,'2021-11-02 16:46:46.257416','2021-11-02 16:46:46.257430',64,'2021-11-02 16:58:18.319561',NULL,'-',NULL,1,6),(12,11,'Por favor incluir la siguiente glosa en la factura: DESARROLLO DE PORTAFOLIO DE POSTRES VEGETALES A BASE DE ALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código 19IR-LR-121872','Validada','2021-11-02',18.4,NULL,NULL,NULL,NULL,NULL,NULL,'2021-11-02 16:48:05.292265','2021-11-02 16:54:03.883001',65,'2021-11-02 16:58:22.558672',NULL,'-',NULL,1,6),(13,8,'Por favor incluir la siguiente glosa en la factura: DESARROLLO DE PORTAFOLIO DE POSTRES VEGETALES A BASE DE ALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código 19IR-LR-121872','Inicial','2021-11-02',0,NULL,NULL,NULL,NULL,NULL,NULL,'2021-11-02 16:58:34.115975','2021-11-02 16:58:34.115990',66,'2021-11-02 16:58:34.119136',NULL,'+',4,1,6),(13,8,'Por favor incluir la siguiente glosa en la factura: DESARROLLO DE PORTAFOLIO DE POSTRES VEGETALES A BASE DE ALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código 19IR-LR-121872','Inicial','2021-11-02',55.199999999999996,NULL,NULL,NULL,NULL,NULL,NULL,'2021-11-02 16:58:34.115975','2021-11-02 16:58:35.531828',67,'2021-11-02 16:58:35.534244',NULL,'~',4,1,6),(13,8,'Por favor incluir la siguiente glosa en la factura: DESARROLLO DE PORTAFOLIO DE POSTRES VEGETALES A BASE DE ALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código 19IR-LR-121872','Inicial','2021-11-02',55.199999999999996,NULL,NULL,NULL,NULL,NULL,NULL,'2021-11-02 16:58:34.115975','2021-11-02 16:58:35.531828',68,'2021-11-02 16:58:42.331599',NULL,'-',4,1,6),(14,8,'Por favor incluir la siguiente glosa en la factura: DESARROLLO DE PORTAFOLIO DE POSTRES VEGETALES A BASE DE ALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código 19IR-LR-121872','Inicial','2021-11-02',0,NULL,NULL,NULL,NULL,NULL,NULL,'2021-11-02 17:00:44.386784','2021-11-02 17:00:44.386797',69,'2021-11-02 17:00:44.390315',NULL,'+',3,41,6),(14,8,'Por favor incluir la siguiente glosa en la factura: DESARROLLO DE PORTAFOLIO DE POSTRES VEGETALES A BASE DE ALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código 19IR-LR-121872','Inicial','2021-11-02',663840,NULL,NULL,NULL,NULL,NULL,NULL,'2021-11-02 17:00:44.386784','2021-11-02 17:00:45.553724',70,'2021-11-02 17:00:45.556268',NULL,'~',3,41,6),(15,9,'Por favor incluir la siguiente glosa en la factura: DESARROLLO DE PORTAFOLIO DE POSTRES VEGETALES A BASE DE ALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código 19IR-LR-121872','Inicial','2021-11-08',0,NULL,NULL,NULL,NULL,NULL,NULL,'2021-11-08 10:58:38.953299','2021-11-08 10:58:38.953314',71,'2021-11-08 10:58:38.955453',NULL,'+',3,41,8),(15,9,'Por favor incluir la siguiente glosa en la factura: DESARROLLO DE PORTAFOLIO DE POSTRES VEGETALES A BASE DE ALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código 19IR-LR-121872','Inicial','2021-11-08',220140,NULL,NULL,NULL,NULL,NULL,NULL,'2021-11-08 10:58:38.953299','2021-11-08 10:58:40.194705',72,'2021-11-08 10:58:40.197056',NULL,'~',3,41,8),(16,10,'Por favor incluir la siguiente glosa en la factura: DESARROLLO DE PORTAFOLIO DE POSTRES VEGETALES A BASE DE ALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código 19IR-LR-121872','Inicial','2021-11-08',0,NULL,NULL,NULL,NULL,NULL,NULL,'2021-11-08 11:47:30.815447','2021-11-08 11:47:30.815463',73,'2021-11-08 11:47:30.817848',NULL,'+',3,41,9),(16,10,'Por favor incluir la siguiente glosa en la factura: DESARROLLO DE PORTAFOLIO DE POSTRES VEGETALES A BASE DE ALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código 19IR-LR-121872','Inicial','2021-11-08',509350,NULL,NULL,NULL,NULL,NULL,NULL,'2021-11-08 11:47:30.815447','2021-11-08 11:47:32.667692',74,'2021-11-08 11:47:32.669756',NULL,'~',3,41,9),(16,10,'Por favor incluir la siguiente glosa en la factura: DESARROLLO DE PORTAFOLIO DE POSTRES VEGETALES A BASE DE ALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código 19IR-LR-121872','Inicial','2021-11-08',509350,NULL,NULL,NULL,NULL,NULL,NULL,'2021-11-08 11:47:30.815447','2021-11-08 12:12:20.167835',75,'2021-11-08 12:12:20.169908',NULL,'~',3,41,9),(16,10,'Por favor incluir la siguiente glosa en la factura: DESARROLLO DE PORTAFOLIO DE POSTRES VEGETALES A BASE DE ALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código 19IR-LR-121872','Validada','2021-11-08',519750,NULL,NULL,NULL,NULL,NULL,NULL,'2021-11-08 11:47:30.815447','2021-11-08 12:12:20.190407',76,'2021-11-08 12:12:20.192728',NULL,'~',3,41,9),(17,11,'Por favor incluir la siguiente glosa en la factura: DESARROLLO DE PORTAFOLIO DE POSTRES VEGETALES A BASE DE ALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código 19IR-LR-121872','Inicial','2021-11-09',0,NULL,NULL,NULL,NULL,NULL,NULL,'2021-11-09 09:28:33.763747','2021-11-09 09:28:33.763760',77,'2021-11-09 09:28:33.766301',NULL,'+',3,41,10),(17,11,'Por favor incluir la siguiente glosa en la factura: DESARROLLO DE PORTAFOLIO DE POSTRES VEGETALES A BASE DE ALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código 19IR-LR-121872','Inicial','2021-11-09',167679.5,NULL,NULL,NULL,NULL,NULL,NULL,'2021-11-09 09:28:33.763747','2021-11-09 09:28:35.345373',78,'2021-11-09 09:28:35.347682',NULL,'~',3,41,10),(17,11,'Por favor incluir la siguiente glosa en la factura: DESARROLLO DE PORTAFOLIO DE POSTRES VEGETALES A BASE DE ALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código 19IR-LR-121872','Inicial','2021-11-09',167679.5,NULL,NULL,NULL,NULL,NULL,NULL,'2021-11-09 09:28:33.763747','2021-11-09 10:48:15.635263',79,'2021-11-09 10:48:15.637381',NULL,'~',3,41,10),(17,11,'Por favor incluir la siguiente glosa en la factura: DESARROLLO DE PORTAFOLIO DE POSTRES VEGETALES A BASE DE ALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código 19IR-LR-121872','Validada','2021-11-09',175437.75,NULL,NULL,NULL,NULL,NULL,NULL,'2021-11-09 09:28:33.763747','2021-11-09 10:48:15.653914',80,'2021-11-09 10:48:15.656213',NULL,'~',3,41,10),(15,9,'Por favor incluir la siguiente glosa en la factura: DESARROLLO DE PORTAFOLIO DE POSTRES VEGETALES A BASE DE ALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código 19IR-LR-121872','Inicial','2021-11-08',220140,NULL,NULL,NULL,NULL,NULL,NULL,'2021-11-08 10:58:38.953299','2021-11-09 16:32:28.500892',81,'2021-11-09 16:32:28.503383',NULL,'~',3,42,8),(15,9,'Por favor incluir la siguiente glosa en la factura: DESARROLLO DE PORTAFOLIO DE POSTRES VEGETALES A BASE DE ALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código 19IR-LR-121872','Validada','2021-11-08',220140,NULL,NULL,NULL,NULL,NULL,NULL,'2021-11-08 10:58:38.953299','2021-11-09 16:32:28.517393',82,'2021-11-09 16:32:28.519505',NULL,'~',3,42,8),(16,10,'Por favor incluir la siguiente glosa en la factura: DESARROLLO DE PORTAFOLIO DE POSTRES VEGETALES A BASE DE ALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código 19IR-LR-121872','Semi-Recepcionada','2021-11-08',519750,NULL,'48348','2021-11-09',NULL,NULL,NULL,'2021-11-08 11:47:30.815447','2021-11-09 17:15:28.281254',83,'2021-11-09 17:15:28.283875',NULL,'~',3,41,9),(16,10,'Por favor incluir la siguiente glosa en la factura: DESARROLLO DE PORTAFOLIO DE POSTRES VEGETALES A BASE DE ALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código 19IR-LR-121872','Semi-Recepcionada','2021-11-08',519750,NULL,'48348','2021-11-09',NULL,NULL,NULL,'2021-11-08 11:47:30.815447','2021-11-09 17:17:31.710315',84,'2021-11-09 17:17:31.712604',NULL,'~',3,41,9);
/*!40000 ALTER TABLE `ordendecompra_historicalordendecompra` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ordendecompra_historicalordendecomprainsumo`
--

DROP TABLE IF EXISTS `ordendecompra_historicalordendecomprainsumo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ordendecompra_historicalordendecomprainsumo` (
  `id` bigint NOT NULL,
  `cantidad` bigint NOT NULL,
  `cantidad_recibida` bigint NOT NULL,
  `detalle` varchar(255) DEFAULT NULL,
  `neto` int NOT NULL,
  `conversion` double DEFAULT NULL,
  `history_id` int NOT NULL AUTO_INCREMENT,
  `history_date` datetime(6) NOT NULL,
  `history_change_reason` varchar(100) DEFAULT NULL,
  `history_type` varchar(1) NOT NULL,
  `history_user_id` int DEFAULT NULL,
  `insumo_id` bigint DEFAULT NULL,
  `orden_id` bigint DEFAULT NULL,
  PRIMARY KEY (`history_id`),
  KEY `ordendecompra_histor_history_user_id_a03ccc45_fk_auth_user` (`history_user_id`),
  KEY `ordendecompra_historicalordendecomprainsumo_id_325aae11` (`id`),
  KEY `ordendecompra_historicalordendecomprainsumo_insumo_id_b625484a` (`insumo_id`),
  KEY `ordendecompra_historicalordendecomprainsumo_orden_id_1125a2ef` (`orden_id`),
  CONSTRAINT `ordendecompra_histor_history_user_id_a03ccc45_fk_auth_user` FOREIGN KEY (`history_user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ordendecompra_historicalordendecomprainsumo`
--

LOCK TABLES `ordendecompra_historicalordendecomprainsumo` WRITE;
/*!40000 ALTER TABLE `ordendecompra_historicalordendecomprainsumo` DISABLE KEYS */;
INSERT INTO `ordendecompra_historicalordendecomprainsumo` VALUES (1,15,0,'',1500,NULL,1,'2021-08-31 16:09:10.822225',NULL,'~',1,1,1),(1,15,0,'',1500,NULL,2,'2021-08-31 16:09:55.779643',NULL,'~',1,1,1),(1,15,0,'',1500,NULL,3,'2021-09-07 09:17:36.469143',NULL,'-',NULL,1,1),(1,25,0,'',150,NULL,4,'2021-09-07 11:53:09.838757',NULL,'+',1,4,2),(1,25,0,'',150,NULL,5,'2021-09-07 11:53:26.413155',NULL,'~',1,4,2),(1,25,25,'',150,NULL,6,'2021-09-07 11:53:44.622106',NULL,'~',1,4,2),(2,50,0,'',150,NULL,7,'2021-09-21 19:12:30.346815',NULL,'+',1,4,3),(2,50,0,'',150,NULL,8,'2021-09-21 19:12:42.471706',NULL,'~',1,4,3),(2,50,50,'',150,NULL,9,'2021-09-21 19:13:03.907773',NULL,'~',1,4,3),(3,100,0,'',1400,NULL,10,'2021-10-22 10:12:54.966919',NULL,'+',41,5,4),(3,100,0,'',1400,NULL,11,'2021-10-22 10:19:44.559372',NULL,'~',41,5,4),(2,50,50,'',150,NULL,12,'2021-10-22 10:25:19.347740',NULL,'-',41,4,3),(1,25,25,'',150,NULL,13,'2021-10-22 10:25:19.349471',NULL,'-',41,4,2),(4,20000,0,'',27,NULL,14,'2021-10-25 17:25:00.662531',NULL,'+',41,6,5),(5,1,0,'',22825,NULL,15,'2021-10-25 17:43:41.298791',NULL,'+',41,8,6),(6,1,0,'',87500,NULL,16,'2021-10-25 17:43:41.301655',NULL,'+',41,7,6),(5,5,0,'',4565,NULL,17,'2021-10-25 17:45:25.870262',NULL,'~',41,8,6),(6,25,0,'',3500,NULL,18,'2021-10-25 17:45:25.874715',NULL,'~',41,7,6),(7,25,0,'',5500,NULL,19,'2021-10-26 16:18:08.949777',NULL,'+',41,9,7),(8,6,0,'',79800,NULL,20,'2021-10-27 10:16:05.459658',NULL,'+',41,10,8),(9,25,0,'',1350,NULL,21,'2021-10-28 12:22:44.486055',NULL,'+',41,11,9),(3,100,100,'',1400,NULL,22,'2021-10-28 12:27:14.753375',NULL,'~',41,5,4),(9,25,0,'',2350,NULL,23,'2021-10-29 08:33:42.988488',NULL,'~',41,11,9),(7,25,0,'',5500,NULL,24,'2021-11-02 15:09:29.499741',NULL,'~',39,9,7),(7,25,0,'',5500,NULL,25,'2021-11-02 15:11:02.777107',NULL,'~',39,9,7),(7,25,25,'',5500,NULL,26,'2021-11-02 15:21:53.610388',NULL,'~',39,9,7),(8,6,0,'',79800,NULL,27,'2021-11-02 15:35:03.276777',NULL,'~',41,10,8),(5,5,5,'',4565,NULL,28,'2021-11-02 15:35:54.362975',NULL,'~',41,8,6),(6,25,25,'',3500,NULL,29,'2021-11-02 15:35:55.734960',NULL,'~',41,7,6),(10,1,0,'',18,NULL,30,'2021-11-02 16:48:05.302317',NULL,'+',1,12,12),(10,1,0,'',18,NULL,31,'2021-11-02 16:54:03.875421',NULL,'~',1,12,12),(9,25,0,'',2350,NULL,32,'2021-11-02 16:54:28.326770',NULL,'-',1,11,9),(10,1,0,'',18,NULL,33,'2021-11-02 16:58:22.554523',NULL,'-',1,12,12),(11,3,0,'',18,NULL,34,'2021-11-02 16:58:34.125652',NULL,'+',1,12,13),(11,3,0,'',18,NULL,35,'2021-11-02 16:58:42.329711',NULL,'-',1,12,13),(12,36000,0,'',18,NULL,36,'2021-11-02 17:00:44.398581',NULL,'+',41,12,14),(13,10,0,'',22014,NULL,37,'2021-11-08 10:58:38.963162',NULL,'+',41,15,15),(14,100,0,'',561,NULL,38,'2021-11-08 11:47:30.830220',NULL,'+',41,18,16),(15,175,0,'',2590,NULL,39,'2021-11-08 11:47:30.838752',NULL,'+',41,17,16),(15,175,0,'',2590,NULL,40,'2021-11-08 12:12:20.176660',NULL,'~',41,17,16),(14,100,0,'',665,NULL,41,'2021-11-08 12:12:20.184596',NULL,'~',41,18,16),(16,25,0,'',6707,NULL,42,'2021-11-09 09:28:33.779606',NULL,'+',41,19,17),(16,25,0,'DOLAR 9/11 809,61',7018,NULL,43,'2021-11-09 10:48:15.646698',NULL,'~',41,19,17),(13,10,0,'',22014,NULL,44,'2021-11-09 16:32:28.512270',NULL,'~',42,15,15),(15,175,150,'',2590,NULL,45,'2021-11-09 17:15:27.167353',NULL,'~',41,17,16),(14,100,100,'',665,NULL,46,'2021-11-09 17:15:28.269636',NULL,'~',41,18,16),(15,175,150,'',2590,NULL,47,'2021-11-09 17:17:31.689311',NULL,'~',41,17,16),(14,100,100,'',665,NULL,48,'2021-11-09 17:17:31.701655',NULL,'~',41,18,16);
/*!40000 ALTER TABLE `ordendecompra_historicalordendecomprainsumo` ENABLE KEYS */;
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
  CONSTRAINT `ordendecompra_ordend_bodega_id_6fe26c51_fk_inventari` FOREIGN KEY (`bodega_id`) REFERENCES `inventario_bodega` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `ordendecompra_ordend_proveedor_id_22f275f4_fk_proveedor` FOREIGN KEY (`proveedor_id`) REFERENCES `proveedores_proveedor` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ordendecompra_ordendecompra`
--

LOCK TABLES `ordendecompra_ordendecompra` WRITE;
/*!40000 ALTER TABLE `ordendecompra_ordendecompra` DISABLE KEYS */;
INSERT INTO `ordendecompra_ordendecompra` VALUES (1,0,'','Rechazada','2021-08-31',22500,NULL,NULL,NULL,NULL,NULL,NULL,'2021-08-31 10:01:56.413968','2021-11-02 15:30:15.636500',NULL,1),(2,1,'','Rechazada','2021-09-07',3750,NULL,'123','2021-09-07',NULL,NULL,NULL,'2021-09-07 11:53:09.528700','2021-11-02 15:30:01.024670',3,1),(3,2,'','Rechazada','2021-09-21',7500,NULL,'679','2021-09-21',NULL,NULL,NULL,'2021-09-21 19:12:30.331166','2021-11-02 15:29:52.120504',3,1),(4,3,'Favor incluir siguiente código en factura: CORFO\r\n19IR-LR-121872','Pagada','2021-10-22',140000,NULL,'67689','2021-10-28','2021-10-26','2021-10-28','transferencia','2021-10-22 10:12:54.960601','2021-10-28 12:28:07.482643',3,1),(5,4,'Por favor incluir la siguiente glosa en la factura: DESARROLLO\r\nDE PORTAFOLIO DE POSTRES VEGETALES A BASE DE\r\nALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código\r\n19IR-LR-121872','Inicial','2021-10-25',540000,NULL,NULL,NULL,NULL,NULL,NULL,'2021-10-25 17:25:00.654670','2021-10-25 17:25:02.706667',3,2),(6,5,'Por favor incluir la siguiente glosa en la factura: DESARROLLO\r\nDE PORTAFOLIO DE POSTRES VEGETALES A BASE DE\r\nALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código\r\n19IR-LR-121872','Recepcionada','2021-10-25',110325,NULL,'284507','2021-11-02',NULL,NULL,NULL,'2021-10-25 17:43:41.294093','2021-11-02 15:35:55.743627',3,3),(7,6,'','Recepcionada','2021-10-26',137500,NULL,'284506','2021-11-02',NULL,NULL,NULL,'2021-10-26 16:18:08.942939','2021-11-02 15:21:53.621376',3,3),(8,7,'Por favor incluir la siguiente glosa en la factura: DESARROLLO DE PORTAFOLIO DE POSTRES VEGETALES A BASE DE ALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código 19IR-LR-121872','Validada','2021-10-27',478800,NULL,NULL,NULL,NULL,NULL,NULL,'2021-10-27 10:16:05.452138','2021-11-02 15:35:03.283420',3,5),(14,8,'Por favor incluir la siguiente glosa en la factura: DESARROLLO DE PORTAFOLIO DE POSTRES VEGETALES A BASE DE ALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código 19IR-LR-121872','Inicial','2021-11-02',663840,NULL,NULL,NULL,NULL,NULL,NULL,'2021-11-02 17:00:44.386784','2021-11-02 17:00:45.553724',3,6),(15,9,'Por favor incluir la siguiente glosa en la factura: DESARROLLO DE PORTAFOLIO DE POSTRES VEGETALES A BASE DE ALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código 19IR-LR-121872','Validada','2021-11-08',220140,NULL,NULL,NULL,NULL,NULL,NULL,'2021-11-08 10:58:38.953299','2021-11-09 16:32:28.517393',3,8),(16,10,'Por favor incluir la siguiente glosa en la factura: DESARROLLO DE PORTAFOLIO DE POSTRES VEGETALES A BASE DE ALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código 19IR-LR-121872','Semi-Recepcionada','2021-11-08',519750,NULL,'48348','2021-11-09',NULL,NULL,NULL,'2021-11-08 11:47:30.815447','2021-11-09 17:17:31.710315',3,9),(17,11,'Por favor incluir la siguiente glosa en la factura: DESARROLLO DE PORTAFOLIO DE POSTRES VEGETALES A BASE DE ALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código 19IR-LR-121872','Validada','2021-11-09',175437.75,NULL,NULL,NULL,NULL,NULL,NULL,'2021-11-09 09:28:33.763747','2021-11-09 10:48:15.653914',3,10);
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
  `neto` float NOT NULL,
  `conversion` double DEFAULT NULL,
  `insumo_id` bigint NOT NULL,
  `orden_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ordendecompra_ordend_insumo_id_10121dd3_fk_proveedor` (`insumo_id`),
  KEY `ordendecompra_ordend_orden_id_ce957df8_fk_ordendeco` (`orden_id`),
  CONSTRAINT `ordendecompra_ordend_insumo_id_10121dd3_fk_proveedor` FOREIGN KEY (`insumo_id`) REFERENCES `proveedores_proveedorinsumo` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `ordendecompra_ordend_orden_id_ce957df8_fk_ordendeco` FOREIGN KEY (`orden_id`) REFERENCES `ordendecompra_ordendecompra` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ordendecompra_ordendecomprainsumo`
--

LOCK TABLES `ordendecompra_ordendecomprainsumo` WRITE;
/*!40000 ALTER TABLE `ordendecompra_ordendecomprainsumo` DISABLE KEYS */;
INSERT INTO `ordendecompra_ordendecomprainsumo` VALUES (3,100,100,'',1400,NULL,5,4),(4,20000,0,'',27,NULL,6,5),(5,5,5,'',4565,NULL,8,6),(6,25,25,'',3500,NULL,7,6),(7,25,25,'',5500,NULL,9,7),(8,6,0,'',79800,NULL,10,8),(12,36000,0,'',18.44,NULL,12,14),(13,10,0,'',22014,NULL,15,15),(14,100,100,'',665,NULL,18,16),(15,175,150,'',2590,NULL,17,16),(16,25,0,'DOLAR 9/11 809,61',7017.51,NULL,19,17);
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
  CONSTRAINT `ordendecompra_regist_orden_id_1b869aee_fk_ordendeco` FOREIGN KEY (`orden_id`) REFERENCES `ordendecompra_ordendecompra` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `ordendecompra_registro_empleado_id_f8c6e67c_fk_auth_user_id` FOREIGN KEY (`empleado_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ordendecompra_registro`
--

LOCK TABLES `ordendecompra_registro` WRITE;
/*!40000 ALTER TABLE `ordendecompra_registro` DISABLE KEYS */;
INSERT INTO `ordendecompra_registro` VALUES (1,'Inicial','2021-08-31 10:01:56.514986','2021-08-31 10:01:56.515027',1,1),(2,'Validada','2021-08-31 16:09:10.849058','2021-08-31 16:09:10.849104',1,1),(3,'Inicial','2021-08-31 16:09:37.222069','2021-08-31 16:09:37.222092',1,1),(4,'Validada','2021-08-31 16:09:55.798169','2021-08-31 16:09:55.798190',1,1),(5,'Inicial','2021-09-07 11:53:09.901801','2021-09-07 11:53:09.901847',1,2),(6,'Validada','2021-09-07 11:53:26.442558','2021-09-07 11:53:26.442639',1,2),(7,'Recepcionada','2021-09-07 11:53:44.664244','2021-09-07 11:53:44.664285',1,2),(8,'Inicial','2021-09-21 19:12:30.353142','2021-09-21 19:12:30.353166',1,3),(9,'Validada','2021-09-21 19:12:42.479346','2021-09-21 19:12:42.479370',1,3),(10,'Recepcionada','2021-09-21 19:13:03.913827','2021-09-21 19:13:03.913840',1,3),(11,'Inicial','2021-10-22 10:12:54.971337','2021-10-22 10:12:54.971357',41,4),(12,'Validada','2021-10-22 10:19:44.562835','2021-10-22 10:19:44.562857',41,4),(13,'Rechazada','2021-10-22 10:20:18.473036','2021-10-22 10:20:18.473054',41,4),(14,'Validada','2021-10-22 10:20:35.228841','2021-10-22 10:20:35.228855',41,4),(15,'Inicial','2021-10-25 17:25:00.665657','2021-10-25 17:25:00.665696',41,5),(16,'Inicial','2021-10-25 17:43:41.305631','2021-10-25 17:43:41.305649',41,6),(17,'Inicial','2021-10-25 17:44:25.768563','2021-10-25 17:44:25.768582',41,6),(18,'Validada','2021-10-25 17:45:25.877545','2021-10-25 17:45:25.877563',41,6),(19,'Inicial','2021-10-26 16:18:08.954237','2021-10-26 16:18:08.954256',41,7),(20,'Inicial','2021-10-27 10:16:05.464919','2021-10-27 10:16:05.464949',41,8),(22,'Recepcionada','2021-10-28 12:27:14.757667','2021-10-28 12:27:14.757682',41,4),(23,'Pagada','2021-10-28 12:28:07.481043','2021-10-28 12:28:07.481063',41,4),(25,'Validada','2021-11-02 15:09:29.503003','2021-11-02 15:09:29.503019',39,7),(26,'Semi-Recepcionada','2021-11-02 15:11:03.819339','2021-11-02 15:11:03.819361',39,7),(27,'Recepcionada','2021-11-02 15:21:53.617760','2021-11-02 15:21:53.617824',39,7),(28,'Rechazada','2021-11-02 15:29:04.846713','2021-11-02 15:29:04.846803',41,3),(29,'Validada','2021-11-02 15:29:22.302628','2021-11-02 15:29:22.302643',41,2),(30,'Inicial','2021-11-02 15:29:28.070995','2021-11-02 15:29:28.071041',41,2),(31,'Inicial','2021-11-02 15:29:32.779996','2021-11-02 15:29:32.780013',41,2),(32,'Recepcionada','2021-11-02 15:29:40.985260','2021-11-02 15:29:40.985273',41,3),(33,'Rechazada','2021-11-02 15:29:52.123676','2021-11-02 15:29:52.123687',41,3),(34,'Rechazada','2021-11-02 15:30:01.028856','2021-11-02 15:30:01.028868',41,2),(35,'Rechazada','2021-11-02 15:30:15.643451','2021-11-02 15:30:15.643485',41,1),(36,'Validada','2021-11-02 15:35:03.281940','2021-11-02 15:35:03.281960',41,8),(37,'Recepcionada','2021-11-02 15:35:55.740516','2021-11-02 15:35:55.740537',41,6),(41,'Inicial','2021-11-02 17:00:44.403284','2021-11-02 17:00:44.403299',41,14),(42,'Inicial','2021-11-08 10:58:38.970755','2021-11-08 10:58:38.970795',41,15),(43,'Inicial','2021-11-08 11:47:30.842331','2021-11-08 11:47:30.842352',41,16),(44,'Validada','2021-11-08 12:12:20.188834','2021-11-08 12:12:20.188860',41,16),(45,'Inicial','2021-11-09 09:28:33.782426','2021-11-09 09:28:33.782440',41,17),(46,'Validada','2021-11-09 10:48:15.652883','2021-11-09 10:48:15.652906',41,17),(47,'Validada','2021-11-09 16:32:28.515915','2021-11-09 16:32:28.515943',42,15),(48,'Semi-Recepcionada','2021-11-09 17:15:28.277755','2021-11-09 17:15:28.277780',41,16),(49,'Semi-Recepcionada','2021-11-09 17:17:31.708371','2021-11-09 17:17:31.708391',41,16);
/*!40000 ALTER TABLE `ordendecompra_registro` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pauta_columna`
--

DROP TABLE IF EXISTS `pauta_columna`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pauta_columna` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pauta_columna`
--

LOCK TABLES `pauta_columna` WRITE;
/*!40000 ALTER TABLE `pauta_columna` DISABLE KEYS */;
INSERT INTO `pauta_columna` VALUES (1,'PH','2021-08-31 09:05:21.308906','2021-08-31 09:05:21.308925'),(2,'T°','2021-08-31 09:05:25.452690','2021-08-31 09:05:25.452711'),(3,'Hora Inicio','2021-09-07 15:49:18.441163','2021-09-07 15:49:18.441184');
/*!40000 ALTER TABLE `pauta_columna` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pauta_etapa`
--

DROP TABLE IF EXISTS `pauta_etapa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pauta_etapa` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `orden` int NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `pauta_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `pauta_etapa_pauta_id_15c79de0_fk_pauta_pauta_id` (`pauta_id`),
  CONSTRAINT `pauta_etapa_pauta_id_15c79de0_fk_pauta_pauta_id` FOREIGN KEY (`pauta_id`) REFERENCES `pauta_pauta` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pauta_etapa`
--

LOCK TABLES `pauta_etapa` WRITE;
/*!40000 ALTER TABLE `pauta_etapa` DISABLE KEYS */;
INSERT INTO `pauta_etapa` VALUES (6,4,'CALENTAMIENTO Hasta 45°C','2021-08-31 13:15:21.746788','2021-08-31 16:00:18.315051',2),(7,1,'Matrimonio','2021-08-31 15:05:18.439627','2021-08-31 16:00:18.375679',2),(8,2,'La morición','2021-08-31 15:05:18.539636','2021-08-31 16:00:18.441067',2),(9,0,'Bailar','2021-08-31 15:31:45.172690','2021-08-31 15:31:45.172715',3),(10,0,'Bailar','2021-08-31 15:32:13.610054','2021-08-31 15:32:13.610087',4),(11,0,'asd','2021-08-31 15:39:09.589120','2021-09-03 16:15:40.938654',5),(12,0,'asd','2021-09-03 15:21:35.806716','2021-09-07 15:29:44.496522',6);
/*!40000 ALTER TABLE `pauta_etapa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pauta_historicalcolumna`
--

DROP TABLE IF EXISTS `pauta_historicalcolumna`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pauta_historicalcolumna` (
  `id` bigint NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `history_id` int NOT NULL AUTO_INCREMENT,
  `history_date` datetime(6) NOT NULL,
  `history_change_reason` varchar(100) DEFAULT NULL,
  `history_type` varchar(1) NOT NULL,
  `history_user_id` int DEFAULT NULL,
  PRIMARY KEY (`history_id`),
  KEY `pauta_historicalcolumna_history_user_id_7eb65072_fk_auth_user_id` (`history_user_id`),
  KEY `pauta_historicalcolumna_id_9035091f` (`id`),
  CONSTRAINT `pauta_historicalcolumna_history_user_id_7eb65072_fk_auth_user_id` FOREIGN KEY (`history_user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pauta_historicalcolumna`
--

LOCK TABLES `pauta_historicalcolumna` WRITE;
/*!40000 ALTER TABLE `pauta_historicalcolumna` DISABLE KEYS */;
INSERT INTO `pauta_historicalcolumna` VALUES (3,'Fecha','2021-08-31 16:30:04.940538','2021-08-31 16:30:04.940557',1,'2021-08-31 16:30:05.024161',NULL,'+',1),(3,'Fecha','2021-08-31 16:30:04.940538','2021-08-31 16:30:04.940557',2,'2021-08-31 17:12:41.459306',NULL,'-',1),(3,'Hora Inicio','2021-09-07 15:49:18.441163','2021-09-07 15:49:18.441184',3,'2021-09-07 15:49:18.473020',NULL,'+',NULL),(4,'Hora Fin','2021-09-07 15:50:20.058192','2021-09-07 15:50:20.058234',4,'2021-09-07 15:50:20.115173',NULL,'+',NULL),(4,'Hora Find','2021-09-07 15:50:20.058192','2021-09-07 15:53:10.187996',5,'2021-09-07 15:53:10.239349',NULL,'~',NULL),(4,'Hora Find','2021-09-07 15:50:20.058192','2021-09-07 15:53:10.187996',6,'2021-09-07 15:57:18.503056',NULL,'-',NULL);
/*!40000 ALTER TABLE `pauta_historicalcolumna` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pauta_historicaletapa`
--

DROP TABLE IF EXISTS `pauta_historicaletapa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pauta_historicaletapa` (
  `id` bigint NOT NULL,
  `orden` int NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `history_id` int NOT NULL AUTO_INCREMENT,
  `history_date` datetime(6) NOT NULL,
  `history_change_reason` varchar(100) DEFAULT NULL,
  `history_type` varchar(1) NOT NULL,
  `history_user_id` int DEFAULT NULL,
  `pauta_id` bigint DEFAULT NULL,
  PRIMARY KEY (`history_id`),
  KEY `pauta_historicaletapa_history_user_id_0f5b43e3_fk_auth_user_id` (`history_user_id`),
  KEY `pauta_historicaletapa_id_a6c60ee8` (`id`),
  KEY `pauta_historicaletapa_pauta_id_a4386f66` (`pauta_id`),
  CONSTRAINT `pauta_historicaletapa_history_user_id_0f5b43e3_fk_auth_user_id` FOREIGN KEY (`history_user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pauta_historicaletapa`
--

LOCK TABLES `pauta_historicaletapa` WRITE;
/*!40000 ALTER TABLE `pauta_historicaletapa` DISABLE KEYS */;
INSERT INTO `pauta_historicaletapa` VALUES (11,0,'asd','2021-08-31 15:39:09.589120','2021-08-31 16:30:11.956319',1,'2021-08-31 16:30:11.983696',NULL,'~',1,5),(11,0,'asd','2021-08-31 15:39:09.589120','2021-08-31 16:31:52.534603',2,'2021-08-31 16:31:52.574863',NULL,'~',1,5),(11,0,'asd','2021-08-31 15:39:09.589120','2021-08-31 16:32:16.806406',3,'2021-08-31 16:32:16.848718',NULL,'~',1,5),(11,0,'asd','2021-08-31 15:39:09.589120','2021-08-31 16:32:27.863227',4,'2021-08-31 16:32:27.907183',NULL,'~',1,5),(11,0,'asd','2021-08-31 15:39:09.589120','2021-08-31 16:33:43.106138',5,'2021-08-31 16:33:43.157423',NULL,'~',1,5),(11,0,'asd','2021-08-31 15:39:09.589120','2021-08-31 16:34:40.414225',6,'2021-08-31 16:34:40.432539',NULL,'~',1,5),(11,0,'asd','2021-08-31 15:39:09.589120','2021-08-31 16:35:22.405107',7,'2021-08-31 16:35:22.430999',NULL,'~',1,5),(11,0,'asd','2021-08-31 15:39:09.589120','2021-08-31 16:35:41.534495',8,'2021-08-31 16:35:41.582727',NULL,'~',1,5),(11,0,'asd','2021-08-31 15:39:09.589120','2021-08-31 16:35:49.565669',9,'2021-08-31 16:35:49.590416',NULL,'~',1,5),(11,0,'asd','2021-08-31 15:39:09.589120','2021-08-31 16:36:02.160727',10,'2021-08-31 16:36:02.223483',NULL,'~',1,5),(11,0,'asd','2021-08-31 15:39:09.589120','2021-08-31 16:36:10.646330',11,'2021-08-31 16:36:10.674583',NULL,'~',1,5),(11,0,'asd','2021-08-31 15:39:09.589120','2021-08-31 16:36:42.266476',12,'2021-08-31 16:36:42.289838',NULL,'~',1,5),(11,0,'asd','2021-08-31 15:39:09.589120','2021-08-31 16:37:27.848278',13,'2021-08-31 16:37:27.872401',NULL,'~',1,5),(11,0,'asd','2021-08-31 15:39:09.589120','2021-08-31 16:37:36.162639',14,'2021-08-31 16:37:36.188994',NULL,'~',1,5),(11,0,'asd','2021-08-31 15:39:09.589120','2021-08-31 16:37:53.267428',15,'2021-08-31 16:37:53.289967',NULL,'~',1,5),(11,0,'asd','2021-08-31 15:39:09.589120','2021-08-31 16:37:59.041259',16,'2021-08-31 16:37:59.064208',NULL,'~',1,5),(11,0,'asd','2021-08-31 15:39:09.589120','2021-08-31 16:38:04.949960',17,'2021-08-31 16:38:04.972381',NULL,'~',1,5),(11,0,'asd','2021-08-31 15:39:09.589120','2021-08-31 16:38:30.072145',18,'2021-08-31 16:38:30.139723',NULL,'~',1,5),(12,0,'asd','2021-09-03 15:21:35.806716','2021-09-03 15:21:35.806739',19,'2021-09-03 15:21:35.864389',NULL,'+',1,6),(12,0,'asd','2021-09-03 15:21:35.806716','2021-09-03 16:08:25.881935',20,'2021-09-03 16:08:25.900734',NULL,'~',1,6),(11,0,'asd','2021-08-31 15:39:09.589120','2021-09-03 16:12:16.941545',21,'2021-09-03 16:12:16.965560',NULL,'~',1,5),(11,0,'asd','2021-08-31 15:39:09.589120','2021-09-03 16:12:25.984907',22,'2021-09-03 16:12:26.007308',NULL,'~',1,5),(11,0,'asd','2021-08-31 15:39:09.589120','2021-09-03 16:12:34.417182',23,'2021-09-03 16:12:34.515438',NULL,'~',1,5),(12,0,'asd','2021-09-03 15:21:35.806716','2021-09-03 16:14:28.569789',24,'2021-09-03 16:14:28.589142',NULL,'~',1,6),(12,0,'asd','2021-09-03 15:21:35.806716','2021-09-03 16:15:34.581029',25,'2021-09-03 16:15:34.597472',NULL,'~',1,6),(11,0,'asd','2021-08-31 15:39:09.589120','2021-09-03 16:15:40.938654',26,'2021-09-03 16:15:40.956220',NULL,'~',1,5),(12,0,'asd','2021-09-03 15:21:35.806716','2021-09-03 16:17:30.555434',27,'2021-09-03 16:17:30.571471',NULL,'~',1,6),(13,0,'Etapa 2','2021-09-07 15:25:11.123903','2021-09-07 15:25:11.123947',28,'2021-09-07 15:25:11.172824',NULL,'+',NULL,7),(13,0,'Etapa 2','2021-09-07 15:25:11.123903','2021-09-07 15:27:33.939621',29,'2021-09-07 15:27:33.963903',NULL,'~',NULL,7),(13,0,'Etapa 2','2021-09-07 15:25:11.123903','2021-09-07 15:27:44.610073',30,'2021-09-07 15:27:44.728467',NULL,'~',NULL,7),(13,0,'Etapon','2021-09-07 15:25:11.123903','2021-09-07 15:27:56.470537',31,'2021-09-07 15:27:56.487663',NULL,'~',NULL,7),(13,0,'Etapon','2021-09-07 15:25:11.123903','2021-09-07 15:27:56.470537',32,'2021-09-07 15:28:27.277719',NULL,'-',NULL,7),(12,0,'asd','2021-09-03 15:21:35.806716','2021-09-07 15:29:44.496522',33,'2021-09-07 15:29:44.512510',NULL,'~',1,6);
/*!40000 ALTER TABLE `pauta_historicaletapa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pauta_historicalingrediente`
--

DROP TABLE IF EXISTS `pauta_historicalingrediente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pauta_historicalingrediente` (
  `id` bigint NOT NULL,
  `cantidad` double NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `history_id` int NOT NULL AUTO_INCREMENT,
  `history_date` datetime(6) NOT NULL,
  `history_change_reason` varchar(100) DEFAULT NULL,
  `history_type` varchar(1) NOT NULL,
  `history_user_id` int DEFAULT NULL,
  `insumo_id` bigint DEFAULT NULL,
  `pauta_id` bigint DEFAULT NULL,
  `unidad` varchar(255) NOT NULL,
  PRIMARY KEY (`history_id`),
  KEY `pauta_historicalingr_history_user_id_c7fe1e93_fk_auth_user` (`history_user_id`),
  KEY `pauta_historicalingrediente_id_2c8088a4` (`id`),
  KEY `pauta_historicalingrediente_insumo_id_925ce4c9` (`insumo_id`),
  KEY `pauta_historicalingrediente_pauta_id_ef3eabee` (`pauta_id`),
  CONSTRAINT `pauta_historicalingr_history_user_id_c7fe1e93_fk_auth_user` FOREIGN KEY (`history_user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=70 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pauta_historicalingrediente`
--

LOCK TABLES `pauta_historicalingrediente` WRITE;
/*!40000 ALTER TABLE `pauta_historicalingrediente` DISABLE KEYS */;
INSERT INTO `pauta_historicalingrediente` VALUES (22,15,'2021-08-31 16:31:52.077600','2021-08-31 16:31:52.077629',1,'2021-08-31 16:31:52.272645',NULL,'+',1,2,5,'gr'),(23,10,'2021-08-31 16:31:52.408318','2021-08-31 16:31:52.408355',2,'2021-08-31 16:31:52.483360',NULL,'+',1,1,5,'gr'),(22,15,'2021-08-31 16:31:52.077600','2021-08-31 16:32:16.701874',3,'2021-08-31 16:32:16.732574',NULL,'~',1,2,5,'gr'),(23,10,'2021-08-31 16:31:52.408318','2021-08-31 16:32:16.759345',4,'2021-08-31 16:32:16.782218',NULL,'~',1,1,5,'gr'),(22,15,'2021-08-31 16:31:52.077600','2021-08-31 16:32:27.737680',5,'2021-08-31 16:32:27.790224',NULL,'~',1,2,5,'gr'),(23,10,'2021-08-31 16:31:52.408318','2021-08-31 16:32:27.808932',6,'2021-08-31 16:32:27.823300',NULL,'~',1,1,5,'gr'),(22,15,'2021-08-31 16:31:52.077600','2021-08-31 16:33:43.008343',7,'2021-08-31 16:33:43.023923',NULL,'~',1,2,5,'gr'),(23,10,'2021-08-31 16:31:52.408318','2021-08-31 16:33:43.058167',8,'2021-08-31 16:33:43.073622',NULL,'~',1,1,5,'gr'),(22,15,'2021-08-31 16:31:52.077600','2021-08-31 16:34:40.318789',9,'2021-08-31 16:34:40.349176',NULL,'~',1,2,5,'gr'),(23,10,'2021-08-31 16:31:52.408318','2021-08-31 16:34:40.367985',10,'2021-08-31 16:34:40.390914',NULL,'~',1,1,5,'gr'),(22,15,'2021-08-31 16:31:52.077600','2021-08-31 16:35:22.259918',11,'2021-08-31 16:35:22.289470',NULL,'~',1,2,5,'gr'),(23,10,'2021-08-31 16:31:52.408318','2021-08-31 16:35:22.308548',12,'2021-08-31 16:35:22.347901',NULL,'~',1,1,5,'gr'),(22,15,'2021-08-31 16:31:52.077600','2021-08-31 16:35:41.442235',13,'2021-08-31 16:35:41.457284',NULL,'~',1,2,5,'gr'),(23,10,'2021-08-31 16:31:52.408318','2021-08-31 16:35:41.483740',14,'2021-08-31 16:35:41.498924',NULL,'~',1,1,5,'gr'),(22,15,'2021-08-31 16:31:52.077600','2021-08-31 16:35:49.392658',15,'2021-08-31 16:35:49.414838',NULL,'~',1,2,5,'gr'),(23,10,'2021-08-31 16:31:52.408318','2021-08-31 16:35:49.492241',16,'2021-08-31 16:35:49.514715',NULL,'~',1,1,5,'gr'),(22,15,'2021-08-31 16:31:52.077600','2021-08-31 16:36:01.993657',17,'2021-08-31 16:36:02.023871',NULL,'~',1,2,5,'gr'),(23,10,'2021-08-31 16:31:52.408318','2021-08-31 16:36:02.051155',18,'2021-08-31 16:36:02.099243',NULL,'~',1,1,5,'gr'),(22,15,'2021-08-31 16:31:52.077600','2021-08-31 16:36:10.540795',19,'2021-08-31 16:36:10.565079',NULL,'~',1,2,5,'gr'),(23,10,'2021-08-31 16:31:52.408318','2021-08-31 16:36:10.591840',20,'2021-08-31 16:36:10.615498',NULL,'~',1,1,5,'gr'),(22,15,'2021-08-31 16:31:52.077600','2021-08-31 16:36:42.110420',21,'2021-08-31 16:36:42.131052',NULL,'~',1,2,5,'gr'),(23,10,'2021-08-31 16:31:52.408318','2021-08-31 16:36:42.160234',22,'2021-08-31 16:36:42.206628',NULL,'~',1,1,5,'gr'),(22,15,'2021-08-31 16:31:52.077600','2021-08-31 16:37:27.737684',23,'2021-08-31 16:37:27.763798',NULL,'~',1,2,5,'gr'),(23,10,'2021-08-31 16:31:52.408318','2021-08-31 16:37:27.791086',24,'2021-08-31 16:37:27.813829',NULL,'~',1,1,5,'gr'),(22,15,'2021-08-31 16:31:52.077600','2021-08-31 16:37:35.961006',25,'2021-08-31 16:37:35.990218',NULL,'~',1,2,5,'gr'),(23,10,'2021-08-31 16:31:52.408318','2021-08-31 16:37:36.051347',26,'2021-08-31 16:37:36.111102',NULL,'~',1,1,5,'gr'),(22,15,'2021-08-31 16:31:52.077600','2021-08-31 16:37:53.127742',27,'2021-08-31 16:37:53.156522',NULL,'~',1,2,5,'gr'),(23,10,'2021-08-31 16:31:52.408318','2021-08-31 16:37:53.183840',28,'2021-08-31 16:37:53.231698',NULL,'~',1,1,5,'gr'),(22,15,'2021-08-31 16:31:52.077600','2021-08-31 16:37:58.884988',29,'2021-08-31 16:37:58.906454',NULL,'~',1,2,5,'gr'),(23,10,'2021-08-31 16:31:52.408318','2021-08-31 16:37:58.933424',30,'2021-08-31 16:37:58.981027',NULL,'~',1,1,5,'gr'),(22,15,'2021-08-31 16:31:52.077600','2021-08-31 16:38:04.843230',31,'2021-08-31 16:38:04.864004',NULL,'~',1,2,5,'gr'),(23,10,'2021-08-31 16:31:52.408318','2021-08-31 16:38:04.892021',32,'2021-08-31 16:38:04.914071',NULL,'~',1,1,5,'gr'),(22,15,'2021-08-31 16:31:52.077600','2021-08-31 16:38:29.959969',33,'2021-08-31 16:38:29.988752',NULL,'~',1,2,5,'gr'),(23,10,'2021-08-31 16:31:52.408318','2021-08-31 16:38:30.016189',34,'2021-08-31 16:38:30.038885',NULL,'~',1,1,5,'gr'),(24,5,'2021-09-03 15:21:35.699300','2021-09-03 15:21:35.699322',35,'2021-09-03 15:21:35.714681',NULL,'+',1,2,6,'gramo'),(25,12,'2021-09-03 15:21:35.740032','2021-09-03 15:21:35.740054',36,'2021-09-03 15:21:35.756118',NULL,'+',1,1,6,'litro'),(24,5,'2021-09-03 15:21:35.699300','2021-09-03 16:08:25.784141',37,'2021-09-03 16:08:25.808655',NULL,'~',1,2,6,'gramo'),(25,12,'2021-09-03 15:21:35.740032','2021-09-03 16:08:25.835266',38,'2021-09-03 16:08:25.858896',NULL,'~',1,1,6,'litro'),(22,15,'2021-08-31 16:31:52.077600','2021-09-03 16:12:16.758144',39,'2021-09-03 16:12:16.790493',NULL,'~',1,2,5,'kilogramo'),(22,15,'2021-08-31 16:31:52.077600','2021-09-03 16:12:16.862573',40,'2021-09-03 16:12:16.882469',NULL,'~',1,2,5,'kilogramo'),(23,10,'2021-08-31 16:31:52.408318','2021-08-31 16:38:30.016189',41,'2021-09-03 16:12:16.914092',NULL,'-',1,1,5,'gramo'),(22,15,'2021-08-31 16:31:52.077600','2021-09-03 16:12:25.854681',42,'2021-09-03 16:12:25.874194',NULL,'~',1,2,5,'kilogramo'),(26,15,'2021-09-03 16:12:25.901299','2021-09-03 16:12:25.901321',43,'2021-09-03 16:12:25.924167',NULL,'+',1,1,5,'litro'),(22,15,'2021-08-31 16:31:52.077600','2021-09-03 16:12:34.319599',44,'2021-09-03 16:12:34.340093',NULL,'~',1,2,5,'kilogramo'),(26,15,'2021-09-03 16:12:25.901299','2021-09-03 16:12:34.368598',45,'2021-09-03 16:12:34.390822',NULL,'~',1,1,5,'cc'),(24,5,'2021-09-03 15:21:35.699300','2021-09-03 16:14:28.463444',46,'2021-09-03 16:14:28.481050',NULL,'~',1,2,6,'gramo'),(25,12,'2021-09-03 15:21:35.740032','2021-09-03 16:14:28.507975',47,'2021-09-03 16:14:28.542138',NULL,'~',1,1,6,'cc'),(24,5,'2021-09-03 15:21:35.699300','2021-09-03 16:15:34.423107',48,'2021-09-03 16:15:34.439800',NULL,'~',1,2,6,'gramo'),(25,12,'2021-09-03 15:21:35.740032','2021-09-03 16:15:34.527445',49,'2021-09-03 16:15:34.556150',NULL,'~',1,1,6,'cc'),(22,15,'2021-08-31 16:31:52.077600','2021-09-03 16:15:40.835781',50,'2021-09-03 16:15:40.856289',NULL,'~',1,2,5,'kilogramo'),(26,15,'2021-09-03 16:12:25.901299','2021-09-03 16:15:40.883352',51,'2021-09-03 16:15:40.906635',NULL,'~',1,1,5,'litro'),(24,5,'2021-09-03 15:21:35.699300','2021-09-03 16:17:30.294283',52,'2021-09-03 16:17:30.314016',NULL,'~',1,2,6,'gramo'),(25,12,'2021-09-03 15:21:35.740032','2021-09-03 16:17:30.332801',53,'2021-09-03 16:17:30.422740',NULL,'~',1,1,6,'cc'),(27,15,'2021-09-07 15:25:11.023779','2021-09-07 15:25:11.023828',54,'2021-09-07 15:25:11.039027',NULL,'+',NULL,2,7,'kilogramo'),(27,10,'2021-09-07 15:25:11.023779','2021-09-07 15:27:33.888328',55,'2021-09-07 15:27:33.913620',NULL,'~',NULL,2,7,'kilogramo'),(28,10,'2021-09-07 15:27:44.486621','2021-09-07 15:27:44.486646',56,'2021-09-07 15:27:44.524995',NULL,'+',NULL,1,7,'litro'),(27,10,'2021-09-07 15:25:11.023779','2021-09-07 15:27:33.888328',57,'2021-09-07 15:27:44.550463',NULL,'-',NULL,2,7,'kilogramo'),(28,10,'2021-09-07 15:27:44.486621','2021-09-07 15:27:56.420160',58,'2021-09-07 15:27:56.438129',NULL,'~',NULL,1,7,'litro'),(28,10,'2021-09-07 15:27:44.486621','2021-09-07 15:27:56.420160',59,'2021-09-07 15:28:27.269104',NULL,'-',NULL,1,7,'litro'),(24,5,'2021-09-03 15:21:35.699300','2021-09-07 15:29:44.165116',60,'2021-09-07 15:29:44.213490',NULL,'~',1,2,6,'gramo'),(25,12,'2021-09-03 15:21:35.740032','2021-09-07 15:29:44.331557',61,'2021-09-07 15:29:44.379092',NULL,'~',1,1,6,'cc'),(24,5,'2021-09-03 15:21:35.699300','2021-09-07 15:29:44.165116',62,'2021-11-08 12:19:11.428081',NULL,'-',41,2,6,'gramo'),(22,15,'2021-08-31 16:31:52.077600','2021-09-03 16:15:40.835781',63,'2021-11-08 12:19:11.433246',NULL,'-',41,2,5,'kilogramo'),(18,150,'2021-08-31 15:04:06.122557','2021-08-31 16:00:18.283676',64,'2021-11-08 12:19:11.434509',NULL,'-',41,2,2,'gramo'),(26,15,'2021-09-03 16:12:25.901299','2021-09-03 16:15:40.883352',65,'2021-11-08 12:19:26.761460',NULL,'-',41,1,5,'litro'),(25,12,'2021-09-03 15:21:35.740032','2021-09-07 15:29:44.331557',66,'2021-11-08 12:19:26.762833',NULL,'-',41,1,6,'cc'),(20,15,'2021-08-31 15:32:13.535758','2021-08-31 15:32:13.535784',67,'2021-11-08 12:19:26.764739',NULL,'-',41,1,4,'gramo'),(19,15,'2021-08-31 15:31:45.122985','2021-08-31 15:31:45.123007',68,'2021-11-08 12:19:26.765858',NULL,'-',41,1,3,'gramo'),(17,15,'2021-08-31 13:16:38.348952','2021-08-31 16:00:18.230357',69,'2021-11-08 12:19:26.766861',NULL,'-',41,1,2,'gramo');
/*!40000 ALTER TABLE `pauta_historicalingrediente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pauta_historicalinstruccion`
--

DROP TABLE IF EXISTS `pauta_historicalinstruccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pauta_historicalinstruccion` (
  `id` bigint NOT NULL,
  `orden` int NOT NULL,
  `descripcion` varchar(255) NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `history_id` int NOT NULL AUTO_INCREMENT,
  `history_date` datetime(6) NOT NULL,
  `history_change_reason` varchar(100) DEFAULT NULL,
  `history_type` varchar(1) NOT NULL,
  `etapa_id` bigint DEFAULT NULL,
  `history_user_id` int DEFAULT NULL,
  PRIMARY KEY (`history_id`),
  KEY `pauta_historicalinst_history_user_id_ec256d34_fk_auth_user` (`history_user_id`),
  KEY `pauta_historicalinstruccion_id_310fc94b` (`id`),
  KEY `pauta_historicalinstruccion_etapa_id_4613db9f` (`etapa_id`),
  CONSTRAINT `pauta_historicalinst_history_user_id_ec256d34_fk_auth_user` FOREIGN KEY (`history_user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pauta_historicalinstruccion`
--

LOCK TABLES `pauta_historicalinstruccion` WRITE;
/*!40000 ALTER TABLE `pauta_historicalinstruccion` DISABLE KEYS */;
INSERT INTO `pauta_historicalinstruccion` VALUES (27,0,'Calentar el Queso','2021-08-31 16:32:16.876341','2021-08-31 16:32:16.876365',1,'2021-08-31 16:32:16.898541',NULL,'+',11,1),(28,1,'Introducir el Queso','2021-08-31 16:32:17.001102','2021-08-31 16:32:17.001122',2,'2021-08-31 16:32:17.066039',NULL,'+',11,1),(27,0,'Calentar el Queso','2021-08-31 16:32:16.876341','2021-08-31 16:32:16.876365',3,'2021-08-31 16:32:17.221023',NULL,'-',11,1),(28,1,'Introducir el Queso','2021-08-31 16:32:17.001102','2021-08-31 16:32:17.001122',4,'2021-08-31 16:32:17.252726',NULL,'-',11,1),(29,0,'Calentar el Queso','2021-08-31 16:32:27.926305','2021-08-31 16:32:27.926327',5,'2021-08-31 16:32:27.973674',NULL,'+',11,1),(29,0,'Calentar el Queso','2021-08-31 16:32:27.926305','2021-08-31 16:32:27.926327',6,'2021-08-31 16:32:28.132740',NULL,'-',11,1),(30,0,'Calentar el Queso','2021-08-31 16:35:22.460159','2021-08-31 16:35:22.460200',7,'2021-08-31 16:35:22.489427',NULL,'+',11,1),(30,0,'Calentar el Queso','2021-08-31 16:35:22.460159','2021-08-31 16:35:22.460200',8,'2021-08-31 16:35:41.656682',NULL,'-',11,1),(31,0,'Calentar el Queso','2021-08-31 16:35:49.626851','2021-08-31 16:35:49.626927',9,'2021-08-31 16:35:49.648195',NULL,'+',11,1),(32,0,'Calentar el Queso','2021-08-31 16:36:02.253133','2021-08-31 16:36:02.253157',10,'2021-08-31 16:36:02.311034',NULL,'+',11,1),(31,0,'Calentar el Queso','2021-08-31 16:35:49.626851','2021-08-31 16:35:49.626927',11,'2021-08-31 16:36:02.589187',NULL,'-',11,1),(32,0,'Calentar el Queso','2021-08-31 16:36:02.253133','2021-08-31 16:36:02.253157',12,'2021-08-31 16:36:02.730895',NULL,'-',11,1),(33,0,'Calentar el Queso','2021-08-31 16:36:10.726245','2021-08-31 16:36:10.726267',13,'2021-08-31 16:36:10.773712',NULL,'+',11,1),(33,0,'Calentar el Queso','2021-08-31 16:36:10.726245','2021-08-31 16:36:10.726267',14,'2021-08-31 16:36:10.903777',NULL,'-',11,1),(34,0,'Calentar el Queso','2021-08-31 16:36:42.318903','2021-08-31 16:36:42.318942',15,'2021-08-31 16:36:42.378327',NULL,'+',11,1),(35,0,'Calentar el Queso','2021-08-31 16:37:27.902079','2021-08-31 16:37:27.902119',16,'2021-08-31 16:37:27.922532',NULL,'+',11,1),(34,0,'Calentar el Queso','2021-08-31 16:36:42.318903','2021-08-31 16:37:53.318100',17,'2021-08-31 16:37:53.378289',NULL,'~',11,1),(35,0,'Calentar el Queso','2021-08-31 16:37:27.902079','2021-08-31 16:37:27.902119',18,'2021-08-31 16:37:53.689464',NULL,'-',11,1),(34,0,'Calentar el Queso','2021-08-31 16:36:42.318903','2021-08-31 16:37:53.318100',19,'2021-08-31 16:37:59.094387',NULL,'-',11,1),(36,0,'Introducir el Queso','2021-08-31 16:38:05.002043','2021-08-31 16:38:05.002087',20,'2021-08-31 16:38:05.072893',NULL,'+',11,1),(36,0,'Introducir el Queso','2021-08-31 16:38:05.002043','2021-08-31 16:38:05.002087',21,'2021-08-31 16:38:05.256742',NULL,'-',11,1),(37,0,'Calentar el Queso','2021-08-31 16:38:30.204274','2021-08-31 16:38:30.204321',22,'2021-08-31 16:38:30.231435',NULL,'+',11,1),(38,0,'xdas','2021-09-03 15:21:35.898935','2021-09-03 15:21:35.898959',23,'2021-09-03 15:21:35.956405',NULL,'+',12,1),(38,0,'xdas','2021-09-03 15:21:35.898935','2021-09-03 16:08:25.927003',24,'2021-09-03 16:08:25.950770',NULL,'~',12,1),(37,0,'Calentar el Queso','2021-08-31 16:38:30.204274','2021-09-03 16:12:16.996536',25,'2021-09-03 16:12:17.015556',NULL,'~',11,1),(37,0,'Calentar el Queso','2021-08-31 16:38:30.204274','2021-09-03 16:12:26.036090',26,'2021-09-03 16:12:26.140590',NULL,'~',11,1),(37,0,'Calentar el Queso','2021-08-31 16:38:30.204274','2021-09-03 16:12:34.543787',27,'2021-09-03 16:12:34.566798',NULL,'~',11,1),(38,0,'xdas','2021-09-03 15:21:35.898935','2021-09-03 16:14:28.616218',28,'2021-09-03 16:14:28.639490',NULL,'~',12,1),(38,0,'xdas','2021-09-03 15:21:35.898935','2021-09-03 16:15:34.624748',29,'2021-09-03 16:15:34.647649',NULL,'~',12,1),(37,0,'Calentar el Queso','2021-08-31 16:38:30.204274','2021-09-03 16:15:40.983810',30,'2021-09-03 16:15:41.097912',NULL,'~',11,1),(38,0,'xdas','2021-09-03 15:21:35.898935','2021-09-03 16:17:30.590214',31,'2021-09-03 16:17:30.612926',NULL,'~',12,1),(39,0,'Hola','2021-09-07 15:25:11.231731','2021-09-07 15:25:11.231755',32,'2021-09-07 15:25:11.289409',NULL,'+',13,NULL),(39,0,'Hola','2021-09-07 15:25:11.231731','2021-09-07 15:27:33.992478',33,'2021-09-07 15:27:34.005741',NULL,'~',13,NULL),(39,0,'Hola','2021-09-07 15:25:11.231731','2021-09-07 15:27:44.771381',34,'2021-09-07 15:27:44.796972',NULL,'~',13,NULL),(39,0,'Hola','2021-09-07 15:25:11.231731','2021-09-07 15:27:56.515304',35,'2021-09-07 15:27:56.538066',NULL,'~',13,NULL),(39,0,'Hola','2021-09-07 15:25:11.231731','2021-09-07 15:27:56.515304',36,'2021-09-07 15:28:27.273247',NULL,'-',13,NULL),(38,0,'xdas','2021-09-03 15:21:35.898935','2021-09-07 15:29:44.540922',37,'2021-09-07 15:29:44.654097',NULL,'~',12,1);
/*!40000 ALTER TABLE `pauta_historicalinstruccion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pauta_historicalpauta`
--

DROP TABLE IF EXISTS `pauta_historicalpauta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pauta_historicalpauta` (
  `id` bigint NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `history_id` int NOT NULL AUTO_INCREMENT,
  `history_date` datetime(6) NOT NULL,
  `history_change_reason` varchar(100) DEFAULT NULL,
  `history_type` varchar(1) NOT NULL,
  `history_user_id` int DEFAULT NULL,
  `rama_id` bigint DEFAULT NULL,
  PRIMARY KEY (`history_id`),
  KEY `pauta_historicalpauta_history_user_id_7f8471b1_fk_auth_user_id` (`history_user_id`),
  KEY `pauta_historicalpauta_id_f2e5b0bd` (`id`),
  KEY `pauta_historicalpauta_rama_id_95a7942a` (`rama_id`),
  CONSTRAINT `pauta_historicalpauta_history_user_id_7f8471b1_fk_auth_user_id` FOREIGN KEY (`history_user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pauta_historicalpauta`
--

LOCK TABLES `pauta_historicalpauta` WRITE;
/*!40000 ALTER TABLE `pauta_historicalpauta` DISABLE KEYS */;
INSERT INTO `pauta_historicalpauta` VALUES (5,'Santiago','2021-08-31 15:39:09.435977','2021-08-31 15:39:09.435997',1,'2021-08-31 15:39:09.467274',NULL,'+',1,1),(6,'Santiago','2021-08-31 15:39:41.924839','2021-08-31 15:39:41.924860',2,'2021-08-31 15:39:41.954432',NULL,'+',1,1),(6,'Yogurt Clasico','2021-08-31 15:39:41.924839','2021-08-31 15:42:37.520719',3,'2021-08-31 15:42:37.562321',NULL,'~',1,1),(6,'Yogurt Clasico','2021-08-31 15:39:41.924839','2021-08-31 15:42:37.520719',4,'2021-08-31 15:44:39.251336',NULL,'-',1,1),(6,'Yogurt Clasico','2021-08-31 15:44:58.459914','2021-08-31 15:44:58.459938',5,'2021-08-31 15:44:58.483951',NULL,'+',1,1),(2,'Cottage','2021-08-31 09:39:37.682164','2021-08-31 16:00:18.115968',6,'2021-08-31 16:00:18.174128',NULL,'~',1,1),(6,'Yogurt Clasico','2021-08-31 15:44:58.459914','2021-08-31 15:44:58.459938',7,'2021-08-31 16:12:48.007331',NULL,'-',1,1),(5,'Santiago','2021-08-31 15:39:09.435977','2021-08-31 16:30:11.816131',8,'2021-08-31 16:30:11.858259',NULL,'~',1,1),(5,'Santiago','2021-08-31 15:39:09.435977','2021-08-31 16:31:51.973498',9,'2021-08-31 16:31:51.999175',NULL,'~',1,1),(5,'Santiago','2021-08-31 15:39:09.435977','2021-08-31 16:32:16.635888',10,'2021-08-31 16:32:16.667848',NULL,'~',1,1),(5,'Santiago','2021-08-31 15:39:09.435977','2021-08-31 16:32:27.488089',11,'2021-08-31 16:32:27.615229',NULL,'~',1,1),(5,'Santiago','2021-08-31 15:39:09.435977','2021-08-31 16:33:42.948182',12,'2021-08-31 16:33:42.973903',NULL,'~',1,1),(5,'Santiago','2021-08-31 15:39:09.435977','2021-08-31 16:34:40.231585',13,'2021-08-31 16:34:40.290543',NULL,'~',1,1),(5,'Santiago','2021-08-31 15:39:09.435977','2021-08-31 16:35:22.118661',14,'2021-08-31 16:35:22.180895',NULL,'~',1,1),(5,'Santiago','2021-08-31 15:39:09.435977','2021-08-31 16:35:41.382983',15,'2021-08-31 16:35:41.407604',NULL,'~',1,1),(5,'Santiago','2021-08-31 15:39:09.435977','2021-08-31 16:35:49.298144',16,'2021-08-31 16:35:49.349583',NULL,'~',1,1),(5,'Santiago','2021-08-31 15:39:09.435977','2021-08-31 16:36:01.877060',17,'2021-08-31 16:36:01.915147',NULL,'~',1,1),(5,'Santiago','2021-08-31 15:39:09.435977','2021-08-31 16:36:10.453891',18,'2021-08-31 16:36:10.499522',NULL,'~',1,1),(5,'Santiago','2021-08-31 15:39:09.435977','2021-08-31 16:36:42.007211',19,'2021-08-31 16:36:42.066276',NULL,'~',1,1),(5,'Santiago','2021-08-31 15:39:09.435977','2021-08-31 16:37:27.671329',20,'2021-08-31 16:37:27.697133',NULL,'~',1,1),(5,'Santiago','2021-08-31 15:39:09.435977','2021-08-31 16:37:35.852704',21,'2021-08-31 16:37:35.881919',NULL,'~',1,1),(5,'Santiago','2021-08-31 15:39:09.435977','2021-08-31 16:37:53.031565',22,'2021-08-31 16:37:53.089602',NULL,'~',1,1),(5,'Santiago','2021-08-31 15:39:09.435977','2021-08-31 16:37:58.819889',23,'2021-08-31 16:37:58.848547',NULL,'~',1,1),(5,'Santiago','2021-08-31 15:39:09.435977','2021-08-31 16:38:04.753432',24,'2021-08-31 16:38:04.798730',NULL,'~',1,1),(5,'Santiago','2021-08-31 15:39:09.435977','2021-08-31 16:38:29.787117',25,'2021-08-31 16:38:29.848920',NULL,'~',1,1),(6,'Asd','2021-09-03 15:21:35.575566','2021-09-03 15:21:35.575592',26,'2021-09-03 15:21:35.607326',NULL,'+',1,3),(5,'Santiago','2021-08-31 15:39:09.435977','2021-09-03 15:46:19.114722',27,'2021-09-03 15:46:19.150164',NULL,'~',1,3),(6,'Asd','2021-09-03 15:21:35.575566','2021-09-03 16:08:25.726537',28,'2021-09-03 16:08:25.750338',NULL,'~',1,3),(5,'Santiago','2021-08-31 15:39:09.435977','2021-09-03 16:12:16.587589',29,'2021-09-03 16:12:16.640113',NULL,'~',1,3),(5,'Santiago','2021-08-31 15:39:09.435977','2021-09-03 16:12:25.802370',30,'2021-09-03 16:12:25.827691',NULL,'~',1,3),(5,'Santiago','2021-08-31 15:39:09.435977','2021-09-03 16:12:34.250394',31,'2021-09-03 16:12:34.281851',NULL,'~',1,3),(6,'Asd','2021-09-03 15:21:35.575566','2021-09-03 16:14:28.398259',32,'2021-09-03 16:14:28.430911',NULL,'~',1,3),(6,'Asd','2021-09-03 15:21:35.575566','2021-09-03 16:15:34.371235',33,'2021-09-03 16:15:34.399277',NULL,'~',1,3),(5,'Santiago','2021-08-31 15:39:09.435977','2021-09-03 16:15:40.753619',34,'2021-09-03 16:15:40.772636',NULL,'~',1,3),(6,'Asd','2021-09-03 15:21:35.575566','2021-09-03 16:17:30.174406',35,'2021-09-03 16:17:30.197907',NULL,'~',1,3),(7,'Vegurti','2021-09-07 15:25:10.902536','2021-09-07 15:25:10.902558',36,'2021-09-07 15:25:10.930842',NULL,'+',NULL,3),(7,'Vegurti','2021-09-07 15:25:10.902536','2021-09-07 15:27:33.791002',37,'2021-09-07 15:27:33.846901',NULL,'~',NULL,3),(7,'Vegurti','2021-09-07 15:25:10.902536','2021-09-07 15:27:44.427380',38,'2021-09-07 15:27:44.446645',NULL,'~',NULL,3),(7,'Vegurti','2021-09-07 15:25:10.902536','2021-09-07 15:27:56.368054',39,'2021-09-07 15:27:56.387979',NULL,'~',NULL,3),(7,'Vegurti','2021-09-07 15:25:10.902536','2021-09-07 15:27:56.368054',40,'2021-09-07 15:28:27.281772',NULL,'-',NULL,3),(6,'Asdd','2021-09-03 15:21:35.575566','2021-09-07 15:29:44.080007',41,'2021-09-07 15:29:44.113846',NULL,'~',1,3);
/*!40000 ALTER TABLE `pauta_historicalpauta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pauta_ingrediente`
--

DROP TABLE IF EXISTS `pauta_ingrediente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pauta_ingrediente` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `cantidad` double NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `insumo_id` bigint NOT NULL,
  `pauta_id` bigint NOT NULL,
  `unidad` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `pauta_ingrediente_pauta_id_6b30c956_fk_pauta_pauta_id` (`pauta_id`),
  KEY `pauta_ingrediente_insumo_id_6dbb9fb2_fk_nucleo_insumo_id` (`insumo_id`),
  CONSTRAINT `pauta_ingrediente_insumo_id_6dbb9fb2_fk_nucleo_insumo_id` FOREIGN KEY (`insumo_id`) REFERENCES `nucleo_insumo` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `pauta_ingrediente_pauta_id_6b30c956_fk_pauta_pauta_id` FOREIGN KEY (`pauta_id`) REFERENCES `pauta_pauta` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pauta_ingrediente`
--

LOCK TABLES `pauta_ingrediente` WRITE;
/*!40000 ALTER TABLE `pauta_ingrediente` DISABLE KEYS */;
/*!40000 ALTER TABLE `pauta_ingrediente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pauta_instruccion`
--

DROP TABLE IF EXISTS `pauta_instruccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pauta_instruccion` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `orden` int NOT NULL,
  `descripcion` varchar(255) NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `etapa_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `pauta_instruccion_etapa_id_0893b16b_fk_pauta_etapa_id` (`etapa_id`),
  CONSTRAINT `pauta_instruccion_etapa_id_0893b16b_fk_pauta_etapa_id` FOREIGN KEY (`etapa_id`) REFERENCES `pauta_etapa` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pauta_instruccion`
--

LOCK TABLES `pauta_instruccion` WRITE;
/*!40000 ALTER TABLE `pauta_instruccion` DISABLE KEYS */;
INSERT INTO `pauta_instruccion` VALUES (14,0,'Calentar el Queso','2021-08-31 13:15:21.771800','2021-08-31 16:00:18.334803',6),(17,0,'Bailar con el queso hasta que no de más','2021-08-31 15:05:18.462649','2021-08-31 16:00:18.402705',7),(18,0,'A dormir se ha dicho','2021-08-31 15:05:18.562420','2021-08-31 16:00:18.477925',8),(19,1,'Bailamos?','2021-08-31 15:05:18.741818','2021-08-31 16:00:18.513940',8),(20,0,'Ponte de pie','2021-08-31 15:31:45.247879','2021-08-31 15:31:45.247901',9),(21,1,'baila','2021-08-31 15:31:45.307570','2021-08-31 15:31:45.307635',9),(22,2,'danza','2021-08-31 15:31:45.406153','2021-08-31 15:31:45.406174',9),(23,0,'Ponte de pie','2021-08-31 15:32:13.639443','2021-08-31 15:32:13.639488',10),(24,1,'baila','2021-08-31 15:32:13.789416','2021-08-31 15:32:13.789436',10),(25,2,'danza','2021-08-31 15:32:13.881273','2021-08-31 15:32:13.881294',10),(37,0,'Calentar el Queso','2021-08-31 16:38:30.204274','2021-09-03 16:15:40.983810',11),(38,0,'xdas','2021-09-03 15:21:35.898935','2021-09-07 15:29:44.540922',12);
/*!40000 ALTER TABLE `pauta_instruccion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pauta_instruccioncolumna`
--

DROP TABLE IF EXISTS `pauta_instruccioncolumna`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pauta_instruccioncolumna` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `columna_id` bigint NOT NULL,
  `instruccion_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `pauta_instruccioncolumna_columna_id_0018225e_fk_pauta_columna_id` (`columna_id`),
  KEY `pauta_instruccioncol_instruccion_id_06e2f729_fk_pauta_ins` (`instruccion_id`),
  CONSTRAINT `pauta_instruccioncol_instruccion_id_06e2f729_fk_pauta_ins` FOREIGN KEY (`instruccion_id`) REFERENCES `pauta_instruccion` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `pauta_instruccioncolumna_columna_id_0018225e_fk_pauta_columna_id` FOREIGN KEY (`columna_id`) REFERENCES `pauta_columna` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=75 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pauta_instruccioncolumna`
--

LOCK TABLES `pauta_instruccioncolumna` WRITE;
/*!40000 ALTER TABLE `pauta_instruccioncolumna` DISABLE KEYS */;
INSERT INTO `pauta_instruccioncolumna` VALUES (27,'2021-08-31 13:15:21.797495','2021-08-31 13:15:21.797539',1,14),(28,'2021-08-31 15:04:06.349888','2021-08-31 15:04:06.349909',2,14),(33,'2021-08-31 15:05:18.488023','2021-08-31 15:05:18.488046',1,17),(34,'2021-08-31 15:05:18.512649','2021-08-31 15:05:18.512672',2,17),(35,'2021-08-31 15:05:18.646018','2021-08-31 15:05:18.646040',1,18),(36,'2021-08-31 15:05:18.696081','2021-08-31 15:05:18.696104',2,18),(37,'2021-08-31 15:05:18.777527','2021-08-31 15:05:18.777549',1,19),(38,'2021-08-31 15:05:18.795842','2021-08-31 15:05:18.795865',2,19),(39,'2021-08-31 15:31:45.273930','2021-08-31 15:31:45.274009',1,20),(40,'2021-08-31 15:31:45.331029','2021-08-31 15:31:45.331062',1,21),(41,'2021-08-31 15:31:45.431178','2021-08-31 15:31:45.431200',1,22),(42,'2021-08-31 15:32:13.714926','2021-08-31 15:32:13.714959',1,23),(43,'2021-08-31 15:32:13.845587','2021-08-31 15:32:13.845626',1,24),(44,'2021-08-31 15:32:13.906521','2021-08-31 15:32:13.906545',1,25),(71,'2021-08-31 16:38:30.257613','2021-08-31 16:38:30.257657',1,37),(72,'2021-08-31 16:38:30.281691','2021-08-31 16:38:30.281713',2,37),(73,'2021-09-03 15:21:35.998904','2021-09-03 15:21:35.998925',1,38),(74,'2021-09-03 16:17:30.635374','2021-09-03 16:17:30.635396',2,38);
/*!40000 ALTER TABLE `pauta_instruccioncolumna` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pauta_pauta`
--

DROP TABLE IF EXISTS `pauta_pauta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pauta_pauta` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `rama_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `pauta_pauta_rama_id_0ba160ef_fk_nucleo_rama_id` (`rama_id`),
  CONSTRAINT `pauta_pauta_rama_id_0ba160ef_fk_nucleo_rama_id` FOREIGN KEY (`rama_id`) REFERENCES `nucleo_rama` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pauta_pauta`
--

LOCK TABLES `pauta_pauta` WRITE;
/*!40000 ALTER TABLE `pauta_pauta` DISABLE KEYS */;
INSERT INTO `pauta_pauta` VALUES (2,'Cottage','2021-08-31 09:39:37.682164','2021-08-31 16:00:18.115968',NULL),(3,'Queso Campo','2021-08-31 15:31:45.019988','2021-08-31 15:31:45.020009',NULL),(4,'Queso Campo','2021-08-31 15:32:13.310752','2021-08-31 15:32:13.310807',NULL),(5,'Santiago','2021-08-31 15:39:09.435977','2021-09-03 16:15:40.753619',3),(6,'Asdd','2021-09-03 15:21:35.575566','2021-09-07 15:29:44.080007',3);
/*!40000 ALTER TABLE `pauta_pauta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pauta_pauta_columnas`
--

DROP TABLE IF EXISTS `pauta_pauta_columnas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pauta_pauta_columnas` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `pauta_id` bigint NOT NULL,
  `columna_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `pauta_pauta_columnas_pauta_id_columna_id_3988f582_uniq` (`pauta_id`,`columna_id`),
  KEY `pauta_pauta_columnas_columna_id_0a91a10c_fk_pauta_columna_id` (`columna_id`),
  CONSTRAINT `pauta_pauta_columnas_columna_id_0a91a10c_fk_pauta_columna_id` FOREIGN KEY (`columna_id`) REFERENCES `pauta_columna` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `pauta_pauta_columnas_pauta_id_fb92a222_fk_pauta_pauta_id` FOREIGN KEY (`pauta_id`) REFERENCES `pauta_pauta` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pauta_pauta_columnas`
--

LOCK TABLES `pauta_pauta_columnas` WRITE;
/*!40000 ALTER TABLE `pauta_pauta_columnas` DISABLE KEYS */;
INSERT INTO `pauta_pauta_columnas` VALUES (3,2,1),(4,2,2),(5,3,1),(6,4,1),(7,5,1),(12,5,2),(13,6,1),(14,6,2);
/*!40000 ALTER TABLE `pauta_pauta_columnas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pauta_pautacolumna`
--

DROP TABLE IF EXISTS `pauta_pautacolumna`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pauta_pautacolumna` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `columna_id` bigint NOT NULL,
  `pauta_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `pauta_pautacolumna_columna_id_b9b8557e_fk_pauta_columna_id` (`columna_id`),
  KEY `pauta_pautacolumna_pauta_id_90b4c443_fk_pauta_pauta_id` (`pauta_id`),
  CONSTRAINT `pauta_pautacolumna_columna_id_b9b8557e_fk_pauta_columna_id` FOREIGN KEY (`columna_id`) REFERENCES `pauta_columna` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `pauta_pautacolumna_pauta_id_90b4c443_fk_pauta_pauta_id` FOREIGN KEY (`pauta_id`) REFERENCES `pauta_pauta` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pauta_pautacolumna`
--

LOCK TABLES `pauta_pautacolumna` WRITE;
/*!40000 ALTER TABLE `pauta_pautacolumna` DISABLE KEYS */;
/*!40000 ALTER TABLE `pauta_pautacolumna` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `perfil_perfil`
--

DROP TABLE IF EXISTS `perfil_perfil`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `perfil_perfil` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `avatar` varchar(100) DEFAULT NULL,
  `pin` varchar(4) NOT NULL,
  `firma_digital` varchar(100) DEFAULT NULL,
  `usuario_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `perfil_perfil_usuario_id_7f05c1ac_uniq` (`usuario_id`),
  CONSTRAINT `perfil_perfil_usuario_id_7f05c1ac_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `perfil_perfil`
--

LOCK TABLES `perfil_perfil` WRITE;
/*!40000 ALTER TABLE `perfil_perfil` DISABLE KEYS */;
INSERT INTO `perfil_perfil` VALUES (2,'profiles/djangopermisos_tClO8Ya.png','1234','firmas/800px-Miguel_Díaz-Canel_firma.png',1),(5,'','4913','firmas/IMG_8329.jpg',11),(17,'','2530','',26),(24,'','4244','',33),(25,'','0347','',34),(27,'','8928','',36),(28,'','7298','',37),(29,'','7132','',38),(30,'','0779','',39),(31,'','4147','',40),(32,'','6429','',41),(33,'','0911','',42);
/*!40000 ALTER TABLE `perfil_perfil` ENABLE KEYS */;
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
  `banco` varchar(255) DEFAULT NULL,
  `cuenta_corriente` varchar(255) DEFAULT NULL,
  `transferencia_email` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `empresa_rut` (`empresa_rut`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proveedores_proveedor`
--

LOCK TABLES `proveedores_proveedor` WRITE;
/*!40000 ALTER TABLE `proveedores_proveedor` DISABLE KEYS */;
INSERT INTO `proveedores_proveedor` VALUES (1,'Ingredion Chile S.A.','82.525.800-0','Ingredientes','Coquimbo','Coquimbo',NULL,NULL,'efren@ingredion.cl',NULL,'2021-08-31 10:01:26.667256','2021-09-07 09:33:29.438861','BANCO_ESTADO',NULL,NULL),(2,'FIBRO CHILE','96863240-K',NULL,'Metropolitana','Cerrillos',NULL,'Verónica Poblete','vpoblete@freevac.cl','+56998738195','2021-10-25 17:23:42.054858','2021-10-25 17:23:42.059588',NULL,NULL,NULL),(3,'PRINAL LTDA','83877600-0',NULL,NULL,'Selecciona una región',NULL,NULL,'alejandra_ervet@prinal.com','999915513','2021-10-25 17:41:10.223123','2021-10-25 17:41:10.233508',NULL,NULL,NULL),(4,'DILACO','83083700-0',NULL,NULL,'Selecciona una región',NULL,NULL,'ksanhueza@dilaco.com',NULL,'2021-10-26 13:57:32.125505','2021-10-26 13:57:32.128652',NULL,NULL,NULL),(5,'MARPLE','76350147-7',NULL,NULL,'Selecciona una región',NULL,NULL,'jcaripan@marple.cl',NULL,'2021-10-27 10:13:49.682909','2021-10-27 10:13:49.689706',NULL,NULL,NULL),(6,'COEXPAN','95590620-7',NULL,NULL,'Selecciona una región',NULL,NULL,'Bgonzalez@coexpan.cl',NULL,'2021-11-02 16:28:24.166299','2021-11-02 16:28:24.170829',NULL,NULL,NULL),(7,'ABASTOPLAST','78.737.530-8',NULL,NULL,'Selecciona una región',NULL,NULL,'m.cabrera@abastoplast.cl',NULL,'2021-11-04 10:21:26.331462','2021-11-04 10:21:26.337544',NULL,NULL,NULL),(8,'INTEGRITY','96.733.780-3',NULL,NULL,'Selecciona una región',NULL,NULL,'pgallegos@integrity.cl',NULL,'2021-11-08 10:55:13.255575','2021-11-08 10:55:13.259451',NULL,NULL,NULL),(9,'PRIMEC','76.042.392-0',NULL,NULL,'Selecciona una región',NULL,NULL,'jfaure@primec.cl',NULL,'2021-11-08 11:36:56.200388','2021-11-08 11:36:56.209295',NULL,NULL,NULL),(10,'FLORAMATIC','82.062.500-5',NULL,NULL,'Selecciona una región',NULL,NULL,'isabel.rozas@floramatic.com',NULL,'2021-11-09 09:23:41.450109','2021-11-09 09:23:41.456109',NULL,NULL,NULL),(11,'DIPISA','93.558.000-5',NULL,NULL,'Selecciona una región',NULL,NULL,'pfuentes@dipisa.cl',NULL,'2021-11-09 10:11:54.945725','2021-11-09 10:11:54.949823',NULL,NULL,NULL),(12,'DITZLER','96.678.110-6',NULL,NULL,'Selecciona una región',NULL,NULL,'andres.rodriguez@ditzler.cl',NULL,'2021-11-09 10:22:17.362046','2021-11-09 10:22:17.365711',NULL,NULL,NULL);
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
  `lead` int NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `insumo_id` bigint NOT NULL,
  `proveedor_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `proveedores_proveedo_insumo_id_2c8f16a6_fk_nucleo_in` (`insumo_id`),
  KEY `proveedores_proveedo_proveedor_id_1c2ccbcd_fk_proveedor` (`proveedor_id`),
  CONSTRAINT `proveedores_proveedo_insumo_id_2c8f16a6_fk_nucleo_in` FOREIGN KEY (`insumo_id`) REFERENCES `nucleo_insumo` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `proveedores_proveedo_proveedor_id_1c2ccbcd_fk_proveedor` FOREIGN KEY (`proveedor_id`) REFERENCES `proveedores_proveedor` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proveedores_proveedorinsumo`
--

LOCK TABLES `proveedores_proveedorinsumo` WRITE;
/*!40000 ALTER TABLE `proveedores_proveedorinsumo` DISABLE KEYS */;
INSERT INTO `proveedores_proveedorinsumo` VALUES (5,'6420',25,1400,5,'2021-10-22 10:11:11.676639','2021-10-22 10:11:11.676661',3,1),(6,'Bolsa Vacio',1,27,30,'2021-10-25 17:24:20.383017','2021-10-25 17:24:20.383033',6,2),(7,'LACTOSA',25,3500,10,'2021-10-25 17:42:02.460963','2021-11-02 15:35:55.730203',7,3),(8,'SAL FUNDENTE ST-115',5,4565,10,'2021-10-25 17:42:47.741563','2021-11-02 15:35:54.359308',8,3),(9,'SAL 1054',1,5500,10,'2021-10-26 16:16:05.908688','2021-11-02 15:21:53.606418',12,3),(10,'POTE 200795 C/TAPA',840,79800,20,'2021-10-27 10:15:32.078563','2021-11-02 15:35:03.274386',13,5),(11,'ACIDO CITRICO',1,1350,15,'2021-10-28 12:22:11.215855','2021-10-28 12:22:11.215875',14,3),(12,'TAPA CORONA GENERICA',1,18.44,20,'2021-11-02 16:29:36.953084','2021-11-02 17:00:44.394289',17,6),(13,'BOTELLA + TAPA BLANCA',1,313,30,'2021-11-04 10:23:00.749901','2021-11-04 10:23:00.749919',19,7),(14,'BOTELLA + TAPA TRANSPARENTE',1,288,30,'2021-11-04 10:24:58.901173','2021-11-04 10:24:58.901195',18,7),(15,'40-12 FL * 540 UN',540,22014,20,'2021-11-08 10:56:40.072120','2021-11-09 16:32:28.509478',20,8),(16,'LECHE EN POLVO DESCREMADA',25,64750,10,'2021-11-08 11:40:39.758992','2021-11-08 11:40:39.759014',21,9),(17,'LECHE EN POLVO DESCREMADA',1,2590,10,'2021-11-08 11:41:13.393378','2021-11-09 17:17:31.686024',21,9),(18,'AZUCAR GRADO 2',1,665,10,'2021-11-08 11:41:54.260766','2021-11-09 17:17:31.699232',22,9),(19,'GELATINA220-BLOOM',1,7017.51,15,'2021-11-09 09:28:05.170393','2021-11-09 10:48:15.643297',24,10),(20,'SALSA DURAZNO',1,1850,40,'2021-11-09 10:25:59.797543','2021-11-09 10:25:59.797563',29,12),(21,'SALSA FRUTILLA',1,1850,40,'2021-11-09 10:26:26.639967','2021-11-09 10:26:26.639999',28,12),(22,'R-704',1,5250,7,'2021-11-09 17:35:56.224191','2021-11-09 17:35:56.224213',11,4),(23,'CAJA RESMA',10,20630,15,'2021-11-09 18:05:47.422921','2021-11-09 18:05:47.422949',27,11),(24,'TOALLA INTERFOLIADA',1,18389,15,'2021-11-09 18:06:28.958996','2021-11-09 18:06:28.959015',25,11);
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

-- Dump completed on 2021-11-09 21:26:54
