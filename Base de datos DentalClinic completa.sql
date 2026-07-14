-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: dentalclinic
-- ------------------------------------------------------
-- Server version	8.0.46

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
-- Dumping data for table `catalogo_tratamientos`
--

LOCK TABLES `catalogo_tratamientos` WRITE;
/*!40000 ALTER TABLE `catalogo_tratamientos` DISABLE KEYS */;
INSERT INTO `catalogo_tratamientos` VALUES (1,'Limpieza dental',35000.00,1),(2,'Destartraje',45000.00,1),(3,'Resina simple',45000.00,1),(4,'Resina compuesta',55000.00,1),(5,'Obturación temporal',30000.00,1),(6,'Endodoncia',180000.00,1),(7,'Corona dental',220000.00,1),(8,'Extracción simple',50000.00,1),(9,'Extracción quirúrgica',95000.00,1),(10,'Implante dental',850000.00,1),(11,'Blanqueamiento',120000.00,1),(12,'Prótesis parcial',450000.00,1),(13,'Prótesis total',650000.00,1),(14,'Sellantes',30000.00,1),(15,'Aplicación de flúor',25000.00,1);
/*!40000 ALTER TABLE `catalogo_tratamientos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `citas`
--

LOCK TABLES `citas` WRITE;
/*!40000 ALTER TABLE `citas` DISABLE KEYS */;
INSERT INTO `citas` VALUES (1,1,1,'2026-06-24','10:00',30,'Control general','PROGRAMADA'),(2,2,1,'2026-07-10','10:00',30,'Evaluación','PROGRAMADA'),(3,2,2,'2026-07-11','10:00',90,'Tratamiento','CONFIRMADA'),(4,3,2,'2026-07-10','09:30',30,'Control','PROGRAMADA'),(5,4,2,'2026-07-13','14:00',45,'Evaluación','PROGRAMADA');
/*!40000 ALTER TABLE `citas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `detalle_presupuesto`
--

LOCK TABLES `detalle_presupuesto` WRITE;
/*!40000 ALTER TABLE `detalle_presupuesto` DISABLE KEYS */;
INSERT INTO `detalle_presupuesto` VALUES (1,1,14,1,30000.00,30000.00);
/*!40000 ALTER TABLE `detalle_presupuesto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `documentos`
--

LOCK TABLES `documentos` WRITE;
/*!40000 ALTER TABLE `documentos` DISABLE KEYS */;
INSERT INTO `documentos` VALUES (1,2,4,'prueba','uploads/documentos/Mystification_Palette_Title_Elegant_Blue_Serenity_Color_Palette_.jpg','2026-07-09'),(2,2,3,'Imagen de prueba','uploads/documentos/descarga_1.jpg','2026-07-13');
/*!40000 ALTER TABLE `documentos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `evoluciones`
--

LOCK TABLES `evoluciones` WRITE;
/*!40000 ALTER TABLE `evoluciones` DISABLE KEYS */;
INSERT INTO `evoluciones` VALUES (1,7,2,'2026-07-12','Prueba de evolución.','');
/*!40000 ALTER TABLE `evoluciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `pacientes`
--

LOCK TABLES `pacientes` WRITE;
/*!40000 ALTER TABLE `pacientes` DISABLE KEYS */;
INSERT INTO `pacientes` VALUES (1,'12.345.678-9','Gabriel','Romero','+56 9 8765 4321','gabriel@email.cl','Peñalolén, Santiago','2014-03-14','ACTIVO'),(2,'19.490.049-K','Fernanda','Julio Reynals','+56 9 1234 5678','fernanda@correo.com','Avenida Grecia, Santiago','1997-02-27','ACTIVO'),(3,'17.123.456-7','Joanny','Romero','+56 9 8765 4321','joanny@correo.com','Av Grecia, Peñalolen','1991-03-30','ACTIVO'),(4,'20.234.567-8','Freya','Romero','+56 9 1234 5678','fernanda@gmail.com','Avenida Grecia, Santiago','2023-11-13','ACTIVO');
/*!40000 ALTER TABLE `pacientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `pagos`
--

LOCK TABLES `pagos` WRITE;
/*!40000 ALTER TABLE `pagos` DISABLE KEYS */;
INSERT INTO `pagos` VALUES (1,2,1,'2026-07-10 20:01:17',10000.00,'EFECTIVO','Abono de tratamiento','REGISTRADO'),(2,2,1,'2026-07-10 20:02:34',5000.00,'DEBITO','Abono','ANULADO'),(3,1,1,'2026-07-13 20:20:59',80000.00,'DEBITO','Abona para el tratamiento total.','REGISTRADO');
/*!40000 ALTER TABLE `pagos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `presupuestos`
--

LOCK TABLES `presupuestos` WRITE;
/*!40000 ALTER TABLE `presupuestos` DISABLE KEYS */;
INSERT INTO `presupuestos` VALUES (1,'PRES-000001',1,1,'2026-07-06','2026-08-04','PENDIENTE',30000.00,'');
/*!40000 ALTER TABLE `presupuestos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'Administrador','Acceso completo al sistema'),(2,'Recepcionista','Gestión de agenda, pacientes y documentos'),(3,'Odontólogo','Gestión clínica, tratamientos y evoluciones');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `tipos_documento`
--

LOCK TABLES `tipos_documento` WRITE;
/*!40000 ALTER TABLE `tipos_documento` DISABLE KEYS */;
INSERT INTO `tipos_documento` VALUES (1,'Consentimiento informado','Documento de autorización del paciente'),(2,'Presupuesto','Documento asociado al plan de tratamiento'),(3,'Radiografía','Imagen clínica del paciente'),(4,'Comprobante','Documento de pago o respaldo administrativo');
/*!40000 ALTER TABLE `tipos_documento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `tratamientos`
--

LOCK TABLES `tratamientos` WRITE;
/*!40000 ALTER TABLE `tratamientos` DISABLE KEYS */;
INSERT INTO `tratamientos` VALUES (1,1,1,'Tratamiento indicado por caries en pieza dental',45000.00,'PLANIFICADO','2026-06-24',NULL,NULL),(2,2,1,'',50000.00,'PLANIFICADO',NULL,15,NULL),(3,2,1,'',25000.00,'PLANIFICADO',NULL,15,NULL),(4,2,1,'',180000.00,'PLANIFICADO',NULL,6,'16'),(5,2,1,'',180000.00,'PLANIFICADO',NULL,6,'26'),(6,2,1,'',55000.00,'PLANIFICADO',NULL,4,'16'),(7,2,1,'',55000.00,'PLANIFICADO',NULL,4,'26'),(8,1,1,'',25000.00,'PLANIFICADO',NULL,15,NULL),(9,1,1,'',35000.00,'PLANIFICADO',NULL,1,NULL),(10,1,1,'',45000.00,'PLANIFICADO',NULL,3,'17'),(11,1,1,'',45000.00,'PLANIFICADO',NULL,3,'35'),(12,4,1,'Limpieza general',45000.00,'PLANIFICADO',NULL,2,NULL);
/*!40000 ALTER TABLE `tratamientos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'19.490.049-K','Fernanda Julio','fernanda@gestiondental.cl','scrypt:32768:8:1$DDWxCUHxBB4FVg2e$3f565e154b043a71527f9a2f9b11dde19a4e21ddf326603f3cef54199bbbcb6d96a5a4eaba75a8ad3eae579d30538a20be0e2e092a3965d2ca0501d358b843cc',1,'ACTIVO'),(2,'18.111.111-1','Dra. Camila Rojas','camila@gestiondental.cl','scrypt:32768:8:1$NEJcwavtxmbER6jl$bf0f076329807aaefee42a5f18c61b455bc63e8246ee23ccbb237ca4c07baa6a9baeb27b16bed1d61f10f7adf1b9ce9cb84b3150a8cf036b1ada4cf8cfc57028',3,'ACTIVO'),(3,'11.111.111-1','Usuario Administrador','administrador@gestiondental.cl','scrypt:32768:8:1$JoNC1bwHjBLfllD0$7af69bc27bc250c354e49aaca3074ab950a6ce4b62d9ab691b9871bede8f513a31e1848ccf60701de6ad5683d30ec51f89058219a6419b5afe4c22022daa5241',1,'ACTIVO'),(4,'22.222.222-2','Recepcionista','recepcionista@gestiondental.cl','scrypt:32768:8:1$tAZGBWGcDXAd1YfM$8e88f93ad25ff7d4c3aed00b8597a112f984d9e400d5ea1aea39c2cf213b1a8a297cf4bcfe425f71abd726edb330d5f100ac06ef4f1b0cdae4074314f795d979',2,'ACTIVO');
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-07-13 22:05:43
