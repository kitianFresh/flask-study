DROP DATABASE IF EXISTS `huajiaogirls`;
CREATE DATABASE `huajiaogirls` DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_general_ci;
USE `huajiaogirls`;
set names utf8mb4;

DROP TABLE IF EXISTS `Tbl_Huajiao_Live`;
CREATE TABLE `Tbl_Huajiao_Live` (
    `FLiveId` INT UNSIGNED NOT NULL,
    `FUserId` INT UNSIGNED NOT NULL,
    `FWatches` INT UNSIGNED NOT NULL DEFAULT 0  COMMENT '观看人数',
    `FPraises` INT UNSIGNED NOT NULL DEFAULT 0  COMMENT '赞数',
    `FReposts` INT UNSIGNED NOT NULL DEFAULT 0  COMMENT 'unknown',
    `FReplies` INT UNSIGNED NOT NULL DEFAULT 0  COMMENT 'unknown',
    `FPublishTimestamp` INT UNSIGNED NOT NULL COMMENT '发布日期',
    `FTitle` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '直播名称',
    `FImage` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '直播封面',
    `FLocation` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '地点',
    `FScrapedTime` timestamp NOT NULL COMMENT '爬虫更新时间',
    PRIMARY KEY (`FLiveId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS `Tbl_Huajiao_User`;
CREATE TABLE `Tbl_Huajiao_User` (
    `FUserId` INT UNSIGNED NOT NULL,
    `FUserName` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '昵称',
    `FLevel` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '等级',
    `FFollow` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '关注数',
    `FFollowed` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '粉丝数',
    `FSupported` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '赞数',
    `FExperience` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '经验值',
    `FAvatar` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '头像地址',
    `FScrapedTime` timestamp NOT NULL COMMENT '爬虫时间',
    PRIMARY KEY (`FUserId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS `Tbl_Beauty_Face`;
CREATE TABLE `Tbl_Beauty_Face` (
    `FFaceId` INT UNSIGNED  AUTO_INCREMENT NOT NULL,
    `FImageUrl` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '图片URL',
    `FImageOriginal` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '原始图片路径',
    `FImageFiltered` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '过滤后图片路径',
    `FImageLandmarks` JSON NOT NULL COMMENT '人脸识别的各种特征点',
    PRIMARY KEY (`FFaceId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;