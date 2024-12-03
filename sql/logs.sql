/*
 Navicat Premium Data Transfer

 Source Server         : bainguoita
 Source Server Type    : MySQL
 Source Server Version : 100428
 Source Host           : localhost:3306
 Source Schema         : control_db

 Target Server Type    : MySQL
 Target Server Version : 100428
 File Encoding         : 65001

 Date: 25/11/2024 16:28:04
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for logs
-- ----------------------------
DROP TABLE IF EXISTS `logs`;
CREATE TABLE `logs`  (
  `log_id` int NOT NULL AUTO_INCREMENT,
  `file_id` int NULL DEFAULT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `log_message` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `timeStart` datetime(6) NULL DEFAULT current_timestamp(6),
  `timeEnd` datetime(6) NULL DEFAULT NULL,
  PRIMARY KEY (`log_id`) USING BTREE,
  INDEX `file_id`(`file_id` ASC) USING BTREE,
  CONSTRAINT `logs_ibfk_1` FOREIGN KEY (`file_id`) REFERENCES `config` (`file_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 60 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of logs
-- ----------------------------
INSERT INTO `logs` VALUES (1, 1, 'Success', 'Load dữ liệu về file csv', '2024-11-25 02:03:52.000000', '2024-11-25 02:04:30.000000');

SET FOREIGN_KEY_CHECKS = 1;
