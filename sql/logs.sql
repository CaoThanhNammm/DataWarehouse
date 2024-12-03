/*
 Navicat Premium Data Transfer

 Source Server         : Localhost
 Source Server Type    : MySQL
 Source Server Version : 100428
 Source Host           : localhost:3306
 Source Schema         : control

 Target Server Type    : MySQL
 Target Server Version : 100428
 File Encoding         : 65001

 Date: 14/11/2024 18:51:34
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for logs
-- ----------------------------
DROP TABLE IF EXISTS `logs`;
CREATE TABLE `logs`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `message` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `quantity` int NULL DEFAULT NULL,
  `statusId` int NULL DEFAULT NULL,
  `websiteId` int NULL DEFAULT NULL,
  `timeStart` datetime(6) NULL DEFAULT NULL,
  `timeEnd` datetime(6) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `FK3d5jkj33k7m98tttikpva61fh`(`statusId` ASC) USING BTREE,
  INDEX `FKdc4xf5e5rg9n4avr0sk1b1d4x`(`websiteId` ASC) USING BTREE,
  CONSTRAINT `logs_ibfk_1` FOREIGN KEY (`statusId`) REFERENCES `status` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `logs_ibfk_2` FOREIGN KEY (`websiteId`) REFERENCES `control` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 53 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of logs
-- ----------------------------
INSERT INTO `logs` VALUES (29, 'starting scrape data', 0, 2, 4, '2024-11-07 22:41:10.000000', NULL);
INSERT INTO `logs` VALUES (30, 'complete scrape data', 1206, 3, 4, '2024-11-07 22:41:10.000000', '2024-11-08 00:00:01.000000');
INSERT INTO `logs` VALUES (31, 'complete scrape data', 958, 3, 1, '2024-11-07 22:41:09.000000', '2024-11-08 00:23:58.000000');
INSERT INTO `logs` VALUES (32, 'starting scrape data', 0, 2, 1, '2024-11-11 20:05:07.000000', NULL);
INSERT INTO `logs` VALUES (34, 'complete scrape data', 1135, 3, 4, '2024-11-11 22:27:43.000000', '2024-11-11 23:36:36.000000');
INSERT INTO `logs` VALUES (35, 'Load Data From Staging to Data Warehouse', 1359, 3, NULL, '2024-11-14 00:02:03.000000', '2024-11-14 00:02:08.000000');

SET FOREIGN_KEY_CHECKS = 1;
